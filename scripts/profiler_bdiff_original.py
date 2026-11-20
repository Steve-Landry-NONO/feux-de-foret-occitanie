#!/usr/bin/env python3
"""Profilage des ZIP originaux BDIFF Occitanie et jointure exploratoire MdF.

Ne calcule aucun indicateur de seuil J+1/J+2 sans validation des dates de validité.
Les CSV BDIFF ont deux lignes de préambule avant les en-têtes métier.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import csv, io, json, zipfile
from profiler_et_joindre_donnees import meteo, jour, dep, OCC

ROOT=Path("datasets/public/bdiff_officiel")
OUT=Path("docs/resultats")
ANNEES=("2024","2025")

def charger(annee):
    path=ROOT / f"bdiff_occitanie_{annee}.zip"
    with zipfile.ZipFile(path) as z:
        text=z.read("Incendies.csv").decode("utf-8-sig")
    lignes=text.splitlines()
    if not lignes[2].startswith("Année;Numéro;Département;"):
        raise ValueError(f"En-tête BDIFF modifié pour {annee}")
    if "OCCITANIE" not in lignes[1] or f"{annee}-01-01" not in lignes[1]:
        raise ValueError("Le préambule ne correspond pas à la zone/année")
    return list(csv.DictReader(io.StringIO("\n".join(lignes[2:])),delimiter=";"))

def profiler():
    OUT.mkdir(parents=True,exist_ok=True)
    meteo_stats, meteo_index, _=meteo()
    profils=[]; raccords=[]; jours_feu={}
    for annee in ANNEES:
        rows=charger(annee)
        keys=set(); doublons=0; invalides=0; deps=Counter(); uniques_par_dept=Counter()
        jours=set(); plages=[]; champs=rows[0].keys() if rows else []
        champs_requis={"Année","Numéro","Département","Code INSEE","Date de première alerte"}
        if not champs_requis.issubset(champs):
            raise ValueError("Colonnes officielles manquantes")
        for r in rows:
            d=dep(r.get("Département"))
            if d not in OCC:raise ValueError("Département hors Occitanie : "+d)
            if str(r["Année"])!=annee:raise ValueError("Année hors période")
            k=(annee,str(r.get("Numéro") or ""))
            if k in keys:doublons+=1
            keys.add(k)
            date_civile=jour(r.get("Date de première alerte"))
            if not date_civile:invalides+=1;continue
            if not date_civile.startswith(annee):raise ValueError("Date hors année")
            jours.add((annee,d,date_civile))
            plages.append(date_civile)
            deps[d]+=1;uniques_par_dept[d]+=1
        jours_feu[annee]=jours
        commun=jours & set(meteo_index)
        hors=jours-set(meteo_index)
        profils.append({"annee":annee,"nb_lignes":len(rows),
            "incendies_31":deps.get("31",0),
            "departements_avec_incendie":len(deps),
            "feux_par_departement":dict(sorted(deps.items())),
            "date_min":min(plages) if plages else None,"date_max":max(plages) if plages else None,
            "dates_invalides":invalides,"doublons_numero":doublons,
            "colonnes":list(champs)})
        raccords.append({"annee":annee,
            "jours_departement_avec_feu":len(jours),
            "jours_departement_avec_meteo_meme_date":len(commun),
            "jours_departement_sans_meteo_meme_date":len(hors),
            "jours_31_avec_feu":sum(1 for k in jours if k[1]=="31"),
            "jours_31_avec_meteo_meme_date":sum(1 for k in commun if k[1]=="31"),
            "jours_departement_avec_feu_pendant_saison_meteo":sum(1 for k in jours if k[1] in OCC and k[2] >= (annee+"-06-03") and k[2] <= (annee+"-09-30")),
        })
    audit={"genere_utc":datetime.now(timezone.utc).isoformat(),
        "provenance":"BDIFF ministère Agriculture, ZIP issus du portail officiel, transport TLS non authentifié côté runner (à confirmer indépendamment)",
        "rapport_validation_transport":"datasets/public/bdiff_officiel/manifest.json",
        "incendies":profils,"raccords_techniques_NON_KPI":raccords,
        "limites":["Le portail exporte ici uniquement 'Type de feu : F'.",
         "La date météo et les échéances J1/J2 nécessitent une validation documentaire.",
         "Une date sans événement dans les données n'est pas nécessairement une journée sans feu garanti.",
         "Un rapprochement sur la même date brute ne constitue pas un taux de couverture du danger.",
         "Le transport TLS non vérifié sur le runner doit faire l'objet d'un contrôle indépendant avant certification de provenance."]}
    (OUT/"profilage_bdiff_officiel_v1.json").write_text(json.dumps(audit,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    md=["# Incendies BDIFF Occitanie — profilage des exports 2024 et 2025",
        "",
        "**Source : ZIP du portail officiel BDIFF, filtrés sur Occitanie et « Type de feu : F ».**",
        "**Réserve :** le certificat du portail n'a pas été validé par le runner ; l'authenticité du transport reste à corroborer.",
        "",
        "## 1. Qualité des événements extraits","",
        "| Année | Événements | Dont Haute-Garonne (31) | Départements avec feux | Première alerte | Dernière alerte | Doublons n° BDIFF |",
        "|---|---:|---:|---:|---|---|---:|"]
    for p in profils:
        md.append(f"| {p['annee']} | {p['nb_lignes']} | {p['incendies_31']} | {p['departements_avec_incendie']} | {p['date_min']} | {p['date_max']} | {p['doublons_numero']} |")
    md+=["","## 2. Jointure exploratoire avec les archives météo (département × date brute)","",
       "| Année | Jours départementaux avec feu | Correspondance météo même date | Sans correspondance | Jours avec feu (31) | Correspondance météo (31) |",
       "|---|---:|---:|---:|---:|---:|"]
    for x in raccords:
        md.append(f"| {x['annee']} | {x['jours_departement_avec_feu']} | {x['jours_departement_avec_meteo_meme_date']} | {x['jours_departement_sans_meteo_meme_date']} | {x['jours_31_avec_feu']} | {x['jours_31_avec_meteo_meme_date']} |")
    md+=["","**Ne pas interpréter ces correspondances comme une sensibilité d'un seuil de danger :** nous n'avons pas fixé la date de validité des prévisions J+1/J+2. Les archives météo n'existent que sur une partie de l'année ; les feux hors saison ne représentent pas une erreur de jointure.",
          "","## 3. Traçabilité et limites","",
          "- [Manifestes ZIP, SHA-256, filtres et état TLS](../../datasets/public/bdiff_officiel/manifest.json).",
          "- [Rapport JSON détaillé](profilage_bdiff_officiel_v1.json) : colonnes, nombres par département, réserves.",
          "- Les originaux contiennent un CSV, un PDF de mentions légales et un PDF de définitions ; ne pas modifier les ZIP.",
          "- Pour Q1, les surfaces forestières IGN restent nécessaires et les communes devront être alignées aux millésimes INSEE.",
          "- Pour Q2/Q3, confirmer la sémantique J1/J2 et l'exhaustivité de chaque campagne, avant de calculer les KPI.",
          "","**Relectures à obtenir :** Maeva (BDIFF et licences), Chantal (qualité), Stéphane (pipeline), Ludovic (KPI).",""]
    (OUT/"profilage_bdiff_officiel_v1.md").write_text("\n".join(md),encoding="utf-8")
    print("\n".join(md[:16]))

if __name__=="__main__":
    profiler()
