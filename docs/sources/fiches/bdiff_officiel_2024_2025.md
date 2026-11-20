# Fiche source — BDIFF, exports officiels Occitanie (2024 et 2025)

**Producteur et portail :** Base de Données sur les Incendies de Forêts, ministère de l'Agriculture / IGN. [Portail de recherche BDIFF](https://bdiff.agriculture.gouv.fr/incendies) · [Document d'aide au téléchargement](https://bdiff.agriculture.gouv.fr/aide/recherche).

**Questions concernées :** Q1, Q2 et Q4. **Commanditaire du cas pédagogique :** SDIS 31, avec les autres départements d'Occitanie pour comparaison.

**Conditions de publication :** le catalogue data.gouv.fr affiche la Licence Ouverte 2.0 ; le ZIP contient aussi les mentions légales exactes, qui doivent être lues et conservées. **Réserve de provenance :** la collecte automatisée a nécessité une exception de vérification du certificat HTTPS sur le runner GitHub ; le transport doit être corroboré indépendamment avant validation définitive de l'origine.

## 1. Extractions préservées à l'identique

| Année | Fichier ZIP conservé | Incendies type F | Dont Haute-Garonne (31) | Annexe |
|---|---|---:|---:|---|
| 2024 | [bdiff_occitanie_2024.zip](../../../datasets/public/bdiff_officiel/bdiff_occitanie_2024.zip) | 413 | 1 | CSV + PDF définitions + PDF mentions légales |
| 2025 | [bdiff_occitanie_2025.zip](../../../datasets/public/bdiff_officiel/bdiff_occitanie_2025.zip) | 472 | 4 | CSV + PDF définitions + PDF mentions légales |

**Filtres réellement présents dans les CSV :** région administrative OCCITANIE ; première alerte du 1er janvier au 31 décembre de chaque année ; **Type de feu : F**. Toutes les lignes observées portent le bon millésime et un code département appartenant à l'Occitanie. Les 13 départements ne sont pas nécessairement représentés par un feu chaque année.

**Métadonnées de collecte :** les URL complètes de recherche et de téléchargement, dates, tailles, contrôles, empreintes SHA-256 et la réserve TLS se trouvent dans le [manifest.json](../../../datasets/public/bdiff_officiel/manifest.json).

## 2. Colonnes réelles et grain

Le CSV contient deux lignes de préambule, puis l'en-tête séparé par point-virgule, avec les champs :
`Année`, `Numéro`, `Département`, `Code INSEE`, `Nom de la commune`, `Date de première alerte`, plusieurs champs de **surface en m²**, `Précision des surfaces`, `Nature`, et des indicateurs de dommages.

**Grain observé :** une fiche incendie BDIFF / une ligne. La clé candidate `Année × Numéro` ne présente pas de doublon dans les deux extractions ; cela ne démontre pas à lui seul son unicité dans l'ensemble de BDIFF.

**Définitions importantes :** le CSV ne doit pas être confondu avec une chronologie des **engagements de moyens SDIS**. Les surfaces parcourues sont des résultats d'incendie, pas des surfaces forestières servant de dénominateur pour Q1.

## 3. Contrôles et jointures

Le [rapport d'exécution du profilage](../../resultats/profilage_bdiff_officiel_v1.md) constate :

- **2024 :** 289 journées *département × jour* avec incendie ; 161 ont une ligne météo de même date brute.
- **2025 :** 340 journées *département × jour* avec incendie ; 208 ont une ligne météo de même date brute.
- **Pour le 31 :** un incendie observé en 2024 et quatre en 2025 ; cette rareté limite les analyses isolées sur le département.

**Le raccord sur la même date n'est pas une validation du KPI Q2.** Pour Q2/Q3, il faut documenter la date de validité des prévisions J+1/J+2, distinguer jours hors période météo des lacunes et contrôler le recensement. Pour Q1, il faut encore les surfaces forestières IGN et les référentiels INSEE au millésime adapté.

## 4. Points à faire valider par le groupe

- **Maeva :** vérifier la provenance avec un téléchargement HTTPS indépendamment contrôlé, comparer les filtres et la licence des annexes PDF.
- **Chantal :** confirmer les definitions, les exclusions, les limites de couverture et les mentions d'attribution.
- **Stéphane :** revérifier les identifiants, le grain, les périodes et les cardinalités.
- **Ludovic :** valider les formules de KPI et la pertinence des échantillons de Haute-Garonne.

Ces éléments sont des propositions de revue, **pas des avis déjà donnés**. Le document et ses données restent sur la PR avant approbation collective.
