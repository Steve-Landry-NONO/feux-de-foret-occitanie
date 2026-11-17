# Matrice questions × sources — faisabilité à confirmer

**Mise à jour : 17 novembre 2026.** La consultation de métadonnées ne vaut pas validation des fichiers. Voir l'[inventaire](inventaire.md) et la [spécification v1](../specification/specification-v1-2026-11-17.md).

| Question | BDIFF | Archives Météo des forêts | Référentiel INSEE | Couverture forestière | Données SDIS |
|---|---|---|---|---|---|
| Q1 — Territoires prioritaires | Événements et localisation à vérifier | — | Correspondances de codes à vérifier | Dénominateur indispensable au ratio | Complément éventuel |
| Q2 — Couverture des seuils | Dates et couverture à vérifier | Danger daté et échéance à vérifier | Raccord départemental | — | — |
| Q3 — Journées de mobilisation et coût | Nécessaire pour distinguer avec/sans feu | Permet le comptage des jours activés sous réserve de complétude | Raccord départemental | — | Nécessaire au coût constaté ; sinon hypothèses explicites |
| Q4 — Comparabilité | Périodes et définitions homogènes | Historique commun requis pour les seuils | Géographie et millésimes homogènes | Nécessaire pour comparer les ratios Q1 | Selon indicateur opérationnel comparé |
| Q5 — Délais de première intervention | Complément de localisation éventuel | Contexte éventuel | Raccord territorial | — | Horodatages, centres, capacités et objectif de délai indispensables |
| Q6 — Départs simultanés et moyens | Multiplicité journalière possible si dates disponibles ; simultanéité non prouvée | Contexte du scénario | Raccord territorial | — | Intervalles d'engagement, disponibilités, compétences et engins indispensables à une mesure réelle |

**Statuts :** les cellules décrivent des besoins ou des usages envisagés, pas des jointures réalisées. « — » signifie non nécessaire au calcul principal.

## Conditions préalables

1. Confirmer un historique commun : BDIFF affiche 2006–2022, les archives météo un début en 2024. Aucun croisement n'est présumé possible.
2. Distinguer date d'émission et date de validité météo ; fixer une échéance.
3. Vérifier le grain événementiel et les clés avant d'agréger au département × jour.
4. Réserver 2022 aux séries qui la couvrent ; ne pas simuler un niveau météo historique absent.
5. Déclarer Q5–Q6 non calculables sur données observées sans accès suffisant ; identifier séparément toute simulation.

## Suivi après revue

Les vérifications A1–A4 sont décrites dans le [plan de suivi](../suivi/actions-faisabilite.md). Elles restent à faire. Aucune ressource métier n'est déclarée exploitable pour un indicateur par cette revue documentaire ; disponibilité, couverture et licence au niveau des fichiers restent à vérifier.
