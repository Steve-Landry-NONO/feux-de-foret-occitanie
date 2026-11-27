# Audit d'invariants des indicateurs Q2–Q3

**Statut :** contrôles automatisés exécutés après les calculs sur les 168 combinaisons, avec succès.

- Conservation : feux couverts + feux non couverts = jours avec feu éligibles.
- Mobilisation : surveillance avec feu + sans feu observé = journées surveillées.
- Aucune couverture définie lorsque le nombre de journées avec feu est nul.
- Plus le seuil augmente, moins il peut y avoir de jours surveillés ou de jours avec feu couverts.
- Cohorte strictement identique pour J+1 et J+2, dans chaque territoire et chaque année.
- Une table de 168 indicateurs : 2 années × 14 territoires (13 départements + Occitanie) × 2 horizons × 3 seuils.

**Cet audit garantit la cohérence arithmétique, pas l'authenticité TLS, ni la sémantique du champ date, ni une interprétation causale des résultats.**
