# Note de revue — Disponibilité météo et cohortes Q2–Q3

**Auteur de la contribution :** Ludovic Tuekam  
**Périmètre :** revue des indicateurs Q2–Q3  
**Ticket associé :** #9  
**Statut :** observation à faire valider par l'équipe, pas une décision métier approuvée.

## 1. Constat sur la cohorte commune

Les indicateurs J+1 et J+2 sont calculés sur une cohorte commune de journées pour lesquelles les données météo nécessaires sont disponibles.

Les éléments de validation consultés indiquent :

| Année | Journées départementales avec feu BDIFF | Journées présentes dans la cohorte commune | Écart |
|---|---:|---:|---:|
| 2024 | 289 | 159 | 130 |
| 2025 | 340 | 208 | 132 |

Ces volumes sont des observations département-jour et ne doivent pas être interprétés comme des dates calendaires uniques.

## 2. Conséquence pour l'interprétation

Les taux de couverture actuellement calculés décrivent la couverture des journées avec feu présentes dans la cohorte météo commune.

Ils ne décrivent donc pas directement la couverture de l'ensemble des journées avec feu recensées dans BDIFF.

Il faut conserver cette distinction dans les tableaux de bord et les restitutions afin de ne pas surestimer la portée des résultats.

## 3. Proposition d'indicateurs complémentaires

En complément des indicateurs existants, proposer :

- `jours_feu_hors_cohorte` : nombre de journées départementales avec feu exclues de la cohorte commune ;
- `taux_disponibilite_meteo` : part des journées éligibles disposant des données météo requises ;
- `couverture_conditionnelle_pct` : couverture calculée uniquement sur les journées avec feu présentes dans la cohorte commune.

Ces indicateurs sont des propositions à discuter. Ils ne doivent pas remplacer les calculs existants sans validation collective.

## 4. Point de vigilance territorial : Haute-Garonne

Les résultats consultés indiquent :

- 2024 : une journée départementale avec feu recensée, non retrouvée dans la cohorte commune ;
- 2025 : quatre journées départementales avec feu recensées, retrouvées dans la cohorte commune.

Les effectifs sont faibles. Il faut éviter de tirer une conclusion générale sur la performance des seuils à partir de ces seuls volumes.

## 5. Précautions d'interprétation

- Une journée de surveillance sans feu observé ne constitue pas automatiquement un faux positif : l'absence d'événement enregistré ne prouve pas l'absence réelle de feu.
- La correspondance entre le champ `date` de l'archive météo et `Reference_time` reste à confirmer.
- Le contrôle TLS de la source BDIFF n'est pas confirmé dans le manifeste consulté.
- Les résultats doivent rester présentés comme une analyse exploratoire, et non comme une doctrine opérationnelle SDIS.

## 6. Documents de référence du dépôt

- `docs/resultats/validation_j1_j2_v1.md`
- `docs/resultats/kpi_scenarios_q2_q3.md`
- `docs/resultats/kpi_scenarios_q2_q3_manifest.json`
- `docs/resultats/profilage_bdiff_officiel_v1.md`
- `docs/modelisation/modeles-de-donnees-v0.md`

## 7. Suite proposée

Faire valider par l'équipe la définition de la cohorte, la sémantique des dates météo et la qualification TLS de BDIFF avant toute évolution des calculs de couverture.
