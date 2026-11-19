#!/usr/bin/env python3
"""Récupérer les codes géographiques INSEE 2025 et extraire les communes d'Occitanie.

Conserver les liens, les empreintes du téléchargement complet et le millésime ;
ne jamais écraser les codes 2024 par ceux de 2025 sans table de passage.
"""
import csv
import hashlib
import io
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SOURCE = "https://www.insee.fr/fr/information/8377162"
FILES = {
    "communes": "https://www.insee.fr/fr/statistiques/fichier/8377162/v_commune_2025.csv",
    "departements": "https://www.insee.fr/fr/statistiques/fichier/8377162/v_departement_2025.csv",
}
OUT = Path("datasets/public/insee_cog_2025")
REGION = "76"  # Occitanie
OCC = {"09","11","12","30","31","32","34","46","48","65","66","81","82"}


def lire_csv(url):
    req=urllib.request.Request(url,headers={"User-Agent":"HETIC-feux-occitanie-recherche/0.1"})
    with urllib.request.urlopen(req, timeout=80) as r:
        raw=r.read(9*1024*1024 + 1)
    if not raw or len(raw)>9*1024*1024 or raw[:10].lstrip().lower().startswith(b"<html"):
        raise ValueError("Réponse INSEE incorrecte ou trop volumineuse")
    txt=raw.decode("utf-8-sig")
    header=txt.splitlines()[0] if txt else ""
    separator=";" if header.count(";")>header.count(",") else ","
    rows=list(csv.DictReader(io.StringIO(txt,newline=""),delimiter=separator))
    return raw,rows,separator


def sauvegarder(label,rows,headers):
    target=OUT/("occitanie_"+label+"_2025.csv")
    with target.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({k:row.get(k,"") for k in headers})
    return str(target), hashlib.sha256(target.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=[]
    count_by_dep={}
    for label,url in FILES.items():
        raw,rows,sep=lire_csv(url)
        if label=="communes":
            required={"COM","REG","DEP","TYPECOM"}
            if not required.issubset(rows[0]):
                raise ValueError("Schéma commune INSEE inattendu")
            extracted=[r for r in rows if str(r.get("REG") or "").strip()==REG and str(r.get("TYPECOM") or "").strip()=="COM"]
            headers=["COM","DEP","REG","TYPECOM","LIBELLE","NCC"]
            codes=[r["COM"] for r in extracted]
            if len(set(codes))!=len(codes):
                raise ValueError("Codes communes dupliqués (TYPECOM=COM)")
            count_by_dep={d:sum(1 for row in extracted if row["DEP"]==d) for d in OCC}
            if sum(count_by_dep.values())!=len(extracted):
                raise ValueError("Couverture départementale Occitanie inattendue")
        else:
            if not {"DEP","REG"}.issubset(rows[0]):
                raise ValueError("Schéma départements INSEE inattendu")
            extracted=[r for r in rows if str(r.get("REG") or "").strip()==REG]
            headers=["DEP","REG","LIBELLE","NCC"]
            if {r["DEP"] for r in extracted}!=OCC:
                raise ValueError("La liste des 13 départements d'Occitanie ne correspond pas aux fichiers INSEE")
        chemin,sha_subset=sauvegarder(label,extracted,headers)
        manifest.append({
          "type":label,"millesime":"2025","url_officielle":url,
          "page_source":SOURCE,
          "date_collecte_utc":datetime.now(timezone.utc).isoformat(),
          "octets_source":len(raw),"sha256_source_entiere":hashlib.sha256(raw).hexdigest(),
          "sep_source":sep,"lignes_source":len(rows),
          "filtre":"REG=76 et TYPECOM=COM" if label=="communes" else "REG=76",
          "fichier_subset":chemin,"lignes_subset":len(extracted),
          "sha256_subset":sha_subset,
          "licence_detail_ressource":"a_verifier_sur_les_conditions_INSEE",
          "statut":"referentiel_officiel_2025_collecte_et_filtre"
        })
        print(label,":",len(rows),"lignes au total ;",len(extracted),"lignes pour Occitanie")
    (OUT/"manifest.json").write_text(json.dumps({"sources":manifest,"communes_par_departement":count_by_dep},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUT/"README.md").write_text(
      "# Référentiel officiel INSEE — COG au 1er janvier 2025\n\n"
      "## Origine et périmètre\n\n"
      "Source : [INSEE — COG 2025]("+SOURCE+"). Deux fichiers CSV officiels ont été téléchargés : communes et départements. "
      "Nous avons conservé uniquement les communes en vigueur (TYPECOM=COM) et les départements de la région 76 (Occitanie).\n\n"
      "Les fichiers du sous-ensemble et leurs empreintes SHA-256 sont archivés ici ; les empreintes des fichiers complets figurent dans le manifeste. "
      "Les codes INSEE sont stockés **en texte**, pour préserver les zéros initiaux.\n\n"
      "## Usage Q1 / Q4\n\n"
      "- Jointure candidate avec les feux 2025 par code INSEE, à tester et documenter.\n"
      "- **Attention :** les feux 2024 doivent être rapprochés du millésime 2024 ou d'une table de passage, pas automatiquement de ce fichier 2025.\n"
      "- Le code département 31 désigne la Haute-Garonne, notre territoire central d'analyse.\n"
      "- Ce référentiel ne renseigne **pas la surface forestière** : aucun ratio Q1 n'en découle à lui seul.\n"
      "- Les conditions de licence détaillées doivent être consignées dans la fiche source avant publication hors cadre du projet.\n\n"
      "Détails : [manifest.json](manifest.json).\n",encoding="utf-8")
    print("COMMUNES PAR DÉPARTEMENT :",count_by_dep)

if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        dossier = Path("docs/resultats")
        dossier.mkdir(parents=True, exist_ok=True)
        description = (
            "# Tentative de collecte INSEE COG 2025 — contrôle technique\n\n"
            "**Statut : collecte non aboutie.** Aucun référentiel INSEE n'est validé par cette tentative.\n\n"
            "Source officielle : https://www.insee.fr/fr/information/8377162\n\n"
            "Erreur interceptée : " + type(exc).__name__ + " — " + str(exc)[:400] + "\n\n"
            "À vérifier : réseau du runner, URL de la ressource, schéma CSV, filtrage REG=76.\n"
        )
        (dossier / "diagnostic_insee_v0.md").write_text(description, encoding="utf-8")
        raise
