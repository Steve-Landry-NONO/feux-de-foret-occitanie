# Note de revue — Disponibilité météo et cohortes Q2–Q3

**Auteur de la contribution :** Ludovic Tuekam  
**Périmètre :** revue des indicateurs Q2–Q3  
**Tickets associés :** #9 et #29  
**Statut :** calculs techniques reproductibles sur les extractions versionnées ; validation métier et humaine encore attendue.

## 1. Constat et preuve de l'intersection

Les unités comptées sont des couples distincts **(département, jour)**, construits à partir des journées avec au moins un feu BDIFF de type F. Une date calendaire commune à plusieurs départements compte donc plusieurs journées départementales.

Pour chaque année :
- **E** = tous les couples département-jour avec au moins un feu BDIFF type F ;
- **A** = couples de E avec une prévision J+1 disponible ;
- **B** = couples de E avec une prévision J+2 disponible ;
- **I = A ∩ B** = couples de E présents simultanément dans A et B.

L'intersection a été calculée directement par égalité des clés département-jour dans le script scripts/auditer_intersection_j1_j2.py. Elle n'est pas déduite du minimum des effectifs.

| Année | E : tous les jours feu | A : J+1 | B : J+2 | A ∩ B | J+1 seul | J+2 seul | Ni J+1 ni J+2 | E hors cohorte |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2024 | 289 | 160 | 159 | **159** | 1 | 0 | 129 | **130** |
| 2025 | 340 | 208 | 210 | **208** | 0 | 2 | 130 | **132** |

Les volumes précédemment annoncés de **159 en 2024** et **208 en 2025 sont donc confirmés comme intersections calculées**.

Clés qui appartiennent à une seule échéance :
- 2024 : J+1 seul — département 11, 4 juin 2024.
- 2025 : J+2 seul — départements 34 et 48, 2 octobre 2025.

Les journées « ni J+1 ni J+2 » sont listées dans le CSV détaillé. Elles peuvent relever de jours hors saison de publication ou d'une indisponibilité à qualifier ; elles ne doivent pas être automatiquement assimilées à des erreurs de collecte.

