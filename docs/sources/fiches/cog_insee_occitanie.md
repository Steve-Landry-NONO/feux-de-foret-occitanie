# Code officiel géographique INSEE — Occitanie, 2024 et 2025

Refs #8, #13 et #17. Contrôles exécutés avec l’assistance de Codex le 27 novembre 2026.

| Rubrique | Valeur |
|---|---|
| Producteur et accès | INSEE. [COG au 1er janvier 2024](https://www.insee.fr/fr/information/7766585) et [COG au 1er janvier 2025](https://www.insee.fr/fr/information/8377162). CSV 2024 et ZIP CSV 2025 récupérés en HTTPS. |
| Licence | Licence Ouverte affichée sur le [catalogue officiel](https://www.data.gouv.fr/datasets/code-officiel-geographique-1) (`fr-lo`). Attribution des tables dérivées : INSEE, Code officiel géographique, millésimes 2024 et 2025. |
| Date de publication | Page 2024 mise à jour le 20 février 2024. Publication de la page 2025 le 4 mars 2025. Les millésimes décrivent la géographie au 1er janvier. Diffusion annuelle. |
| Format et contenu | Membres CSV UTF-8 à virgules. `v_commune` contient notamment TYPECOM, COM, REG, DEP, LIBELLE, COMPARENT. `v_departement` contient DEP, REG, CHEFLIEU et LIBELLE. `v_mvt_commune_2025` contient date d’effet, motif, codes et types avant/après. |
| Grain, clés et emprise | Une commune en vigueur par `(millésime, COM)` après filtre `TYPECOM=COM`. Un département par `(millésime, DEP)`. Une ligne de mouvement décrit une relation avant/après à une date d’effet. Origine nationale, sorties filtrées sur `REG=76`. Les codes sont des chaînes, y compris les zéros initiaux. |
| Volumétrie | 37 544 et 37 548 lignes nationales brutes dans les fichiers communes 2024 et 2025. 101 lignes dans le fichier départements 2025. Pour le détail régional, voir les preuves ci-dessous. |
| Données personnelles | Les tables examinées portent sur des unités administratives et leurs libellés. |
| Questions servies | Q1 et Q4 pour le rattachement territorial. La superficie forestière et les géométries viennent d’autres sources. |

## Preuves et contrat d’intégration

Les deux ressources officielles ont été ouvertes et leurs empreintes calculées. Les deux CSV directs de 2025 (communes et départements) ont également été téléchargés. Leurs empreintes correspondent aux mêmes fichiers dans le ZIP. Le manifeste conserve sources, schémas, filtres, effectifs et empreintes des sorties.

| Contrôle | Résultat |
|---|---|
| Périmètre | 13 départements, dont le 31. 4 453 communes en 2024 et 4 446 en 2025. 586 communes en Haute-Garonne dans chacun des deux millésimes. |
| Unicité | Aucun doublon de COM après filtre TYPECOM=COM dans chaque millésime, ni de DEP dans le fichier 2025. |
| Comparaison | 4 445 codes communs, 8 codes disparus et 1 apparu. Parmi les codes communs, 6 ont un libellé ou un département modifié. |
| Mouvements | 26 lignes INSEE couvrant les changements pertinents, avec les types avant/après. Conques-en-Rouergue passe de `12076` à `12218` le 4 mars 2024. Garder ces dates pour un rapprochement à la date de l’événement. |
| Raccord exploratoire BDIFF | Sur les ZIP de la PR #3, 413/413 lignes 2024 et 472/472 lignes 2025 retrouvent un code et le bon département avec le COG du même millésime. Un raccord des feux 2024 au COG 2025 laisse 3 lignes sans correspondance, sous les codes `09287` et `34093`. Transport initial des ZIP toujours à corroborer selon #5. |

**Pour Stéphane et Ludovic.** Importer `COM`, `DEP` et `REG` en texte. Ajouter le millésime à partir du nom du fichier et construire la clé `(millésime, COM)`. Conserver les codes BDIFF bruts. Pour des résultats en géographie 2025, convertir explicitement les cas concernés en suivant les mouvements officiels, avec contrôle de cardinalité. Par exemple, `09287 → 09088` et `34093 → 34144` le 1er janvier 2025. Un code commun peut aussi désigner une commune dont le périmètre a changé. Le fichier des mouvements contient des lignes `COMD` et peut avoir plusieurs lignes par code initial. Une jointure directe avec ce fichier peut multiplier les événements.

Pour un rattachement territorial précis **à la date de l’alerte**, prendre en compte la date d’effet des mouvements. Le test ci-dessus établit une compatibilité avec des instantanés annuels.

## Reproduction

Depuis la racine du dépôt, avec Python 3 et un accès HTTPS :

```bash
python3 scripts/collecter_cog_insee.py --sortie /tmp/cog-occitanie
```

Pour rejouer hors ligne avec les deux fichiers officiels listés dans le manifeste :

```bash
date_collecte="$(python3 -c 'import json; print(json.load(open("datasets/public/insee_cog_2025/manifest.json"))["date_collecte_utc"])')"
python3 scripts/collecter_cog_insee.py --entrees /chemin/vers/fichiers-insee \
  --sortie /tmp/cog-occitanie --date-collecte-utc "$date_collecte"
diff -rq datasets/public/insee_cog_2025 /tmp/cog-occitanie
```

La reproduction hors ligne a produit les mêmes fichiers octet pour octet. Voir les [tables et le manifeste](../../../datasets/public/insee_cog_2025/).

### Reproduire le raccord exploratoire aux copies BDIFF

```bash
git fetch origin refs/heads/docs/notebooks-exploration-v0-2026-11-19
python3 - <<'PY'
import csv
import io
import subprocess
import zipfile
from pathlib import Path

directory = Path("datasets/public/insee_cog_2025")
ref = "479e5d91296a5994eaed304678504cdc05fb3a17"
indices = {}
for year in (2024, 2025):
    with (directory / f"occitanie_communes_{year}.csv").open(encoding="utf-8") as stream:
        indices[year] = {row["COM"]: row["DEP"] for row in csv.DictReader(stream)}
for year in (2024, 2025):
    path = f"datasets/public/bdiff_officiel/bdiff_occitanie_{year}.zip"
    raw = subprocess.check_output(["git", "show", f"{ref}:{path}"])
    with zipfile.ZipFile(io.BytesIO(raw)) as bundle:
        lines = bundle.read("Incendies.csv").decode("utf-8-sig").splitlines()
    events = list(csv.DictReader(lines[2:], delimiter=";"))
    for target, index in indices.items():
        missing = [row["Code INSEE"] for row in events if row["Code INSEE"] not in index]
        conflicts = [row["Code INSEE"] for row in events if row["Code INSEE"] in index
                     and index[row["Code INSEE"]] != row["Département"].zfill(2)]
        print(year, target, len(events), len(missing), sorted(set(missing)), len(conflicts))
PY
```
