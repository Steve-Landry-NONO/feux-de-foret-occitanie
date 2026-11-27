#!/usr/bin/env python3
"""Préparer les tables territoriales d’Occitanie depuis les CSV officiels INSEE."""
import argparse
import csv
import hashlib
import io
import json
import re
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SOURCES = ("v_commune_2024.csv", "v_commune_2025.csv", "v_departement_2025.csv")
DEPARTEMENTS = set("09 11 12 30 31 32 34 46 48 65 66 81 82".split())
CATALOGUE = "https://www.data.gouv.fr/datasets/code-officiel-geographique-1"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_archives(directory):
    metadata = []
    files = {}
    for year, page, name in (
        (2024, "7766585", "v_commune_2024.csv"),
        (2025, "8377162", "cog_ensemble_2025_csv.zip"),
    ):
        url = f"https://www.insee.fr/fr/statistiques/fichier/{page}/{name}"
        final_url = None
        if directory:
            raw = (directory / name).read_bytes()
        else:
            with urllib.request.urlopen(url, timeout=120) as response:
                raw = response.read()
                final_url = response.url
        if year == 2025:
            with zipfile.ZipFile(io.BytesIO(raw)) as bundle:
                if bundle.testzip() is not None:
                    raise ValueError(f"Archive corrompue : {name}")
                for member in (*SOURCES[1:], "v_mvt_commune_2025.csv"):
                    files[member] = bundle.read(member)
        else:
            files[name] = raw
        metadata.append({"fichier": name, "url": url, "url_finale_observee": final_url,
                         "millesime": year, "octets": len(raw), "sha256": sha256(raw)})
    return files, metadata


def read_source(name, raw, key, fields):
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
    if not reader.fieldnames or not set(fields) <= set(reader.fieldnames):
        raise ValueError(f"Colonnes attendues absentes dans {name}")
    rows = list(reader)
    if any(None in row or None in row.values() for row in rows):
        raise ValueError(f"Ligne CSV mal formée dans {name}")
    is_commune = key == "COM"
    expected_national = {"v_commune_2024.csv": 34935, "v_commune_2025.csv": 34875, "v_departement_2025.csv": 101}
    base = [row for row in rows if not is_commune or row["TYPECOM"] == "COM"]
    if len(base) != expected_national[name] or len({row[key] for row in base}) != len(base):
        raise ValueError(f"Effectif national ou unicité inattendu dans {name}")
    subset = sorted((row for row in base if row["REG"] == "76"), key=lambda row: row[key])
    if {row["DEP"] for row in subset} != DEPARTEMENTS:
        raise ValueError(f"Couverture régionale incohérente dans {name}")
    pattern = r"\d{5}" if is_commune else r"\d{2}"
    if any(not re.fullmatch(pattern, row[key]) or not row[key].startswith(row["DEP"]) or not row["LIBELLE"] for row in subset):
        raise ValueError(f"Code ou libellé invalide dans {name}")
    meta = {
        "fichier": name,
        "millesime": int(name[-8:-4]), "sha256": sha256(raw), "octets": len(raw),
        "lignes_nationales": len(rows), "lignes_nationales_apres_filtre_type": len(base),
        "colonnes": reader.fieldnames, "lignes_occitanie": len(subset),
        "filtre": "REG=76 et TYPECOM=COM" if is_commune else "REG=76",
    }
    return subset, meta


def csv_output(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrees", type=Path, help="Dossier des fichiers officiels déjà téléchargés")
    parser.add_argument("--sortie", type=Path, required=True)
    parser.add_argument("--date-collecte-utc", help="Date UTC constatée pour les fichiers locaux")
    args = parser.parse_args()
    if args.entrees and not args.date_collecte_utc:
        parser.error("--entrees requiert --date-collecte-utc")
    commune_fields = ["COM", "DEP", "REG", "TYPECOM", "LIBELLE", "NCC"]
    dep_fields = ["DEP", "REG", "LIBELLE", "NCC"]
    archives, archive_metadata = load_archives(args.entrees)
    tables, metadata = {}, []
    for name in SOURCES:
        key, fields = ("COM", commune_fields) if name.startswith("v_commune") else ("DEP", dep_fields)
        tables[name], meta = read_source(name, archives[name], key, fields)
        metadata.append(meta)
    c24, c25, dep25 = tables.values()
    old = {row["COM"]: row for row in c24}
    new = {row["COM"]: row for row in c25}
    common = old.keys() & new.keys()
    changes = []
    for code in sorted(old.keys() | new.keys()):
        before, after = old.get(code), new.get(code)
        if before is None or after is None or (before["DEP"], before["LIBELLE"]) != (after["DEP"], after["LIBELLE"]):
            changes.append({
                "COM": code,
                "statut": "apparu" if before is None else "disparu" if after is None else "attribut_modifie",
                "libelle_2024": before["LIBELLE"] if before else "",
                "libelle_2025": after["LIBELLE"] if after else "",
                "dep_2024": before["DEP"] if before else "",
                "dep_2025": after["DEP"] if after else "",
            })
    movement_bytes = archives["v_mvt_commune_2025.csv"]
    movement_rows = list(csv.DictReader(io.StringIO(movement_bytes.decode("utf-8-sig")), strict=True))
    movement_fields = ["DATE_EFF", "MOD", "TYPECOM_AV", "COM_AV", "LIBELLE_AV",
                       "TYPECOM_AP", "COM_AP", "LIBELLE_AP"]
    if not movement_rows or not set(movement_fields) <= set(movement_rows[0]):
        raise ValueError("Schéma des mouvements inattendu")
    movements = [
        row for row in movement_rows
        if "2024-01-01" < row["DATE_EFF"] <= "2025-01-01"
        and (row["COM_AV"] in old or row["COM_AP"] in new)
        and (row["TYPECOM_AV"] == "COM" or row["TYPECOM_AP"] == "COM")
    ]
    outputs = {
        "occitanie_communes_2024.csv": csv_output(commune_fields, c24),
        "occitanie_communes_2025.csv": csv_output(commune_fields, c25),
        "occitanie_departements_2025.csv": csv_output(dep_fields, dep25),
        "mouvements_communes_2024_2025.csv": csv_output(movement_fields, movements),
        "ecarts_communes_2024_2025.csv": csv_output(
            ["COM", "statut", "libelle_2024", "libelle_2025", "dep_2024", "dep_2025"], changes),
    }
    manifest = {
        "producteur": "Insee", "catalogue": CATALOGUE,
        "licence_catalogue": "Licence Ouverte (fr-lo)",
        "date_collecte_utc": args.date_collecte_utc or datetime.now(timezone.utc).isoformat(),
        "mode": "Fichiers officiels locaux" if args.entrees else "HTTPS",
        "archives": archive_metadata,
        "mouvements": {"fichier": "v_mvt_commune_2025.csv", "sha256": sha256(movement_bytes),
                       "lignes_nationales": len(movement_rows), "lignes_retenues": len(movements)},
        "sources": metadata, "codes_communs": len(common),
        "ecarts": dict(Counter(row["statut"] for row in changes)),
        "communes_par_dep_2024": dict(sorted(Counter(row["DEP"] for row in c24).items())),
        "communes_par_dep_2025": dict(sorted(Counter(row["DEP"] for row in c25).items())),
        "sorties_sha256": {name: sha256(data) for name, data in outputs.items()},
    }
    args.sortie.mkdir(parents=True, exist_ok=True)
    for name, data in outputs.items():
        (args.sortie / name).write_bytes(data)
    (args.sortie / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
