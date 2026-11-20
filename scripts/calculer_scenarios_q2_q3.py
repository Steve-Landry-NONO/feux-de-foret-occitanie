#!/usr/bin/env python3
"""Scénarios Q2/Q3 : évaluer la Météo des forêts (J+1, J+2) sur BDIFF.

Cette analyse pédagogique n'établit pas les procédures réelles du SDIS.
Les deux échéances sont évaluées sur un MÊME ensemble de jours éligibles.
Les résultats restent conditionnels à l'hypothèse 'date' = date de référence
Météo-France (documentation : 'Reference_time') et aux feux BDIFF type F.
"""
import csv
import gzip
import hashlib
import io
import json
import zipfile
from collections import Counter
from datetime import date, timedelta, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MDF = ROOT / "datasets/public/meteo_des_forets/manifest.json"
BDIFF = ROOT / "datasets/public/bdiff_officiel/manifest.json"
OUT = ROOT / "docs/resultats"
OCC = {"09","11","12","30","31","32","34","46","48","65","66","81","82"}
SEUILS = (2, 3, 4)
ECHEANCES = ("J+1", "J+2")
YEARS = (2024,2025)

def verify_sha(path, sha):
    if hashlib.sha256(path.read_bytes()).hexdigest() != sha:
        raise ValueError("SHA-256 incorrect pour " + str(path))

def charger_previsions():
    meta=json.loads(MDF.read_text(encoding="utf-8"))
    idx={}
    for fiche in meta["extractions"]:
        if int(fiche["annee_archive"]) not in YEARS: continue
        src=ROOT/fiche["fichier"]
        verify_sha(src,fiche["sha256"])
        with gzip.open(src,"rt",newline="",encoding="utf-8-sig") as f:
            for r in csv.DictReader(f,delimiter=fiche["separateur_csv"]):
                depart=str(r["num_dep"]).strip().zfill(2)
                if depart not in OCC: continue
                original=date.fromisoformat(r["date"][:10])
                for offset in (1,2):
                    niveau=int(r["niveau_j"+str(offset)])
                    if niveau not in (1,2,3,4): raise ValueError("Danger hors 1..4")
                    valid=(original+timedelta(days=offset)).isoformat()
                    # Le découpage annuel est fixé par la date de validité.
                    if int(valid[:4]) not in YEARS: continue
                    k=(depart,valid,"J+"+str(offset))
                    if k in idx: raise ValueError("Prévision dupliquée : "+str(k))
                    idx[k]=niveau
    return idx

def charger_evenements():
    meta=json.loads(BDIFF.read_text(encoding="utf-8"))
    docs={int(x["annee"]):x for x in meta["extractions"]}
    events=Counter()
    for year in YEARS:
        ref=docs[year];src=BDIFF.parent/ref["fichier"]
        verify_sha(src,ref["sha256"])
        with zipfile.ZipFile(src) as z:
            lignes=z.read("Incendies.csv").decode("utf-8-sig").splitlines()
        if "OCCITANIE" not in lignes[1] or "Type de feu : F" not in lignes[1]:
            raise ValueError("Filtres BDIFF non reconnus")
        if not lignes[2].startswith("Année;Numéro;Département;"):
            raise ValueError("En-tête CSV inconnu")
        n=0;unique=set()
        for r in csv.DictReader(io.StringIO("\n".join(lignes[2:])),delimiter=";"):
            n+=1
            if int(r["Année"])!=year: raise ValueError("Année BDIFF erronée")
            dep=str(r["Département"]).strip().zfill(2)
            if dep not in OCC: raise ValueError("Département hors Occitanie")
            d=date.fromisoformat(r["Date de première alerte"][:10]).isoformat()
            event_id=(year,str(r["Numéro"]))
            if event_id in unique: raise ValueError("Identifiant BDIFF dupliqué")
            unique.add(event_id)
            events[(dep,d)]+=1
        if n!=ref["controle"]["lignes"]:
            raise ValueError("Nombre BDIFF ne correspond pas au manifeste")
    return events