**Preuves :**
- [Rapport de calcul de l'intersection](../resultats/intersection_j1_j2_feux.md)
- [Détail exhaustif par département-jour et appartenance à A/B/I](../resultats/intersection_j1_j2_feux.csv)
- [Script reproductible](../../scripts/auditer_intersection_j1_j2.py)
- [Exécution GitHub Actions](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/actions/runs/46126102346)

Le script recharge les archives et vérifie leurs SHA-256 depuis les manifestes avant le calcul. Les tests unitaires couvrent notamment un cas où les deux ensembles ont le même effectif mais une intersection strictement plus petite, afin d'empêcher toute déduction par minimum.

## 2. Indicateurs et formules — numérateurs et dénominateurs

| Indicateur | Numérateur | Dénominateur | Statut / interprétation |
|---|---|---|---|
| jours_feu_hors_cohorte | Nombre de clés de E qui ne sont pas dans I | Aucun : c'est un volume | 130 en 2024 ; 132 en 2025 |
| taux_jours_feu_hors_cohorte_pct | Nombre de clés de E hors I | Nombre de clés de E | 130/289 = 44,98 % en 2024 ; 132/340 = 38,82 % en 2025 |
| taux_couverture_cohorte_feu_pct (disponibilité météo sur les jours feu) | Nombre de clés de I | Nombre de clés de E | 159/289 = 55,02 % en 2024 ; 208/340 = 61,18 % en 2025 |
| couverture_conditionnelle_pct (horizon h, seuil s) | Nombre de clés de I avec feu dont le niveau de l'horizon h est ≥ s | Nombre de clés de I avec feu | Couverture des jours feu de la cohorte commune ; afficher le volume du dénominateur |
| jours_surveillance | Nombre de couples département-jour de la grille météo commune dont le niveau de l'horizon choisi est ≥ s | Aucun : c'est un volume | Proxy de journées-département activées, pas un coût financier |
| mobilisation_pct | Nombre de couples département-jour activés au seuil s | Nombre de couples département-jour météo éligibles dans la cohorte commune | Taux de mobilisation simulée, avec et sans feu |
| taux_disponibilite_meteo_pct (global, à construire) | Nombre de couples département-jour attendus avec J+1 ET J+2 valides | Nombre de couples département-jour pour lesquels les deux publications sont attendues selon le calendrier officiel | **Non calculé** : il faut d'abord définir la grille attendue G, y compris les dates et départements où la publication est prévue |

Pour éviter toute ambiguïté, la disponibilité sur les seuls jours BDIFF avec feu est mesurée par taux_couverture_cohorte_feu_pct (I/E). Elle ne remplace pas le taux global de disponibilité météo, dont le dénominateur doit être la grille de publication attendue G, avec ou sans feu.

Exemples de couverture conditionnelle au seuil 2, calculés sur la cohorte commune :

| Année | Horizon | Numérateur : jours feu avec niveau ≥ 2 | Dénominateur : jours feu dans I | Couverture |
|---|---|---:|---:|---:|
| 2024 | J+1 | 134 | 159 | 84,28 % |
| 2024 | J+2 | 127 | 159 | 79,87 % |
| 2025 | J+1 | 181 | 208 | 87,02 % |
| 2025 | J+2 | 174 | 208 | 83,65 % |

Les taux de couverture des seuils ne portent donc pas sur les 289 ou 340 jours BDIFF de départ, mais sur les 159 ou 208 journées départementales avec feu qui disposent simultanément de J+1 et J+2.

## 3. Conséquence pour l'interprétation

Les indicateurs J+1 et J+2 existants décrivent la couverture conditionnelle des journées avec feu dans I. Ils ne décrivent pas la couverture de l'ensemble des journées avec feu recensées dans BDIFF.

La part de journées avec feu exclues de la cohorte commune est non négligeable : 44,98 % en 2024 et 38,82 % en 2025. Cette exclusion doit être visible dans les restitutions et ne doit pas être cachée par le seul taux conditionnel.

## 4. Point de vigilance territorial : Haute-Garonne

- 2024 : une journée départementale avec feu, hors de la cohorte commune ; elle ne dispose ni de J+1 ni de J+2.
- 2025 : quatre journées départementales avec feu, toutes dans la cohorte commune.

Les effectifs restent faibles. Il faut éviter de tirer une conclusion générale sur la performance des seuils à partir de ces seuls volumes.

## 5. Précautions d'interprétation

- Une journée de surveillance sans feu observé ne constitue pas automatiquement un faux positif : l'absence d'événement enregistré ne prouve pas l'absence réelle de feu.
- Météo-France décrit les archives avec le champ Reference_time (date et heure de production). Les fichiers du dépôt exposent une colonne date ; l'équivalence de ces deux champs reste à corroborer formellement.
- Le manifeste BDIFF indique que le contrôle du certificat TLS lors du téléchargement initial n'est pas confirmé. Les SHA-256 vérifiées garantissent l'intégrité des fichiers versionnés, pas à elles seules l'authenticité du transport initial.
- La Météo des forêts est une information départementale de sensibilisation du public, et non une doctrine opérationnelle SDIS. Les scénarios restent pédagogiques.
- Les faibles effectifs de Haute-Garonne imposent d'afficher les dénominateurs et de limiter les conclusions.

## 6. Documents de référence du dépôt

- docs/resultats/validation_j1_j2_v1.md
- docs/resultats/kpi_scenarios_q2_q3.md
- docs/resultats/kpi_scenarios_q2_q3_manifest.json
- docs/resultats/intersection_j1_j2_feux.md
- docs/resultats/intersection_j1_j2_feux.csv
- docs/modelisation/modeles-de-donnees-v0.md
- docs/modelisation/modele-decisionnel-v1-ludovic.md

## 7. Suite proposée

Faire relire par le groupe :
1. la définition du jour BDIFF et le traitement des événements multiples le même jour ;
2. l'alignement du champ date avec Reference_time ;
3. le calendrier attendu pour calculer la disponibilité météo globale ;
4. la provenance TLS des exports BDIFF ;
5. les formules et l'interprétation des seuils.

Les résultats techniques et les fichiers de preuve sont désormais présents sur la branche personnelle. Ils restent soumis à la revue humaine et à la coordination de l'intégration de la PR #29 avec la PR #3 et le ticket #12.
