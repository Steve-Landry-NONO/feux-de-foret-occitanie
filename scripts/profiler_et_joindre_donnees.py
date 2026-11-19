#!/usr/bin/env python3
"""Profilage réel des archives météo et test de compatibilité des feux dérivés BDIFF.

Un raccord par date n'est pas une validation des seuils J+1 / J+2.
Les fichiers incendies ArcGIS restent en local tant que leur redistribution
n'a pas été vérifiée. Standard Python 3.10+, sans données simulées.
"""
import csv
import gzip
import json
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

OCC = {"09","11","12","30","31","32","34","46","48","65","66","81","82"}
RESULT = Path("docs/resultats")
MDF = Path("datasets/public/meteo_des_forets/manifest.json")
FEUX = Path("data/raw/arcgis_bdiff_derive")

def jour(v):
    x=str(v or "").strip()
    if not x: return None
    try: return date.fromisoformat(x[:10]).isoformat()
    except ValueError: pass
    for fmt in ("%d/%m/%Y","%Y%m%d","%d-%m-%Y"):
        try: return datetime.strptime(x[:10],fmt).date().isoformat()
        except ValueError: pass
    return None

def dep(v):
    x=str(v or "").strip().upper()
    return x.zfill(2) if x.isdigit() else x

def meteo():
    manifest=json.loads(MDF.read_text(encoding="utf-8"))
    stats=[]; index={}; graph=defaultdict(Counter)
    for item in manifest["extractions"]:
        annee=item["annee_archive"]
        doubles=invalides=nb=0
        dates=set(); departements=set(); vides=Counter(); niveaux=Counter()
        with gzip.open(item["fichier"],"rt",newline="",encoding="utf-8-sig") as h:
            r=csv.DictReader(h,delimiter=item["separateur_csv"])
            cols=r.fieldnames or []
            if not {"date","num_dep","niveau_j1","niveau_j2"}.issubset(cols):
                raise ValueError("Colonnes météo absentes en "+annee)
            for row in r:
                nb+=1
                d=jour(row.get("date")); p=dep(row.get("num_dep"))
                departements.add(p)
                if not d: invalides+=1
                else:
                    dates.add(d); key=(annee,p,d)
                    if key in index: doubles+=1
                    else: index[key]={"j1":row.get("niveau_j1"),"j2":row.get("niveau_j2")}
                for c in cols:
                    if not str(row.get(c) or "").strip(): vides[c]+=1
                v=str(row.get("niveau_j1") or "").strip() or "(vide)"
                niveaux[v]+=1
                if p=="31": graph[annee][v]+=1
        stats.append({
            "annee":annee,"lignes":nb,"departements":len(departements),
            "departements_occitanie":len(departements & OCC),
            "dates_distinctes":len(dates),"date_min":min(dates) if dates else None,
            "date_max":max(dates) if dates else None,
            "dates_invalides":invalides,"doublons_depart_jour":doubles,
            "champs":cols,"vides":dict(vides),"niveaux_j1":dict(niveaux)
        })
    return stats,index,graph

def incendies():
    etat=[]; jours=set(); nb_feux=Counter()
    for annee in ("2024","2025"):
        p=FEUX/("evenements_derive_bdiff_"+annee+"_occitanie.csv")
        if not p.exists():
            etat.append({"annee":annee,"statut":"non_collecte"}); continue
        total=0; sansdate=0; horszone=0; uniques=set()
        with p.open(encoding="utf-8",newline="") as h:
            for row in csv.DictReader(h):
                total+=1
                code=dep(row.get("Departement"))
                if code not in OCC: horszone+=1; continue
                d=jour(row.get("date_jour_paris"))
                if not d: sansdate+=1; continue
                key=(annee,code,str(row.get("OBJECTID") or ""))
                if key in uniques: continue
                uniques.add(key); jours.add((annee,code,d)); nb_feux[(annee,code,d)]+=1
        etat.append({"annee":annee,"statut":"derive_BDIFF_Esri_non_recoupe_avec_original",
                     "lignes":total,"evenements_retenus":len(uniques),
                     "sans_date":sansdate,"hors_occitanie":horszone})
    return etat,jours,nb_feux

def graphique_svg(gr):
    couleurs=["#3265B8","#2D9F85","#C48A41","#785CAD","#D25F64"]
    lignes=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 350">','<rect width="800" height="350" fill="white"/>',
       '<text x="20" y="32" font-size="18" font-family="sans-serif" fill="#1E293B">Haute-Garonne — codes J1 enregistrés dans les archives</text>',
       '<text x="20" y="53" font-size="12" font-family="sans-serif" fill="#64748B">Répartition descriptive brute ; signification du seuil à valider</text>']
    cats=sorted({v for counts in gr.values() for v in counts})
    for i,annee in enumerate(sorted(gr)):
        y=95+80*i
        total=sum(gr[annee].values())
        lignes.append(f'<text x="20" y="{y+15}" font-size="14" fill="#1E293B">{annee} ({total})</text>')
        x=170
        for j,cat in enumerate(cats):
            w=570*gr[annee][cat]/max(1,total)
            lignes.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="22" fill="{couleurs[j%len(couleurs)]}"/>')
            x+=w
    lignes.append('<text x="20" y="338" font-size="12" fill="#64748B">Ordre des codes : '+", ".join(cats)+'</text></svg>')
    return "\n".join(lignes)+"\n"