def evaluer(index, events):
    # Comparaison juste : ne retenir QUE les jours où J+1 ET J+2 existent.
    days=sorted({(dep,jour) for dep,jour,e in index if e=="J+1"
                 and (dep,jour,"J+2") in index and int(jour[:4]) in YEARS})
    rows=[]
    for dep,day in days:
        events_n=events.get((dep,day),0)
        rows.append({"annee":int(day[:4]),"departement":dep,"jour":day,
                     "nb_feux_observes_type_f":events_n,
                     "jour_avec_feu_observe":int(events_n>0),
                     "danger_j1":index[(dep,day,"J+1")],
                     "danger_j2":index[(dep,day,"J+2")]})
    # Tous les seuils et horizons utilisent ce dénominateur commun.
    if not rows: raise ValueError("Aucun jour comparable J+1/J+2")
    return rows

def indicateurs(rows, annee, territoire, horizon, seuil):
    if territoire=="Occitanie": subset=[r for r in rows if r["annee"]==annee]
    else: subset=[r for r in rows if r["annee"]==annee and r["departement"]==territoire]
    n=len(subset)
    feu=sum(r["jour_avec_feu_observe"] for r in subset)
    raw="danger_j1" if horizon=="J+1" else "danger_j2"
    actives=[r for r in subset if r[raw]>=seuil]
    surveillance=len(actives)
    captes=sum(r["jour_avec_feu_observe"] for r in actives)
    rates=lambda a,b: round(100*a/b,2) if b else None
    return {"annee":annee,"territoire":territoire,"horizon":horizon,
            "seuil":seuil,"jours_eligibles":n,"jours_avec_feu_observe":feu,
            "jours_surveillance":surveillance,"jours_feu_couverts":captes,
            "jours_feu_non_couverts":feu-captes,
            "jours_surveillance_sans_feu_observe":surveillance-captes,
            "couverture_feu_pct":rates(captes,feu),
            "mobilisation_pct":rates(surveillance,n),
            "feux_observes_type_f":sum(r["nb_feux_observes_type_f"] for r in subset),
            "unite_cout":"journee-departement de surveillance (proxy non monetaire)"}

def ecrire_csv(path, rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)

