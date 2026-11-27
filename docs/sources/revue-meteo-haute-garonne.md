# Revue des archives Météo des forêts en Haute-Garonne

Cette revue complète le [ticket #4](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/issues/4). Les groupes de lignes étudiés correspondent au code département `31`. Les trois archives sont celles de la [PR #3 au commit 479e5d9](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/tree/479e5d9/datasets/public/meteo_des_forets). Chaque empreinte SHA-256 calculée correspond au manifeste.

| Archive | Lignes du 31 | Première date brute (UTC) | Dernière date brute (UTC) | Dates brutes répétées |
|---|---:|---|---|---:|
| 2024 | 120 | 2024-06-03 | 2024-09-30 | 0 |
| 2025 | 120 | 2025-06-03 | 2025-09-30 | 0 |
| 2026 | 131 | 2026-05-28 | 2026-10-05 | 0 |

Les deux colonnes de niveau sont renseignées sur toutes les lignes examinées et leurs valeurs sont comprises entre 1 et 4. Le champ `date` est lu en UTC. Ce relevé décrit les dates présentes dans le fichier. La correspondance exacte du champ avec la date de référence du producteur reste à confirmer avant de fixer définitivement la règle de jointure par date de validité.

## Reproduction depuis un clone du dépôt

Exécuter à la racine avec Git, Python 3.9+ et la base de fuseaux horaires IANA. Le contrôle lit les objets Git en place sans modifier le répertoire de travail.

```bash
git fetch origin refs/heads/docs/notebooks-exploration-v0-2026-11-19
python3 - <<'PYCODE'
import csv
import gzip
import hashlib
import io
import json
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo

ref = "479e5d91296a5994eaed304678504cdc05fb3a17"
directory = "datasets/public/meteo_des_forets"

def read(path):
    return subprocess.check_output(["git", "show", f"{ref}:{path}"])

manifest = json.loads(read(f"{directory}/manifest.json"))
for archive in manifest["extractions"]:
    raw = read(archive["fichier"])
    assert hashlib.sha256(raw).hexdigest() == archive["sha256"]
    with io.TextIOWrapper(gzip.GzipFile(fileobj=io.BytesIO(raw)), encoding="utf-8-sig", newline="") as stream:
        rows = [row for row in csv.DictReader(stream, delimiter=archive["separateur_csv"]) if row["num_dep"] == "31"]
    stamps = [datetime.fromisoformat(row["date"].replace("Z", "+00:00")) for row in rows]
    dates = [stamp.date() for stamp in stamps]
    hours = [stamp.astimezone(ZoneInfo("Europe/Paris")).time() for stamp in stamps]
    invalid = sum(row[key] not in {"1", "2", "3", "4"} for row in rows for key in ("niveau_j1", "niveau_j2"))
    print(archive["annee_archive"], len(rows), min(dates), max(dates),
          len(dates) - len(set(dates)), invalid, min(hours), max(hours), "SHA-256 OK")
PYCODE
```

Sortie obtenue le 27 novembre 2026. Les colonnes donnent l’année, le nombre de lignes, les bornes des dates UTC, les dates répétées, les niveaux absents ou hors domaine, puis les bornes horaires en heure de Paris.

```text
2024 120 2024-06-03 2024-09-30 0 0 18:00:00 18:00:00 SHA-256 OK
2025 120 2025-06-03 2025-09-30 0 0 16:50:02 16:50:09 SHA-256 OK
2026 131 2026-05-28 2026-10-05 0 0 16:50:02 16:50:10 SHA-256 OK
```

## Corroboration du champ date

La [documentation des archives](https://confluence-meteofrance.atlassian.net/wiki/spaces/OpenDataMeteoFrance/pages/1492025345/) décrit `Reference_time` comme l’horodatage de production, et J+1/J+2 comme les échéances de validité. Le [catalogue Météo-France](https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets) fournit un échantillon indépendant des archives annuelles.

```bash
sample_url=https://static.data.gouv.fr/resources/archives-de-la-meteo-des-forets/20260909-144222/donnees-expertisees-meteodesforets-echantillons-20240522.zip
sample_zip="$(mktemp)"
curl -fsSL "$sample_url" -o "$sample_zip"
sha256sum "$sample_zip"
unzip -p "$sample_zip" tableau-meteo-foret.csv | awk -F';' 'NR==1 || $2=="31"'
unzip -p "$sample_zip" carte-meteo-foretJ1.png > carte-meteo-foretJ1.png
rm "$sample_zip"
```

Le ZIP téléchargé a pour SHA-256 `d5ccd236fb6cd681a736261627e5f67034a869c2cd270f9040fc9946a172c960`. Le CSV renvoie l’en-tête `reference_time;dep_code;niveau_j1;niveau_j2;dep_nom` et, pour le 31, `2024-05-22T14:50:05Z;31;2;1;Haute-Garonne`. La carte J+1 du même ZIP indique une diffusion le 22 mai à 17 h et une validité le 23 mai. L’horodatage de l’échantillon correspond à 16 h 50 min 05 s à Paris le jour de la diffusion.

Ce recoupement confirme la distinction production, diffusion et validité pour l’échantillon. Les heures observées en 2025 et 2026 sont compatibles avec cette interprétation. Le jour de l’échantillon est hors de la plage du CSV annuel 2024 et l’heure de celui-ci diffère. L’équivalence exacte entre `date` et `Reference_time` dans les exports annuels, en particulier en 2024, reste à confirmer avec une carte couvrant une date commune ou une réponse du producteur.

Contrôles exécutés avec l’assistance de Codex. Relecture humaine attendue. Ticket #4 ouvert.
