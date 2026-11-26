# Revue des archives Météo des forêts en Haute-Garonne

Cette revue complète le [ticket #4](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/issues/4). Les groupes de lignes étudiés correspondent au code département `31`. Les trois archives sont celles de la [PR #3 au commit 479e5d9](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/tree/479e5d9/datasets/public/meteo_des_forets). Chaque empreinte SHA-256 calculée correspond au manifeste.

| Archive | Lignes du 31 | Première date brute (UTC) | Dernière date brute (UTC) | Dates brutes répétées |
|---|---:|---|---|---:|
| 2024 | 120 | 2024-06-03 | 2024-09-30 | 0 |
| 2025 | 120 | 2025-06-03 | 2025-09-30 | 0 |
| 2026 | 131 | 2026-05-28 | 2026-10-05 | 0 |

Les deux colonnes de niveau sont renseignées sur toutes les lignes examinées et leurs valeurs sont comprises entre 1 et 4. Le champ `date` est lu en UTC. Ce relevé décrit les dates présentes dans le fichier. La correspondance exacte du champ avec la date de référence du producteur reste à confirmer avant de fixer définitivement la règle de jointure par date de validité.

Pour reproduire le contrôle, vérifier les empreintes des archives avec le manifeste, ouvrir chaque CSV avec son séparateur déclaré, filtrer `num_dep=31`, puis compter les lignes et les dates distinctes dans `date`. Contrôler les valeurs de `niveau_j1` et `niveau_j2` sur ce même sous-ensemble.

Contrôles exécutés avec l’assistance de Codex. Relecture par Maeva et Steve attendue.
