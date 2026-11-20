# Scénarios Q2–Q3 : seuils Météo des forêts et journées de surveillance

**Exploration pédagogique conditionnelle — pas une recommandation officielle au SDIS 31.**

## Hypothèses et définition des KPI

- Unité : **département × jour de validité**. Les lignes BDIFF sont agrégées en jours avec au moins un feu de type F.
- Pour une comparaison honnête de J+1 et J+2, ne conserver que les jours où **les deux échéances existent** ; ce dénominateur est identique pour les seuils 2, 3 et 4.
- Une journée de surveillance est comptée quand le niveau prévu atteint le seuil.
- Couverture = journées avec feu recensé et surveillance / journées avec feu recensé parmi les jours éligibles.
- Mobilisation sans feu observé = journées de surveillance - journées avec feu couvertes. Ce n'est pas une mesure d'inefficacité.
- Coût de surveillance : **proxy en journées-département**, sans inventer de dépense monétaire.

## Haute-Garonne (31) — cœur de la commande

### Année 2024
| Échéance | Seuil | Jours éligibles | Jours avec feu | Jours de surveillance | Jours avec feu couverts | Couverture | Jours sans feu observé mobilisés |
|---|---:|---:|---:|---:|---:|---:|---:|
| J+1 | ≥ 2 | 119 | 0 | 16 | 0 | n.d. | 16 |
| J+1 | ≥ 3 | 119 | 0 | 1 | 0 | n.d. | 1 |
| J+1 | ≥ 4 | 119 | 0 | 0 | 0 | n.d. | 0 |
| J+2 | ≥ 2 | 119 | 0 | 12 | 0 | n.d. | 12 |
| J+2 | ≥ 3 | 119 | 0 | 1 | 0 | n.d. | 1 |
| J+2 | ≥ 4 | 119 | 0 | 0 | 0 | n.d. | 0 |

### Année 2025
| Échéance | Seuil | Jours éligibles | Jours avec feu | Jours de surveillance | Jours avec feu couverts | Couverture | Jours sans feu observé mobilisés |
|---|---:|---:|---:|---:|---:|---:|---:|
| J+1 | ≥ 2 | 119 | 4 | 51 | 2 | 50.0 % | 49 |
| J+1 | ≥ 3 | 119 | 4 | 10 | 2 | 50.0 % | 8 |
| J+1 | ≥ 4 | 119 | 4 | 0 | 0 | 0.0 % | 0 |
| J+2 | ≥ 2 | 119 | 4 | 47 | 2 | 50.0 % | 45 |
| J+2 | ≥ 3 | 119 | 4 | 10 | 2 | 50.0 % | 8 |
| J+2 | ≥ 4 | 119 | 4 | 0 | 0 | 0.0 % | 0 |

## Occitanie — comparaison régionale

### Année 2024
| Échéance | Seuil | Jours éligibles | Jours avec feu | Jours de surveillance | Jours avec feu couverts | Couverture | Jours sans feu observé mobilisés |
|---|---:|---:|---:|---:|---:|---:|---:|
| J+1 | ≥ 2 | 1547 | 159 | 403 | 134 | 84.28 % | 269 |
| J+1 | ≥ 3 | 1547 | 159 | 77 | 45 | 28.3 % | 32 |
| J+1 | ≥ 4 | 1547 | 159 | 1 | 1 | 0.63 % | 0 |
| J+2 | ≥ 2 | 1547 | 159 | 365 | 127 | 79.87 % | 238 |
| J+2 | ≥ 3 | 1547 | 159 | 39 | 24 | 15.09 % | 15 |
| J+2 | ≥ 4 | 1547 | 159 | 0 | 0 | 0.0 % | 0 |

### Année 2025
| Échéance | Seuil | Jours éligibles | Jours avec feu | Jours de surveillance | Jours avec feu couverts | Couverture | Jours sans feu observé mobilisés |
|---|---:|---:|---:|---:|---:|---:|---:|
| J+1 | ≥ 2 | 1547 | 208 | 651 | 181 | 87.02 % | 470 |
| J+1 | ≥ 3 | 1547 | 208 | 177 | 93 | 44.71 % | 84 |
| J+1 | ≥ 4 | 1547 | 208 | 7 | 5 | 2.4 % | 2 |
| J+2 | ≥ 2 | 1547 | 208 | 613 | 174 | 83.65 % | 439 |
| J+2 | ≥ 3 | 1547 | 208 | 142 | 78 | 37.5 % | 64 |
| J+2 | ≥ 4 | 1547 | 208 | 7 | 5 | 2.4 % | 2 |

## Autres livrables

- [Table complète des indicateurs par département](kpi_scenarios_q2_q3.csv), années et échéances (168 lignes).
- [Journées avec feu ou situées dans le 31](jours_feu_et_31.csv), utiles pour contrôler les observations.
- [Manifeste des hypothèses et restrictions](kpi_scenarios_q2_q3_manifest.json).

## Validation nécessaire avant toute conclusion opérationnelle

1. Le producteur documente J+1 et J+2, mais l'équivalence entre le champ de fichier 'date' et 'Reference_time' n'a pas été formellement corroborée.
2. Contrôler les ZIP BDIFF avec un téléchargement indépendant vérifiant les certificats HTTPS.
3. Faire valider le périmètre, les formules et les exclusions par les membres du groupe.
4. La Météo des forêts est un **produit de sensibilisation du public** et non la doctrine opérationnelle de surveillance SDIS.
5. Les faibles effectifs du 31 impliquent de présenter les taux avec leur dénominateur, plutôt que d'y voir une précision statistique.
