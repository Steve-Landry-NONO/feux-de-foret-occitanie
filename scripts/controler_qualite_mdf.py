"""Contrôles qualité reproductibles des archives Météo des forêts (ticket #14).

Usage :
    python scripts/controler_qualite_mdf.py FICHIER.csv.gz [...] [--manifest manifest.json]

Les règles contrôlées sont décrites dans docs/qualite/registre-regles-qualite.md
(identifiants MDF-xx). Le script lit les fichiers sans les modifier et n'utilise
que la bibliothèque standard. Il ne valide pas la sémantique des prévisions
(date d'émission ou de validité) : ce point reste à confirmer auprès du producteur.
"""
import argparse
import csv
import gzip
import hashlib
import io
import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

OCCITANIE = {"09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"}
COLONNES_ATTENDUES = {"date", "num_dep", "niveau_j1", "niveau_j2", "nom_dep"}
ALIAS = {"dep_nom": "nom_dep"}
NIVEAUX = {"1", "2", "3", "4"}


def lire(chemin):
    brut = Path(chemin).read_bytes()
    texte = gzip.decompress(brut).decode("utf-8-sig")
    entete = next(iter(texte.splitlines()), "")
    sep = ";" if entete.count(";") > entete.count(",") else ","
    lignes = list(csv.DictReader(io.StringIO(texte), delimiter=sep))
    return brut, sep, entete.split(sep), lignes


def code_dep(valeur):
    v = (valeur or "").strip()
    return v.zfill(2) if v.isdigit() else v.upper()


def jour(valeur):
    try:
        return datetime.fromisoformat(valeur.strip().replace("Z", "+00:00")).date()
    except (AttributeError, ValueError):
        return None


def controler(chemin, manifest):
    brut, sep, colonnes, lignes = lire(chemin)
    res = {"fichier": Path(chemin).name, "lignes": len(lignes), "separateur": sep}

    # MDF-01 Schéma : colonnes attendues après normalisation des alias documentés
    normalisees = {ALIAS.get(c, c) for c in colonnes}
    res["MDF-01_alias_utilises"] = sorted(c for c in colonnes if c in ALIAS)
    res["MDF-01_colonnes_manquantes"] = sorted(COLONNES_ATTENDUES - normalisees)
    res["MDF-01_colonnes_inattendues"] = sorted(normalisees - COLONNES_ATTENDUES)

    # MDF-02 Intégrité : empreinte identique au manifeste de collecte
    attendu = (manifest or {}).get(Path(chemin).name)
    res["sha256_source"] = hashlib.sha256(brut).hexdigest()
    res["MDF-02_statut"] = ("NON_CONTROLE" if not attendu and manifest is None else
                            "ECHEC" if not attendu or res["sha256_source"] != attendu else "CONFORME")
    res["MDF-02_sha256_conforme"] = (
        None if not attendu else hashlib.sha256(brut).hexdigest() == attendu
    )

    # MDF-08 Format des codes département (01 vs 1)
    res["MDF-08_codes_sans_zero_initial"] = sum(
        1 for l in lignes if (l.get("num_dep") or "").strip().isdigit()
        and len(l["num_dep"].strip()) == 1
    )

    occ = [l for l in lignes if code_dep(l.get("num_dep")) in OCCITANIE]
    res["lignes_occitanie"] = len(occ)

    # MDF-03 Validité des dates
    jours = [jour(l.get("date")) for l in occ]
    res["MDF-03_dates_invalides"] = sum(1 for j in jours if j is None)

    # MDF-04 Unicité département × jour
    cles = Counter((code_dep(l["num_dep"]), j) for l, j in zip(occ, jours) if j)
    res["MDF-04_doublons_dep_jour"] = sum(n - 1 for n in cles.values() if n > 1)

    # MDF-05 Domaine des niveaux (nul compté à part de hors domaine)
    for col in ("niveau_j1", "niveau_j2"):
        vals = [(l.get(col) or "").strip() for l in occ]
        res[f"MDF-05_{col}_vides"] = sum(1 for v in vals if v == "")
        res[f"MDF-05_{col}_hors_domaine"] = sum(1 for v in vals if v and v not in NIVEAUX)
        res[f"MDF-05_{col}_distribution"] = dict(sorted(Counter(vals).items()))

    # MDF-06 Complétude de population : 13 départements chaque jour publié
    par_jour = defaultdict(set)
    for l, j in zip(occ, jours):
        if j:
            par_jour[j].add(code_dep(l["num_dep"]))
    incomplets = {str(j): sorted(OCCITANIE - d) for j, d in par_jour.items() if d != OCCITANIE}
    res["MDF-06_jours_publies"] = len(par_jour)
    res["MDF-06_jours_population_incomplete"] = incomplets

    # MDF-07 Continuité du calendrier entre première et dernière date
    if par_jour:
        debut, fin = min(par_jour), max(par_jour)
        attendus = {debut + timedelta(days=i) for i in range((fin - debut).days + 1)}
        res["MDF-07_periode"] = [str(debut), str(fin)]
        res["MDF-07_jours_absents"] = sorted(str(j) for j in attendus - set(par_jour))

    # MDF-09 Horodatage : nombre d'heures de publication distinctes par jour (information)
    heures = defaultdict(set)
    for l, j in zip(occ, jours):
        if j:
            heures[j].add(l["date"].strip()[11:19])
    res["MDF-09_jours_plusieurs_horodatages"] = sum(1 for h in heures.values() if len(h) > 1)
    return res


def statut(r):
    bloquants = [
        bool(r["MDF-01_colonnes_manquantes"]),
        r["MDF-02_statut"] == "ECHEC",
        r["lignes_occitanie"] == 0,
        r["MDF-06_jours_publies"] == 0,
        r["MDF-05_niveau_j1_vides"] > 0,
        r["MDF-05_niveau_j2_vides"] > 0,
        r["MDF-02_sha256_conforme"] is False,
        r["MDF-03_dates_invalides"] > 0,
        r["MDF-04_doublons_dep_jour"] > 0,
        r["MDF-05_niveau_j1_hors_domaine"] > 0,
        r["MDF-05_niveau_j2_hors_domaine"] > 0,
    ]
    if any(bloquants):
        return "ECHEC"
    if r["MDF-02_statut"] == "NON_CONTROLE":
        return "NON_CONTROLE"
    return "CONFORME_SUR_REGLES_BLOQUANTES"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("fichiers", nargs="+")
    p.add_argument("--manifest")
    p.add_argument("--commit-source", help="SHA du commit des données source")
    a = p.parse_args(argv)
    manifest = None
    if a.manifest:
        manifest = {}
        for e in json.loads(Path(a.manifest).read_text(encoding="utf-8"))["extractions"]:
            manifest[Path(e["fichier"]).name] = e.get("sha256")
    sortie = {"date_execution": date.today().isoformat(), "commit_source": a.commit_source, "resultats": []}
    for f in a.fichiers:
        r = controler(f, manifest)
        r["statut"] = statut(r)
        sortie["resultats"].append(r)
    json.dump(sortie, sys.stdout, ensure_ascii=False, indent=2)
    print()
    if any(r["statut"] == "ECHEC" for r in sortie["resultats"]):
        return 1
    return 2 if any(r["statut"] == "NON_CONTROLE" for r in sortie["resultats"]) else 0


if __name__ == "__main__":
    sys.exit(main())
