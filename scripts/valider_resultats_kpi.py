#!/usr/bin/env python3
"""Validation post-calcul des invariants des indicateurs Q2–Q3."""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"docs/resultats/kpi_scenarios_q2_q3.csv"
MANIFEST=ROOT/"docs/resultats/kpi_scenarios_q2_q3_manifest.json"
REPORT=ROOT/"docs/resultats/audit_kpi_q2_q3.md"

def valider():
    with PATH.open(encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    by=defaultdict(dict)
    for r in rows:
        key=(r["annee"],r["territoire"],r["horizon"])
        seuil=int(r["seuil"])
        if seuil in by[key]:raise ValueError("Seuil dupliqué : "+str((key,seuil)))
        by[key][seuil]=r
        n=int(r["jours_eligibles"])
        feu=int(r["jours_avec_feu_observe"])
        surveilles=int(r["jours_surveillance"])
        captes=int(r["jours_feu_couverts"])
        rates=[int(r["jours_feu_non_couverts"]),int(r["jours_surveillance_sans_feu_observe"])]
        if not 0<=captes<=min(feu,surveilles)<=n:
            raise ValueError("Comptage incohérent pour "+str((key,seuil)))
        if rates!=[feu-captes,surveilles-captes]:
            raise ValueError("Conservation des volumes non respectée")
        if not feu and r["couverture_feu_pct"] not in ("",None):
            raise ValueError("Un taux ne doit pas être défini en absence de journées avec feu")
        if feu and abs(float(r["couverture_feu_pct"])-100*captes/feu)>0.011:
            raise ValueError("Taux de couverture incohérent")
        if n and abs(float(r["mobilisation_pct"])-100*surveilles/n)>0.011:
            raise ValueError("Taux de mobilisation incohérent")
    for key, scenarios in by.items():
        if set(scenarios)!={2,3,4}:raise ValueError("Seuils incomplets : "+str(key))
        for metric in ("jours_surveillance","jours_feu_couverts"):
            a=[int(scenarios[i][metric]) for i in (2,3,4)]
            if not a[0]>=a[1]>=a[2]:
                raise ValueError("Monotonie du seuil brisée : "+str((key,metric,a)))
        counterpart=(key[0],key[1],"J+2" if key[2]=="J+1" else "J+1")
        if counterpart not in by:raise ValueError("Échéance manquante : "+str(key))
        for field in ("jours_eligibles","jours_avec_feu_observe"):
            if scenarios[2][field]!=by[counterpart][2][field]:
                raise ValueError("Cohorte non comparable : "+str((key,field)))
    meta=json.loads(MANIFEST.read_text(encoding="utf-8"))
    if len(rows)!=2*14*2*3 or len(by)!=2*14*2:
        raise ValueError("Il manque des années/départements/échéances/seuils")
    assert meta["nombre_jours_departement_eligibles"]==sum(
        int(v[2]["jours_eligibles"]) for k,v in by.items() if k[1]=="Occitanie" and k[2]=="J+1"
    )
    lines=["# Audit d'invariants des indicateurs Q2–Q3","",
      "**Statut :** contrôles automatisés exécutés après les calculs sur les 168 combinaisons, avec succès.",
      "",
      "- Conservation : feux couverts + feux non couverts = jours avec feu éligibles.",
      "- Mobilisation : surveillance avec feu + sans feu observé = journées surveillées.",
      "- Aucune couverture définie lorsque le nombre de journées avec feu est nul.",
      "- Plus le seuil augmente, moins il peut y avoir de jours surveillés ou de jours avec feu couverts.",
      "- Cohorte strictement identique pour J+1 et J+2, dans chaque territoire et chaque année.",
      "- Une table de 168 indicateurs : 2 années × 14 territoires (13 départements + Occitanie) × 2 horizons × 3 seuils.",
      "",
      "**Cet audit garantit la cohérence arithmétique, pas l'authenticité TLS, ni la sémantique du champ date, ni une interprétation causale des résultats.**",""]
    REPORT.write_text("\n".join(lines),encoding="utf-8")
    print("PASS : 168 KPI, seuils monotones et dénominateurs cohérents")

if __name__=="__main__":
    valider()
