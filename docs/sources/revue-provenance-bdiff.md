# Vérification de provenance BDIFF — 27 novembre 2026

Refs #5. Les archives examinées proviennent du commit `479e5d91296a5994eaed304678504cdc05fb3a17`. Le manifeste et le script de collecte indiquent que la vérification du certificat TLS était désactivée lors de la collecte originale. 

Depuis un clone du dépôt, après `git fetch origin refs/heads/docs/notebooks-exploration-v0-2026-11-19` :

```bash
python3 - <<'PY'
import hashlib
import io
import json
import subprocess
import zipfile

base = "479e5d91296a5994eaed304678504cdc05fb3a17:datasets/public/bdiff_officiel/"

def read(path):
    return subprocess.check_output(["git", "show", base + path])

for archive in json.loads(read("manifest.json"))["extractions"]:
    raw = read(archive["fichier"])
    assert len(raw) == archive["octets"]
    assert hashlib.sha256(raw).hexdigest() == archive["sha256"]
    with zipfile.ZipFile(io.BytesIO(raw)) as bundle:
        assert bundle.testzip() is None
        print(archive["annee"], len(raw), hashlib.sha256(bundle.read("Incendies.csv")).hexdigest())
PY
```

| Année | Taille du ZIP (octets) | SHA-256 du CSV interne |
|---|---:|---|
| 2024 | 602878 | `d4409942d4cd9f2296489f62e85a8f4cf1f340a90a0061a548633a4c30996595` |
| 2025 | 604702 | `a19b489e19937cebb84ac846632d2d3703e39ed5e58295db1971f928caddc2b2` |

Les deux empreintes ZIP concordent avec le manifeste et les contrôles CRC sont passés. Ces contrôles établissent l’intégrité des copies versionnées. Ils ne prouvent pas la provenance du transfert initial.

```bash
curl -fsSL --max-time 10 -o /dev/null -w 'HTTP %{http_code} TLS %{ssl_verify_result}\n' \
  https://bdiff.agriculture.gouv.fr/incendies
```

La requête lancée avec la vérification TLS par défaut a renvoyé `HTTP 503 TLS 0`. Aucun export indépendant n’a été obtenu. La prochaine vérification consiste à refaire la recherche officielle pour 2024 et 2025 avec les filtres consignés au manifeste, puis à comparer le préambule, les identifiants, les dates et les colonnes du CSV interne. Un ZIP peut changer d’empreinte si son emballage change. Garder les originaux et le manifeste intacts.

Contrôles exécutés avec l’assistance de Codex. Ticket #5 ouvert.
