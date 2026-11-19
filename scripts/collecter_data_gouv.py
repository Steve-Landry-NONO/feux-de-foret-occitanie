#!/usr/bin/env python3
"""Inventorier puis télécharger des ressources publiques data.gouv.fr de façon reproductible.

N'aspire jamais un jeu entier sans sélection explicite. Aucun fichier brut n'est
créé dans Git ; utiliser data/raw/ (à ignorer par Git).
Dépendances : bibliothèque standard Python 3.10+.
"""

import argparse
import hashlib
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://www.data.gouv.fr/api/1/datasets/"
UA = "HETIC-feux-occitanie/0.1 (recherche académique; contact via GitHub)"
ACCEPTED = ("csv", "csv.gz", "json", "geojson", "zip", "parquet", "gz", "xlsx")


def get_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=50) as response:
        return json.load(response)


def filename_safe(value):
    value = unicodedata.normalize("NFKD", str(value))
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-._")[:80] or "ressource"


def selection(r, motif, formats):
    title = str(r.get("title") or "")
    fmt = str(r.get("format") or "").lower().lstrip(".")
    return re.search(motif, title, flags=re.IGNORECASE) is not None and fmt in formats and bool(r.get("url"))


def download_resource(r, slug, directory, max_bytes):
    identifier = str(r.get("id") or "sans-id")
    fmt = str(r.get("format") or "bin").lower().lstrip(".")
    extension = "." + fmt if fmt else ""
    output = directory / f"{filename_safe(slug)}_{filename_safe(identifier)}_{filename_safe(r.get('title') or 'fichier')}{extension}"
    if output.exists():
        raise FileExistsError(f"Fichier déjà présent, aucun écrasement automatique : {output}")
    tmp = output.with_suffix(output.suffix + ".part")
    h = hashlib.sha256()
    size = 0
    req = urllib.request.Request(r["url"], headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as src, tmp.open("wb") as dst:
            while chunk := src.read(1024 * 1024):
                size += len(chunk)
                if size > max_bytes:
                    raise ValueError(f"Ressource trop volumineuse (limite : {max_bytes // (1024 * 1024)} Mio)")
                h.update(chunk)
                dst.write(chunk)
        tmp.replace(output)
    finally:
        if tmp.exists():
            tmp.unlink()

    return {
        "date_collecte_utc": datetime.now(timezone.utc).isoformat(),
        "jeu": slug, "id_ressource": identifier, "titre": r.get("title"),
        "source_catalogue": API + slug + "/",
        "url_ressource": r.get("url"), "licence_affichee": None,
        "format_declare": fmt, "taille_octets": size,
        "sha256": h.hexdigest(), "fichier_local": str(output),
        "statut": "telecharge_non_profile",
        "periode_reelle": "non_verifiee", "grain_reel": "non_verifie",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jeu", required=True, help="Slug data.gouv.fr, ex. archives-de-la-meteo-des-forets")
    parser.add_argument("--motif", default=".*", help="Regex sur le titre des ressources")
    parser.add_argument("--lister", action="store_true", help="Afficher les ressources, sans téléchargement")
    parser.add_argument("--telecharger", action="store_true", help="Télécharger les ressources filtrées")
    parser.add_argument("--limite-mo", type=int, default=50, help="Limite de taille par fichier (50 Mio par défaut)")
    parser.add_argument("--max-fichiers", type=int, default=5, help="Garde-fou, nombre maximal de fichiers")
    parser.add_argument("--dossier", default="data/raw", help="Dossier local, hors versionnement Git")
    args = parser.parse_args()
    if not args.lister and not args.telecharger:
        parser.error("Choisir --lister ou --telecharger")
    if args.limite_mo < 1 or args.max_fichiers < 1:
        parser.error("Limites strictement positives requises")

    dataset = get_json(API + args.jeu + "/")
    resources = dataset.get("resources", [])
    filtres = [r for r in resources if selection(r, args.motif, ACCEPTED)]
    print(f"Jeu : {dataset.get('title')} — {len(resources)} ressources, {len(filtres)} correspondances")
    for r in filtres:
        print(f"- {r.get('id')} | {r.get('title')} | {r.get('format')} | {r.get('filesize')} octets")
    if not args.telecharger:
        return
    if not filtres:
        raise SystemExit("Aucune ressource correspondant au filtre. Vérifier les titres avec --lister.")
    if len(filtres) > args.max_fichiers:
        raise SystemExit(f"{len(filtres)} fichiers sélectionnés, limite={args.max_fichiers}. Affiner --motif.")
    folder = Path(args.dossier)
    folder.mkdir(parents=True, exist_ok=True)
    manifest = folder / "registre_extractions.jsonl"
    for r in filtres:
        try:
            item = download_resource(r, args.jeu, folder, args.limite_mo * 1024 * 1024)
            item["licence_affichee"] = dataset.get("license")
            with manifest.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")
            print("OK", item["fichier_local"], item["sha256"])
        except (urllib.error.URLError, OSError, ValueError) as exc:
            print(f"ÉCHEC {r.get('title')} : {exc}", file=sys.stderr)
            # Ne pas considérer la collecte réussie si un fichier manque.
            sys.exit(1)


if __name__ == "__main__":
    main()
