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
