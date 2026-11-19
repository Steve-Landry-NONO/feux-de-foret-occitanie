#!/usr/bin/env python3
"""Collecte contrôlée des archives publiques MdF 2024-2026 sur un runner connecté.

Le téléchargement est effectué exclusivement depuis les identifiants stables
des ressources officielles data.gouv.fr. On valide les fichiers avant publication.
"""
from __future__ import annotations
import csv
import gzip
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RESOURCES = {
    "2024": "59f2c103-f8d5-4216-9e46-de2327f4dc5a",
    "2025": "c1f8f7c8-e8cc-4d70-9372-43da3c878c81",
    "2026": "14f5607c-68b1-4b91-be36-b1265f309c51",
}
DIR = Path("datasets/public/meteo_des_forets")
MAX_SIZE = 5 * 1024 * 1024  # ~0,5 Mo annoncés par ressource ; garde-fou 5 Mio
MIN_ROWS = 100

def main():
    DIR.mkdir(parents=True, exist_ok=True)
    entries = []
    for year, rid in RESOURCES.items():
        url = f"https://www.data.gouv.fr/api/1/datasets/r/{rid}"
        target = DIR / f"mdf_{year}.csv.gz"
        req = urllib.request.Request(url, headers={"User-Agent": "HETIC-MD5-feux-occitanie-academic/0.1"})
        # Pas d'écrasement silencieux des données déjà collectées.
        if target.exists():
            raise SystemExit(f"Le fichier existe déjà : {target}. Effectuer une revue avant actualisation.")
        with urllib.request.urlopen(req, timeout=90) as response:
            blob = response.read(MAX_SIZE + 1)
        if not blob.startswith(b"\x1f\x8b") or len(blob) > MAX_SIZE:
            raise SystemExit(f"Échec de validation du GZIP {year} (taille / signature)")
        try:
            decompressed = gzip.decompress(blob)
            text = decompressed.decode("utf-8-sig")
            # Un parseur csv sert seulement à compter les lignes physiques : pas de modèle métier présumé.
            header = text.splitlines()[0] if text.splitlines() else ""
            candidates = (";", ",", "\t", "|")
            sep = max(candidates, key=header.count)
            print(f"Entête archive {year} : {header[:200]!r} ; séparateur détecté : {sep!r}")
            if header.count(sep) == 0:
                raise SystemExit(f"Impossible de détecter le séparateur CSV pour {year}")
            rows = list(csv.reader(text.splitlines(), delimiter=sep))
        except (OSError, UnicodeError, csv.Error) as exc:
            raise SystemExit(f"Archive {year} non exploitable comme CSV : {exc}")
        if len(rows) < MIN_ROWS or len(rows[0]) < 2:
            raise SystemExit(f"Archive {year} suspecte : {len(rows)} lignes, {len(rows[0]) if rows else 0} champs")
        target.write_bytes(blob)
        entries.append({
            "annee_archive": year,
            "source": "Météo-France — Archives de la Météo des forêts",
            "page_catalogue": "https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets",
            "url_ressource_stable": url,
            "identifiant_ressource": rid,
            "licence_catalogue": "Licence Ouverte / Open Licence 2.0",
            "date_collecte_utc": datetime.now(timezone.utc).isoformat(),
            "fichier": str(target),
            "taille_octets": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "lignes_y_compris_entete": len(rows),
            "en_tetes_observees": rows[0],
            "separateur_csv": sep,
            "statut": "fichier_telecharge_et_structure_initiale_observee",
            "grain_reel": "a_confirmer",
            "couverture_reelle": "a_confirmer",
            "jointures": "non_validees",
        })
        print(f"{year} : {len(blob)} octets / {len(rows)-1} enregistrements / SHA256 {entries[-1]['sha256']}")

    manifest = DIR / "manifest.json"
    manifest.write_text(json.dumps({"schema_version":1,"extractions":entries},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__ == "__main__":
    main()
