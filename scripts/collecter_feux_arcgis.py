#!/usr/bin/env python3
"""Récupérer des incendies 2024–2025 d'une couche ArcGIS secondaire dérivée de BDIFF.

ATTENTION : cette source est diffusée par Esri France à partir de données IGNF /
Géorisques. Elle ne remplace pas un export officiel BDIFF et sa licence de
redistribution reste à vérifier. Les données brutes restent dans data/raw/
et ne sont PAS commitées ; seul le rapport agrégé est destiné au dépôt.
"""
import csv
import hashlib
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

LAYERS = {
    "2024": "https://services.arcgis.com/d3voDfTFbHOCRwVR/ArcGIS/rest/services/G%C3%A9orisques___Les_feux_de_For%C3%AAt__2024_/FeatureServer/16",
    "2025": "https://services.arcgis.com/d3voDfTFbHOCRwVR/ArcGIS/rest/services/G%C3%A9orisques___Les_feux_de_For%C3%AAt/FeatureServer/14",
}
OCCITANIE = ("09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82")
CHAMPS = ("OBJECTID", "Annee", "Numero", "Departement", "Code_INSEE",
          "Nom_de_la_commune", "Date_de_premiere_alerte", "Nature",
          "Surface_parcourue", "Surface_foret", "Moyens_de_premiere_intervention")
DOSSIER = Path("data/raw/arcgis_bdiff_derive")


def requete(url, params):
    adresse = url + "/query?" + urllib.parse.urlencode({**params, "f": "json"})
    request = urllib.request.Request(adresse, headers={"User-Agent": "HETIC-MD5-feux-de-foret/0.2"})
    with urllib.request.urlopen(request, timeout=75) as response:
        contenu = response.read(12 * 1024 * 1024 + 1)
    if len(contenu) > 12 * 1024 * 1024:
        raise ValueError("Réponse REST trop volumineuse")
    resultat = json.loads(contenu)
    if "error" in resultat:
        raise RuntimeError(str(resultat["error"]))
    return resultat


def date_locale(epoch):
    if epoch is None:
        return "", ""
    utc = datetime.fromtimestamp(int(epoch) / 1000, tz=timezone.utc)
    paris = utc.astimezone(ZoneInfo("Europe/Paris"))
    return utc.isoformat(), paris.isoformat()


def collecter(annee, couche):
    # Le filtrage par code département est contrôlé une seconde fois localement.
    where = "Departement IN (" + ",".join(f"'{d}'" for d in OCCITANIE) + ")"
    ids = requete(couche, {"where": where, "returnIdsOnly": "true"}).get("objectIds") or []
    if len(ids) > 12000:
        raise ValueError("Plus de 12 000 objets : vérifier le filtre géographique")
    ids = sorted(set(ids))
    lignes = []
    for debut in range(0, len(ids), 300):
        paquet = ids[debut:debut + 300]
        response = requete(couche, {
            "objectIds": ",".join(str(i) for i in paquet),
            "outFields": ",".join(CHAMPS), "returnGeometry": "false"
        })
        lignes.extend(f.get("attributes", {}) for f in response.get("features", []))
    if len(lignes) != len(ids):
        raise ValueError(f"Pagination incomplète : {len(lignes)} objets / {len(ids)} identifiants attendus")
    for a in lignes:
        dep = str(a.get("Departement") or "").zfill(2)
        if dep not in OCCITANIE:
            raise ValueError(f"Département hors Occitanie : {dep}")
        if str(a.get("Annee")) != annee:
            raise ValueError(f"Année inattendue : {a.get('Annee')} au lieu de {annee}")
    return lignes, where


def main():
    DOSSIER.mkdir(parents=True, exist_ok=True)
    manifest = []
    erreurs = []
    for annee, url in LAYERS.items():
        try:
            attributs, filtre = collecter(annee, url)
            if not attributs:
                raise ValueError(f"Aucun feu trouvé en {annee} : contrôle de filtre requis")
        except Exception as exc:
            print(f"ÉCHEC contrôlé pour {annee} : {type(exc).__name__}: {exc}", flush=True)
            erreurs.append({"annee": annee, "couche": url, "type": type(exc).__name__, "message": str(exc)[:500]})
            continue
        path = DOSSIER / f"evenements_derive_bdiff_{annee}_occitanie.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(CHAMPS) + ["date_alerte_utc", "date_alerte_paris", "date_jour_paris"])
            writer.writeheader()
            for a in attributs:
                utc, local = date_locale(a.get("Date_de_premiere_alerte"))
                record = {key: a.get(key) for key in CHAMPS}
                record.update({"date_alerte_utc": utc, "date_alerte_paris": local,
                               "date_jour_paris": local[:10] if local else ""})
                writer.writerow(record)
        blob = path.read_bytes()
        manifest.append({
            "annee": annee, "url_couche": url, "url_requete": url + "/query",
            "filtre_departement": filtre, "nb_objets": len(attributs),
            "nom_fichier_local": str(path), "taille_octets": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "collecte_utc": datetime.now(timezone.utc).isoformat(),
            "producteur_initial_declare": "IGNF / Géorisques (BDIFF)",
            "diffuseur_de_la_couche": "Esri France",
            "licence_de_redistribution": "A_VERIFIER_AVANT_PUBLICATION",
            "limite_connue": "Une vingtaine d'enregistrements avec codes communes disparus peuvent manquer à la couche Esri ; périmètre exact à vérifier.",
            "statut": "source_secondaire_non_validee_par_comparaison_aux_exports_BDIFF"
        })
        print(f"{annee} : {len(attributs)} feux, fichier local {path}, empreinte SHA-256 {manifest[-1]['sha256']}")
    (DOSSIER / "manifest-local.json").write_text(
        json.dumps({"sources": manifest, "erreurs": erreurs}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

if __name__ == "__main__":
    main()
