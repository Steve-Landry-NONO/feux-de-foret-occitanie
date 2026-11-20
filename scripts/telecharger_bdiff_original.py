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
    if not zipfile.is_zipfile(io.BytesIO(data)):raise ValueError("Réponse ZIP invalide : "+repr(data[:140]))
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=z.namelist()
        csvs=[n for n in names if n.lower().endswith(".csv")]
        pdfs=[n for n in names if n.lower().endswith(".pdf")]
        if len(csvs)!=1: raise ValueError("On attend un CSV unique, trouvé : "+str(csvs))
        if not pdfs:raise ValueError("Documentation PDF manquante dans l'export")
        raw=z.read(csvs[0])
        txt=raw.decode("utf-8-sig")
        try:sep=csv.Sniffer().sniff(txt[:4096],delimiters=";,\t").delimiter
        except csv.Error:sep=";"
        candidates=txt.splitlines()[:5]
        reader=csv.DictReader(io.StringIO(txt),delimiter=sep)
        rows=list(reader)
        return {"fichiers":names,"csv":csvs[0],"pdfs":pdfs,"premieres_lignes_csv":candidates,"champs":reader.fieldnames,"separateur":sep,"lignes":len(rows),
                "extrait_annees":sorted({str(row.get(k,"")) for row in rows for k in (reader.fieldnames or []) if normaliser(k) in ("annee","annee du feu")}),
                "extrait_departements":sorted({str(row.get(k,"")) for row in rows for k in (reader.fieldnames or []) if "departement" in normaliser(k)}),
                "premiere_ligne_extrait":{"noms_champs":list(rows[0]) if rows else []}}

def main():
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    journal=["# Tentative de collecte officielle BDIFF","",
             "Source : https://bdiff.agriculture.gouv.fr/incendies ; méthode : formulaire public GET puis lien /incendies/zip.",
             "**Attention :** l'instance GitHub Actions rencontre une anomalie de chaîne TLS sur le site. La lecture utilise ici un contexte sans vérification de certificat ; **le transport n'est donc pas authentifié** et les fichiers restent en quarantaine tant qu'un contrôle indépendant n'est pas réalisé.",
             ""]
    cert=ssl._create_unverified_context()
    opener=build_opener(HTTPCookieProcessor(CookieJar()),HTTPSHandler(context=cert))
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
            filename=f"bdiff_occitanie_{annee}_transport_tls_non_verifie.zip"
            (OUT/filename).write_bytes(zipped)
            journal.append(f"- SHA-256 : {hashlib.sha256(zipped).hexdigest()}")
        journal.append("\n**Statut : fichiers téléchargés techniquement, à mettre en quarantaine avant publication.**")
    except Exception as e:
        journal.append("\n**Collecte interrompue** : "+type(e).__name__+" — "+str(e)[:1200])
    REPORT.write_text("\n".join(journal)+"\n",encoding="utf-8")
    print(REPORT.read_text(encoding="utf-8")[-8500:])

if __name__=="__main__":main()
