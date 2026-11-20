#!/usr/bin/env python3
"""Rechercher et télécharger le ZIP officiel BDIFF avec les filtres du site.

Tentative de collecte ; aucune donnée publiée tant que les contrôles
département/année et licence ne sont pas passés.
"""
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import build_opener, HTTPCookieProcessor, HTTPSHandler, Request
from http.cookiejar import CookieJar
import ssl, json, re, csv, io, hashlib, zipfile, unicodedata
from html import unescape
from datetime import datetime, timezone

BASE="https://bdiff.agriculture.gouv.fr"
REPORT=Path("docs/resultats/diagnostic_collecte_bdiff.md")
OUT=Path("datasets/public/bdiff_officiel")
OCC={"09","11","12","30","31","32","34","46","48","65","66","81","82"}
MAX=20*1024*1024

def normaliser(x):
    return "".join(c for c in unicodedata.normalize("NFKD",str(x)) if not unicodedata.combining(c)).lower().strip()

def ouvrir(opener,url):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; HETIC-feux-Occitanie/1.0; educational research)","Accept":"text/html,application/zip,*/*"})
    with opener.open(req,timeout=85) as r:
        data=r.read(MAX+1)
        return r.url,r.status,r.headers.get("Content-Type",""),data

def selection_region(html):
    # Le champ 'if[ra]' est présent dans le formulaire officiel.
    m=re.search(r'<select\b[^>]*id=["\']if_ra["\'][^>]*>(.*?)</select>',html,re.I|re.S)
    if not m:
        raise RuntimeError("Select région if_ra non trouvé")
    for opt in re.finditer(r'<option\b([^>]*)>(.*?)</option>',m.group(1),re.I|re.S):
        attrs=opt.group(1)
        val=re.search(r'\bvalue=["\']([^"\']+)["\']',attrs)
        texte=normaliser(unescape(re.sub(r'<[^>]+>',"",opt.group(2))))
        if "occitanie" in texte and val:
            return val.group(1)
    raise RuntimeError("Option Occitanie introuvable dans le formulaire")

def inspect_zip(data,annee):
    if not zipfile.is_zipfile(io.BytesIO(data)):
        raise ValueError("Réponse non ZIP : "+repr(data[:140]))
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=z.namelist()
        csvs=[n for n in names if n.lower().endswith(".csv")]
        pdfs=[n for n in names if n.lower().endswith(".pdf")]
        if len(csvs)!=1 or len(pdfs)<2:
            raise ValueError("ZIP incomplet : "+str(names))
        raw=z.read(csvs[0])
        txt=raw.decode("utf-8-sig")
        lines=txt.splitlines()
        if len(lines)<4 or "Critères de sélection" not in lines[1] or "OCCITANIE" not in lines[1]:
            raise ValueError("Préambule BDIFF / Région inattendu")
        if "Type de feu : F" not in lines[1]:
            raise ValueError("Type de feu inattendu dans l'export")
        match=re.search(r"Nombre d.incendies suivant les critères de sélection :\s*(\d+)",lines[0])
        if not match:
            raise ValueError("Nombre de feux absent du préambule")
        header=next((i for i,line in enumerate(lines[:8]) if line.startswith("Année;Numéro;Département;")),None)
        if header is None:
            raise ValueError("Entête CSV métier manquante")
        reader=csv.DictReader(io.StringIO("\n".join(lines[header:])),delimiter=";")
        cols=reader.fieldnames or []
        required={"Année","Numéro","Département","Code INSEE","Date de première alerte"}
        if not required.issubset(cols):raise ValueError("Schéma inattendu : "+repr(cols))
        rows=list(reader)
        if len(rows)!=int(match.group(1)):
            raise ValueError(f"Nombre enregistrements != bandeau ({len(rows)} vs {match.group(1)})")
        deps=sorted({str(row["Département"]).strip().upper().zfill(2) for row in rows})
        years=sorted({str(row["Année"]) for row in rows})
        if years != [str(annee)]:raise ValueError("Année hors filtre : "+repr(years))
        if not set(deps).issubset(OCC):raise ValueError("Département hors Occitanie : "+repr(deps))
        invalid_dates=sum(1 for row in rows if not str(row["Date de première alerte"]).startswith(str(annee)+"-"))
        if invalid_dates:raise ValueError(f"Dates alerte hors année : {invalid_dates}")
        if any(not z.read(name).startswith(b"%PDF") for name in pdfs):
            raise ValueError("Un PDF d'annexe ne possède pas de signature PDF")
        return {"fichiers":names,"csv":csvs[0],"pdfs":pdfs,
                "criteres_export":lines[1],"champs":cols,"separateur":";",
                "lignes":len(rows),"annees":years,"departements_presents":deps,
                "dates_alerte_hors_annee":invalid_dates,"validation_structure":"OK"}



def main():
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    journal=["# Tentative de collecte officielle BDIFF","",
             "Source : https://bdiff.agriculture.gouv.fr/incendies ; méthode : formulaire public GET puis lien /incendies/zip.",
             "**Attention :** l'instance GitHub Actions rencontre une anomalie de chaîne TLS sur le site. La lecture utilise ici un contexte sans vérification de certificat ; **le transport n'est donc pas authentifié** et les fichiers restent en quarantaine tant qu'un contrôle indépendant n'est pas réalisé.",
             ""]
    cert=ssl._create_unverified_context()
    opener=build_opener(HTTPCookieProcessor(CookieJar()),HTTPSHandler(context=cert))
    collected=[]
    try:
        url,status,typ,b=ouvrir(opener,BASE+"/incendies")
        region=selection_region(b.decode("utf-8",errors="replace"))
        journal.append(f"- Champ Région Occitanie détecté : valeur HTML {region!r}")
        for annee in (2024,2025):
            params={"if[dateAlerteDeb][date]":f"01/01/{annee}",
                    "if[dateAlerteDeb][time][hour]":"0",
                    "if[dateAlerteDeb][time][minute]":"0",
                    "if[dateAlerteFin][date]":f"31/12/{annee}",
                    "if[dateAlerteFin][time][hour]":"23",
                    "if[dateAlerteFin][time][minute]":"59",
                    "if[ra]":region,"if[submit]":""}
            url,status,typ,page=ouvrir(opener,BASE+"/incendies?"+urlencode(params))
            html=page.decode("utf-8",errors="replace")
            match=re.search(r'(\d[\d \xa0]*)\s+incendies',html,re.I)
            journal.append(f"## {annee}\n\n- Recherche HTTP {status}, URL finale {url}\n- Nombre indiqué sur page : {match.group(1) if match else 'non trouvé'}\n")
            if "/incendies/zip" not in html:raise RuntimeError("Aucun lien /incendies/zip dans la réponse filtrée")
            zurl,zstatus,ztype,zipped=ouvrir(opener,BASE+"/incendies/zip")
            journal.append(f"- ZIP : HTTP {zstatus}, content-type {ztype}, taille {len(zipped)} octets")
            metadata=inspect_zip(zipped,annee)
            journal.append("- Contenu observé : \n\n~~~json\n"+json.dumps(metadata,ensure_ascii=False,indent=2)+"\n~~~\n")
            filename=f"bdiff_occitanie_{annee}.zip"
            (OUT/filename).write_bytes(zipped)
            sha=hashlib.sha256(zipped).hexdigest()
            collected.append({"annee":annee,"fichier":filename,"sha256":sha,
                              "url_recherche":url,"url_export":zurl,"octets":len(zipped),
                              "controle":metadata,"date_collecte_utc":datetime.now(timezone.utc).isoformat(),
                              "tls_certificat_verifie":False,"statut":"export_officiel_structure_verifiee_transport_tls_a_confirmer"})
            journal.append(f"- SHA-256 : {sha}")
        (OUT/"manifest.json").write_text(json.dumps({"source":"Portail BDIFF / ministère de l’Agriculture","transfert_tls_verifie":False,"extractions":collected},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        journal.append("\n**Statut : ZIP officiels récupérés depuis le portail et contrôlés (schéma, année, zone, annexes) ; certificat TLS non vérifié sur le runner, réserve de provenance à lever indépendamment.**")
    except Exception as e:
        journal.append("\n**Collecte interrompue** : "+type(e).__name__+" — "+str(e)[:1200])
    REPORT.write_text("\n".join(journal)+"\n",encoding="utf-8")
    print(REPORT.read_text(encoding="utf-8")[-8500:])

if __name__=="__main__":main()
