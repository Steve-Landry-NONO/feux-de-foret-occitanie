# Notebooks d'exploration — V0

Projet **Feux de forêt – Occitanie / SDIS 31**. Ces cinq carnets servent à confronter les hypothèses de la [spécification v1](../docs/specification/specification-v1-2026-11-17.md) aux données réellement disponibles. **Aucune source brute n'a été analysée dans cette première version.**

| Notebook | Questions | Vérification prioritaire |
|---|---|---|
| 01 — BDIFF | Q1, Q2, Q4 | Dates, localisation, granularité et doublons |
| 02 — Météo des forêts | Q2, Q3, Q4 | Période, codes de danger et échéances |
| 03 — Jointures | Q2, Q3, Q4 | Grain département × jour, couverture et cardinalité |
| 04 — Territoires | Q1, Q4 | Référentiels, millésimes et surfaces forestières |
| 05 — SDIS | Q5, Q6 | Accès, horodatages et confidentialité |

## Mode d'emploi

Installer `pandas`, `matplotlib`, `jupyterlab` et ouvrir les carnets avec Jupyter. Les chemins `data/raw/`, `data/processed/` et `data/restricted/` sont des emplacements proposés ; adapter les noms de fichiers après téléchargement et documentation. Ne pas commiter les données brutes ou confidentielles.

Avant toute conclusion, renseigner l'URL de la ressource, sa date, sa licence, son empreinte SHA-256, le grain, la période et les exclusions dans le [suivi de faisabilité](../docs/suivi/actions-faisabilite.md). Les mentions nominatives sont des **demandes de relecture**, pas des validations inventées.

## Étape suivante

Comparer les périodes BDIFF et météo, puis vérifier si la jointure département × jour est possible avant de calculer Q2–Q3. Toute modification du modèle doit rester liée à une question décisionnelle et documenter sa justification.

## Collecte des sources — travail préparatoire (19/11/2026)

Un [catalogue des 18 pistes de données](../docs/sources/catalogue-collecte-v0.md) relie les jeux candidats aux questions Q1–Q6 et signale les jointures encore à tester. Le [script de collecte](../scripts/collecter_data_gouv.py) interroge l'API du catalogue data.gouv.fr et permet de télécharger des ressources explicitement filtrées, avec empreinte SHA-256. Les données brutes restent exclues du dépôt.

Depuis la racine du projet, sur un ordinateur connecté :

```bash
# 1. Vérifier la liste réelle des fichiers Météo des forêts (sans télécharger)
python scripts/collecter_data_gouv.py --jeu archives-de-la-meteo-des-forets --motif '^mdf\\.202[456]$' --lister

# 2. Télécharger uniquement les trois archives annuelles, après vérification des titres
python scripts/collecter_data_gouv.py --jeu archives-de-la-meteo-des-forets --motif '^mdf\\.202[456]$' --telecharger --max-fichiers 3

# 3. Rechercher un export climatologique du département 31 (sans télécharger)
python scripts/collecter_data_gouv.py --jeu donnees-climatologiques-de-base-quotidiennes --motif 'departement_31.*2025-2026' --lister
```

Les fichiers téléchargés et le registre JSONL sont placés sous `data/raw/`. Le script n'a **pas été exécuté sur les fichiers bruts ici**, faute d'accès réseau de téléchargement ; les sorties des notebooks restent donc à produire. La BDIFF demande une étude séparée de son interface d'export, car son catalogue référence une ressource de type API et ne fournit pas directement le même type d'archive.
