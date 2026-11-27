# Prototype de tableau de bord Q2–Q3

**Objectif :** rendre les résultats du [calculateur de scénarios](../scripts/calculer_scenarios_q2_q3.py) compréhensibles sans connaître Python.

## Démarrage local

Depuis la racine du dépôt, après génération des rapports :

```bash
python3 scripts/calculer_scenarios_q2_q3.py
python3 -m http.server 8000
```

Ouvrir ensuite **http://localhost:8000/dashboard/**.

L'interface charge le CSV [docs/resultats/kpi_scenarios_q2_q3.csv](../docs/resultats/kpi_scenarios_q2_q3.csv) depuis le même dépôt. Elle ne possède **ni API secrète, ni backend, ni données simulées**, et n'accède pas au serveur du SDIS. Un double-clic sur le fichier HTML sans serveur local peut échouer à charger le CSV à cause des restrictions du navigateur.

## Fonctionnalités V0

- Sélection de l'année (2024, 2025), de la Haute-Garonne, de la région Occitanie ou d'un autre département.
- Comparaison de J+1/J+2 à dénominateur strictement égal.
- Comparaison des seuils ≥2, ≥3 et ≥4, et de leur compromis surveillance / couverture.
- Détail des journées de mobilisation, des journées avec feu couvertes ou manquées, et des journées mobilisées sans feu recensé.
- Absence de taux fictif lorsque le nombre de journées avec feu est nul : **n.d.**
- Affichage permanent des réserves relatives au recensement BDIFF, aux dates et au caractère pédagogique.

## Limites et garde-fous

Cette V0 est une **restitution interactive descriptive**, pas une application de pilotage d'interventions, ni une prédiction du comportement des feux. Les données sont départementales, et aucun coût réel n'est fourni. Les conclusions du 31 doivent être interprétées avec précaution lorsque le nombre de journées avec feu est faible.

Le projet devra valider la correspondance des dates des archives météo et la provenance TLS des ZIP BDIFF avant toute conclusion métier définitive.

## Évolutions envisagées

Après revue du modèle et des KPI : filtre de cohorte temporelle, graphique de sensibilité par année, intégration d'une carte **2D** sur référentiel géographique fiable, puis scénarios de moyens avec paramètres explicites. Une simulation **3D** ou un modèle d'apprentissage ne seront retenus que si leurs hypothèses sont contrôlables et si le résultat éclaire une décision Q1–Q6.
