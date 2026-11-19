# Archives Météo des forêts 2024–2026 — données publiques

**Producteur :** Météo-France  
**Catalogue :** https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets  
**Licence affichée au catalogue :** Licence Ouverte / Open Licence 2.0  
**Collecte :** 19 novembre 2026, via GitHub Actions  
**Statut :** fichiers téléchargés, intégrité enregistrée, premiers champs observés ; analyse métier et jointures à confirmer.

## Contenu versionné

| Fichier | Lignes de données | Séparateur | Colonnes observées |
|---|---:|---|---|
| `mdf_2024.csv.gz` | 11 520 | `,` | `date, num_dep, niveau_j1, niveau_j2, nom_dep` |
| `mdf_2025.csv.gz` | 11 520 | `,` | `date, num_dep, niveau_j1, niveau_j2, dep_nom` |
| `mdf_2026.csv.gz` | 12 576 | `;` | `date, num_dep, niveau_j1, niveau_j2, nom_dep` |

Les ressources ont été téléchargées depuis les **identifiants pérennes officiels** et conservées sous forme compressée **sans modification**. Le fichier [manifest.json](manifest.json) contient les URLs exactes, la date de collecte, les tailles, les identifiants et les empreintes SHA-256.

## Usage pour le projet SDIS 31

- **Q2 :** confronter les jours avec départ de feu au niveau météorologique prédit (sous réserve d'obtenir des dates BDIFF compatibles).
- **Q3 :** compter les jours pour lesquels un seuil de danger aurait déclenché un dispositif renforcé.
- **Q4 :** comparer les saisons et les départements sur des fenêtres et règles homogènes.

### Points encore à vérifier

1. La signification de la colonne `date` (émission ou date de référence) et les règles exactes de validité de `niveau_j1` et `niveau_j2`.
2. La couverture des 13 départements d'Occitanie, les jours absents, les codes et les éventuels doublons.
3. Les modalités de correspondance avec les événements BDIFF : **une date commune et un code département ne suffisent pas sans vérifier le grain et la cardinalité**.
4. La portée de la licence pour la ressource et les obligations d'attribution. La licence affichée est documentée, mais l'équipe doit finaliser la fiche d'identité.

**Important :** ces archives ne contiennent pas les incendies eux-mêmes et ne permettent donc pas de calculer seules le taux de couverture des journées avec feu. Les résultats des analyses ne doivent pas être inventés.

## Reproductibilité

Les fichiers ont été collectés par `scripts/collecter_archives_mdf_ci.py` et contrôlés avant commit par le workflow `.github/workflows/collecte-mdf.yml`. Une nouvelle extraction doit être publiée comme une **version révisée clairement datée**, après comparaison des empreintes, et non écraser silencieusement les archives présentes.

Les autres données volumineuses ou confidentielles restent exclues du dépôt par `.gitignore`.
