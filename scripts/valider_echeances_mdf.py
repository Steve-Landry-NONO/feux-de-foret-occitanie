#!/usr/bin/env python3
"""Météo des forêts : transformer J+1/J+2 en dates de validité et tester BDIFF.

Référence Météo-France : publication à 17 h, J+1 lendemain, J+2 surlendemain.
Le champ "date" de nos CSV est interprété comme la date de référence :
la documentation nomme ce champ "Reference_time", correspondance à confirmer.
"""
import csv
import gzip
import io
import json
import zipfile
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MDF = ROOT / "datasets/public/meteo_des_forets/manifest.json"
BDIFF = ROOT / "datasets/public/bdiff_officiel"
OUT = ROOT / "docs/resultats"
OCC = {"09","11","12","30","31","32","34","46","48","65","66","81","82"}

def previsions_ligne(ligne):
    reference = date.fromisoformat(str(ligne["date"])[:10])
    dep = str(ligne["num_dep"]).strip().zfill(2)
    results = []
    for echeance in (1, 2):
        niveau = str(ligne[f"niveau_j{echeance}"]).strip()
        if niveau not in {"1","2","3","4"}:
            raise ValueError("Niveau invalide : " + repr(ligne))
        results.append({"departement":dep, "date_reference":reference.isoformat(),
                        "date_validite":(reference+timedelta(days=echeance)).isoformat(),
                        "echeance":f"J+{echeance}", "niveau":niveau})
    return results

def lire_meteo():
    archive = json.loads(MDF.read_text(encoding="utf-8"))
    index = {}
    controle = []
    for meta in archive["extractions"]:
        n=0
        with gzip.open(ROOT / meta["fichier"],"rt",newline="",encoding="utf-8-sig") as h:
            for row in csv.DictReader(h,delimiter=meta["separateur_csv"]):
                n+=1
                for v in previsions_ligne(row):
                    key=(v["departement"],v["date_validite"],v["echeance"])
                    if key in index:
                        raise ValueError("Doublon département/date valide/échéance : "+str(key))
                    index[key]=v["niveau"]
        controle.append({"annee":meta["annee_archive"],"lignes_source":n,"previsions_generees":2*n,
             "dates_ref_min":None,"point_verifie":"Unicité des clés, niveaux 1..4 et décalage calendaire"})
    return index,controle

def lire_bdiff():
    jours = {}
    for annee in (2024,2025):
        with zipfile.ZipFile(BDIFF / f"bdiff_occitanie_{annee}.zip") as z:
            lines = z.read("Incendies.csv").decode("utf-8-sig").splitlines()
        if len(lines)<3 or not lines[2].startswith("Année;Numéro;Département;"):
            raise ValueError("Schéma officiel BDIFF non reconnu")
        pairs=set()
        for row in csv.DictReader(io.StringIO("\n".join(lines[2:])),delimiter=";"):
            if str(row["Année"])!=str(annee):
                raise ValueError("Année BDIFF incohérente")
            dep=str(row["Département"]).strip().zfill(2)
            if dep not in OCC: raise ValueError("Incendie hors Occitanie : "+dep)
            jour=str(row["Date de première alerte"])[:10]
            date.fromisoformat(jour)
            pairs.add((dep,jour))
        jours[annee]=pairs
    return jours

def auditer():
    index,controles=lire_meteo()
    feux=lire_bdiff()
    sorties=[]
    for annee in (2024,2025):
        for echeance in ("J+1","J+2"):
            source=feux[annee]
            raccordes={(dep,jour) for dep,jour in source if (dep,jour,echeance) in index}
            classes=Counter(index[(dep,jour,echeance)] for dep,jour in raccordes)
            sorties.append({"annee":annee,"echeance":echeance,
                 "jours_departement_avec_feu":len(source),
                 "jours_avec_prevision_valide":len(raccordes),
                 "jours_sans_prevision_valide":len(source-raccordes),
                 "jours_31_avec_feu":sum(1 for dep,j in source if dep=="31"),
                 "jours_31_raccordes":sum(1 for dep,j in raccordes if dep=="31"),
                 "niveaux_sur_jours_raccordes":dict(classes)})
    doc="https://confluence-meteofrance.atlassian.net/wiki/spaces/OpenDataMeteoFrance/pages/874741792/Donn%2Bes%2Bexpertis%Bes"
    obj={"execution_utc":datetime.now(timezone.utc).isoformat(),
         "regle_officielle":"Diffusion à 17 h ; J+1 lendemain, J+2 surlendemain ; danger départemental de 1 à 4",
         "point_non_formellement_confirme":"Le champ archive date correspond au Reference_time documenté",
         "source_metier":doc,"archives":controles,"raccords":sorties,
         "reserves":["Pas de KPI final sans confirmation du libellé date/Reference_time",
                     "Météo des forêts est un produit de sensibilisation, non outil opérationnel SDIS",
                     "Le transfert HTTPS des ZIP BDIFF requiert un contrôle indépendant",
                     "Comparer uniquement les jours couverts par les archives météo"]}
    OUT.mkdir(exist_ok=True,parents=True)
    (OUT/"validation_j1_j2_v1.json").write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# Validation documentaire et test du décalage J+1 / J+2","",
       "**Règle confirmée par Météo-France :** à 17 h un jour J, publication du danger de J+1 (lendemain) et J+2 (surlendemain).",
       "",
       "**Différence de libellé restante :** le producteur décrit Reference_time comme date/heure de production ; les archives récupérées ont une colonne date. L'alignement est plausible, mais doit être corroboré explicitement.",
       "",
       "## Jointures exploratoires sur date de validité recalculée","",
       "| Année | Échéance | Jours départementaux avec feu | Avec prévision | Sans prévision | Jours feu Haute-Garonne | Raccordés Haute-Garonne |",
       "|---|---|---:|---:|---:|---:|---:|"]
    for r in sorties:
        lines.append(f"| {r['annee']} | {r['echeance']} | {r['jours_departement_avec_feu']} | {r['jours_avec_prevision_valide']} | {r['jours_sans_prevision_valide']} | {r['jours_31_avec_feu']} | {r['jours_31_raccordes']} |")
    lines+=["","**Ces nombres sont des contrôles de raccord, pas encore des résultats Q2–Q3 validés.**",
            "",
            "Le scénario métier le plus cohérent est la décision à J-1 après la publication de 17 h, basée sur le niveau_j1 de la veille. Une variante de planification à J-2 peut utiliser niveau_j2 deux jours avant l'intervention. Il faut garder ces variantes distinctes.",
            "",
            "**Attention :** ce produit Météo-France vise la sensibilisation grand public, pas le pilotage opérationnel des moyens des SDIS.",
            "",
            "Références : "+doc+" ; https://meteofrance.com/actualites/la-meteo-des-forets-sinformer-sur-le-danger-de-feux",
            "","## Contrôles encore ouverts","",
            "- Confirmation du champ date / Reference_time auprès du producteur ou dans le descriptif de l'archive.",
            "- Comparaison d'un jour d'archive à une carte datée de Météo-France.",
            "- Validation du périmètre et des scénarios avec le groupe.",
            "- Contrôle indépendant de la provenance TLS des archives BDIFF.",""]
    (OUT/"validation_j1_j2_v1.md").write_text("\n".join(lines),encoding="utf-8")
    for r in sorties:print(r)

if __name__=="__main__":
    auditer()