def produire():
    idx=charger_previsions()
    events=charger_evenements()
    comparable=evaluer(idx,events)
    result=[]
    for year in YEARS:
        for territory in ["Occitanie"]+sorted(OCC):
            for horizon in ECHEANCES:
                for t in SEUILS:
                    result.append(indicateurs(comparable,year,territory,horizon,t))
    OUT.mkdir(parents=True,exist_ok=True)
    ecrire_csv(OUT/"kpi_scenarios_q2_q3.csv",result)
    # Restreindre les détails aux jours d'incendies et aux journées du 31.
    # Le CSV complet est dérivable, sans déposer une matrice journalière nationale.
    ecrire_csv(OUT/"jours_feu_et_31.csv",
      [x for x in comparable if x["jour_avec_feu_observe"] or x["departement"]=="31"])
    meta={"date_execution_utc":datetime.now(timezone.utc).isoformat(),
          "perimetre":"Occitanie, jours communs J+1/J+2 par département sur saisons 2024–2025",
          "nombre_jours_departement_eligibles":len(comparable),
          "annees":YEARS,"seuils":SEUILS,"horizons":ECHEANCES,
          "regle_date":"date archive supposée date de référence, J+1= date +1, J+2= date +2",
          "type_feu_bdiff":"F (tel que précisé dans les ZIP officiels)",
          "previsions_mdf":"danger départemental pour sensibilisation grand public",
          "denominateur":"jours départementaux où J+1 ET J+2 sont disponibles (intersection identique)",
          "jour_sans_feu":"aucun feu type F recensé par BDIFF dans l'export, pas une certitude d'absence d'incendie",
          "limites":["Correspondance du champ 'date' et 'Reference_time' non corroborée formellement",
                    "Certificat HTTPS non validé sur le runner lors de l'acquisition BDIFF",
                    "Échantillon du 31 très faible (1 événement 2024 et 4 en 2025 sur toute l'année)",
                    "Pas de mesure de coût monétaire ni de politique SDIS réelle",
                    "Danger départemental non pertinent pour comparer directement des communes",
                    "Les seuils ne prouvent pas de prévention causale"],
          "fichiers":[ "kpi_scenarios_q2_q3.csv","jours_feu_et_31.csv"]}
    (OUT/"kpi_scenarios_q2_q3_manifest.json").write_text(
      json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    def block(year,territory):
        subset=[r for r in result if r["annee"]==year and r["territoire"]==territory]
        resultlines=["| Échéance | Seuil | Jours éligibles | Jours avec feu | Jours de surveillance | Jours avec feu couverts | Couverture | Jours sans feu observé mobilisés |",
                     "|---|---:|---:|---:|---:|---:|---:|---:|"]
        for v in subset:
            ratio="n.d." if v["couverture_feu_pct"] is None else str(v["couverture_feu_pct"])+" %"
            resultlines.append(f"| {v['horizon']} | ≥ {v['seuil']} | {v['jours_eligibles']} | {v['jours_avec_feu_observe']} | {v['jours_surveillance']} | {v['jours_feu_couverts']} | {ratio} | {v['jours_surveillance_sans_feu_observe']} |")
        return resultlines
    report=["# Scénarios Q2–Q3 : seuils Météo des forêts et journées de surveillance",
      "","**Exploration pédagogique conditionnelle — pas une recommandation officielle au SDIS 31.**",
      "",
      "## Hypothèses et définition des KPI",
      "",
      "- Unité : **département × jour de validité**. Les lignes BDIFF sont agrégées en jours avec au moins un feu de type F.",
      "- Pour une comparaison honnête de J+1 et J+2, ne conserver que les jours où **les deux échéances existent** ; ce dénominateur est identique pour les seuils 2, 3 et 4.",
      "- Une journée de surveillance est comptée quand le niveau prévu atteint le seuil.",
      "- Couverture = journées avec feu recensé et surveillance / journées avec feu recensé parmi les jours éligibles.",
      "- Mobilisation sans feu observé = journées de surveillance - journées avec feu couvertes. Ce n'est pas une mesure d'inefficacité.",
      "- Coût de surveillance : **proxy en journées-département**, sans inventer de dépense monétaire.",
      "",
      "## Haute-Garonne (31) — cœur de la commande",
      "",
      "### Année 2024", *block(2024,"31"),
      "","### Année 2025",*block(2025,"31"),
      "","## Occitanie — comparaison régionale",
      "","### Année 2024",*block(2024,"Occitanie"),
      "","### Année 2025",*block(2025,"Occitanie"),
      "",
      "## Autres livrables",
      "",
      "- [Table complète des indicateurs par département](kpi_scenarios_q2_q3.csv), années et échéances (168 lignes).",
      "- [Journées avec feu ou situées dans le 31](jours_feu_et_31.csv), utiles pour contrôler les observations.",
      "- [Manifeste des hypothèses et restrictions](kpi_scenarios_q2_q3_manifest.json).",
      "",
      "## Validation nécessaire avant toute conclusion opérationnelle",
      "",
      "1. Le producteur documente J+1 et J+2, mais l'équivalence entre le champ de fichier 'date' et 'Reference_time' n'a pas été formellement corroborée.",
      "2. Contrôler les ZIP BDIFF avec un téléchargement indépendant vérifiant les certificats HTTPS.",
      "3. Faire valider le périmètre, les formules et les exclusions par les membres du groupe.",
      "4. La Météo des forêts est un **produit de sensibilisation du public** et non la doctrine opérationnelle de surveillance SDIS.",
      "5. Les faibles effectifs du 31 impliquent de présenter les taux avec leur dénominateur, plutôt que d'y voir une précision statistique.",
      ""]
    (OUT/"kpi_scenarios_q2_q3.md").write_text("\n".join(report),encoding="utf-8")
    print("Lignes de cohorte :",len(comparable),"indicateurs :",len(result))
    for row in result:
        if row["territoire"]=="31":print(row)

if __name__=="__main__":
    produire()
