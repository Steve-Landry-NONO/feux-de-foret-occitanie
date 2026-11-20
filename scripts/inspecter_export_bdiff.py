#!/usr/bin/env python3
"""Inspection publique et sans authentification des options d'export BDIFF.

On se limite à la recherche et aux liens publics. Ne saisit aucun compte,
ne contourne pas les accès et ne publie pas de données brutes sans contrôle.
"""
from html.parser import HTMLParser
import json
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

BASE="https://bdiff.agriculture.gouv.fr/incendies"
OUT=Path("docs/resultats/diagnostic_export_bdiff.md")
class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(); self.forms=[];self.links=[];self.buttons=[];self._form=None;self._link=None;self._button=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="form":
            self._form={"action":a.get("action"),"method":a.get("method"),"inputs":[]}
        if tag in ("input","select","button") and self._form is not None:
            self._form["inputs"].append({k:a.get(k) for k in ("name","type","value","id") if a.get(k)})
        if tag=="a":
            self._link={"href":a.get("href"),"text":""}
        if tag=="button":
            self._button={"type":a.get("type"),"text":""}
    def handle_data(self,data):
        if self._link is not None:self._link["text"]+=data
        if self._button is not None:self._button["text"]+=data
    def handle_endtag(self,tag):
        if tag=="form" and self._form:
            self.forms.append(self._form);self._form=None
        if tag=="a" and self._link:
            self.links.append(self._link);self._link=None
        if tag=="button" and self._button:
            self.buttons.append(self._button);self._button=None

def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    report=["# Inspection du portail BDIFF : recherche de l'export officiel","",
            "Cette inspection ne télécharge pas de données de tiers et ne modifie pas le portail.",""]
    try:
        req=urllib.request.Request(BASE,headers={"User-Agent":"HETIC-recherche-academique/1.0","Accept":"text/html"})
        with urllib.request.urlopen(req,timeout=45) as r:
            b=r.read(5_000_000)
            report+=["- URL finale : "+r.url,"- HTTP : "+str(r.status),"- Taille HTML : "+str(len(b))]
        html=b.decode("utf-8",errors="replace")
        p=Inspect();p.feed(html)
        report+=["","## Formulaires (noms publics des champs)","","~~~json",json.dumps(p.forms,ensure_ascii=False,indent=2)[:18000],"~~~",
                 "","## Liens associés à téléchargement / export / CSV / zip",""]
        links=[l for l in p.links if any(k in (str(l["text"])+str(l["href"])).lower() for k in ("csv","export","telecharg","télécharg","zip","download"))]
        for l in links:
            report.append("- "+l["text"].strip()[:130]+" : "+urljoin(BASE,str(l["href"])))
        report+=["","## Boutons et entrées apparentées",""]
        for button in p.buttons:
            if any(k in button["text"].lower() for k in ("csv","filtrer","telecharg","télécharg","export")):
                report.append("- "+button["text"].strip()[:160])
        if not links:report.append("Aucun lien de téléchargement direct reconnu : potentiellement généré par formulaire/session.")
    except Exception as e:
        report+=["","- Échec de la requête : "+type(e).__name__+" — "+str(e)[:600]]
    OUT.write_text("\n".join(report)+"\n",encoding="utf-8")
    print(OUT.read_text(encoding="utf-8")[:3500])

if __name__=="__main__":main()