def run():
    RESULT.mkdir(parents=True,exist_ok=True)
    ms,mi,gr=meteo()
    es,feu,_=incendies()
    joint=[]
    for annee in ("2024","2025"):
        a={k for k in feu if k[0]==annee}
        b=a & set(mi)
        joint.append({"annee":annee,"jours_avec_feu":len(a),
            "raccord_meme_date":len(b),"sans_correspondance":len(a-b),
            "jours_avec_feu_31":sum(1 for k in a if k[1]=="31"),
            "raccord_31":sum(1 for k in b if k[1]=="31")})
    result={"genere_utc":datetime.now(timezone.utc).isoformat(),
        "meteo":ms,"incendies":es,"raccord_technique_NON_KPI":joint,
        "limites":[
           "La date de référence météo et la validité J+1/J+2 restent à établir.",
           "Les valeurs de jour sans feu ne sont pas garanties si le recensement est incomplet.",
           "ArcGIS est une source Esri dérivée de BDIFF, sans validation par l'export primaire.",
           "Les intervalles d'engagement et les coûts SDIS ne sont pas disponibles ici."]}
    (RESULT/"profilage_sources_v1.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lignes=["# Profilage des sources — constats reproductibles","",
    "**Données mesurées depuis les fichiers ; aucune recommandation opérationnelle n'est encore validée.**","",
    "## Archives Météo des forêts","",
    "| Année | Lignes | Départements | Départements d'Occitanie | Dates | Min | Max | Dates invalides | Doublons clé |",
    "|---|---:|---:|---:|---:|---|---|---:|---:|"]
    for s in ms:
        lignes.append(f"| {s['annee']} | {s['lignes']} | {s['departements']} | {s['departements_occitanie']} | {s['dates_distinctes']} | {s['date_min']} | {s['date_max']} | {s['dates_invalides']} | {s['doublons_depart_jour']} |")
    lignes+=["","Les colonnes, codes J1 et valeurs manquantes sont listés dans le [JSON d'audit](profilage_sources_v1.json).",
        "","![Répartition J1 (31)](danger_j1_haute_garonne.svg)","","## Source incendies dérivée BDIFF / Esri","",
        "| Année | Statut | Lignes | Événements retenus | Dates manquantes |",
        "|---|---|---:|---:|---:|"]
    for e in es:
        lignes.append(f"| {e['annee']} | {e['statut']} | {e.get('lignes','—')} | {e.get('evenements_retenus','—')} | {e.get('sans_date','—')} |")
    lignes+=["","## Jointure exploratoire de même date — non validée pour Q2 et Q3","",
      "| Année | Jours avec feu | Raccord météo même date | Sans raccord | Jours avec feu 31 | Raccord 31 |",
      "|---|---:|---:|---:|---:|---:|"]
    for j in joint:
        lignes.append(f"| {j['annee']} | {j['jours_avec_feu']} | {j['raccord_meme_date']} | {j['sans_correspondance']} | {j['jours_avec_feu_31']} | {j['raccord_31']} |")
    lignes+=["","**Important :** même date n'implique pas même date de validité de la prévision. Aucun ratio de couverture des seuils n'est publié tant que le producteur n'a pas clarifié cette sémantique.",
    "","## Contrôles restant ouverts","",
    "- Maeva : vérifier la concordance avec l'export BDIFF officiel (source secondaire Esri).",
    "- Chantal : relire licences, lacunes et périmètre d'usage.",
    "- Stéphane : vérifier la cardinalité et les doublons de la clé de rapprochement.",
    "- Ludovic : confirmer les dates de validité J1/J2 avant les KPI.",
    "- Steve : tracer les conclusions dans les tickets et la PR.",
    "","Ces noms désignent des relectures **proposées**, pas des validations déjà effectuées.",""]
    (RESULT/"profilage_sources_v1.md").write_text("\n".join(lignes),encoding="utf-8")
    (RESULT/"danger_j1_haute_garonne.svg").write_text(graphique_svg(gr),encoding="utf-8")
    for s in ms: print("MÉTÉO",s["annee"],s["lignes"],s["date_min"],s["date_max"],s["doublons_depart_jour"])
    for e in es: print("INCENDIES",e)
    for j in joint: print("RACCORD",j)

if __name__=="__main__":
    run()
