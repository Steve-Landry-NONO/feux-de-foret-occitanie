# Analyse de la commande - Stéphane DOMI

> **Proposition de travail à relire, personnaliser et valider par l'étudiant concerné.** Commande : SDIS 31, Haute-Garonne — saison des feux 2027.

## 1. Les questions

Quatre questions dont la réponse aiderait la direction à trancher.

> [!test] Test
> Si la réponse est X, la direction fait A ; si elle est Y, elle fait B. Si A et B sont identiques, la question n'est pas pertinente.

1. **À quelle granularité peut-on rapprocher les observations d'incendie et de danger ?** Argument décisionnel : Choisir le grain de l'entrepôt sans fabriquer de précision artificielle.
2. **Quelle profondeur historique commune est disponible ?** Argument décisionnel : Choisir une période d'étude robuste et reproductible.
3. **Quels écarts de codes géographiques empêchent les jointures ?** Argument décisionnel : Mettre en place un référentiel de correspondance historisé.
4. **Quelles mises à jour pourraient modifier une analyse déjà produite ?** Argument décisionnel : Conserver les versions et rendre les chargements traçables.

## 2. Les termes inconnus

| Terme | Ce que je crois qu'il veut dire | Ce qu'il faudrait vérifier |
|---|---|---|
| Départ de feu | Événement initial d'ignition | Définition et règles de dédoublonnage du producteur |
| Feu de forêt | Incendie affectant un espace boisé | Périmètre retenu par chaque source |
| Danger élevé | Niveau de danger de la Météo des forêts | Niveaux exacts et correspondance avec les données historiques |
| Dispositif renforcé | Patrouilles, guet et moyens additionnels | Coût, durée et critères actuels de déclenchement |
| Département | Territoire administratif de comparaison | Compatibilité avec les zones météo et les zones de couverture des secours |

## 3. Les besoins

**La décision à éclairer, en une phrase :** Choisir le grain de l'entrepôt sans fabriquer de précision artificielle. Choisir une période d'étude robuste et reproductible. Mettre en place un référentiel de correspondance historisé. Conserver les versions et rendre les chargements traçables.

**Ce qui manque dans la commande pour y répondre :**
- Le seuil actuellement appliqué, sa justification et son historique.
- Les contraintes budgétaires chiffrées et les capacités humaines disponibles.
- Les définitions opérationnelles des événements, les périodes d'observation et les zones exactes.
- Les conditions de comparabilité des données entre départements.

## 4. Les données

Pour chaque question, la donnée idéale qu'il faudrait disposer avant de choisir les sources.

| Question | Donnée idéale | Grain (une ligne = ?) | Période | Fraîcheur | Emprise géographique |
|---|---|---|---|---|---|
| 1 | Clés temporelles et géographiques des deux sources | Source × champ | Historique pluriannuel, incluant si possible 2024–2026 ; à vérifier | Dernier millésime disponible ; à vérifier | Haute-Garonne, Occitanie et France selon la question |
| 2 | Dates minimales et maximales des observations | Source × année | Historique pluriannuel, incluant si possible 2024–2026 ; à vérifier | Dernier millésime disponible ; à vérifier | Haute-Garonne, Occitanie et France selon la question |
| 3 | Codes INSEE, millésimes, communes et départements | Code géographique × millésime | Historique pluriannuel, incluant si possible 2024–2026 ; à vérifier | Dernier millésime disponible ; à vérifier | Haute-Garonne, Occitanie et France selon la question |
| 4 | Dates de publication, versions et historiques | Fichier × version | Historique pluriannuel, incluant si possible 2024–2026 ; à vérifier | Dernier millésime disponible ; à vérifier | Haute-Garonne, Occitanie et France selon la question |

*Note méthodologique : la période et la fraîcheur sont des besoins idéaux, et non des caractéristiques vérifiées de sources existantes.*
