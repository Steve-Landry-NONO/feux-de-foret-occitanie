# Feux de forêt en Occitanie — Projet HETIC MD5

> **Statut : dossier de cadrage pédagogique, en cours de validation collective.** Aucun résultat chiffré ni accès à une source n'est affirmé sans vérification.

## 1. Contexte et commande

Dans le cadre de l'UE01 « Stratégie business data-driven », volet « Modélisation et pipelines de données », le groupe répond à une commande fictive de la **direction du SDIS 31 (Haute-Garonne)**, pour préparer la saison 2027. Deux arbitrages structurent l'étude : **où concentrer les moyens humains et financiers** et **à partir de quel niveau de la Météo des forêts déclencher un dispositif renforcé**. Le commanditaire demande une comparaison avec les autres départements d'Occitanie et la France entière.

Le projet ne vise pas à prédire automatiquement chaque incendie. Il vise à produire des données documentées et des analyses utiles aux décisions, tout en explicitant les limites des observations.

## 2. Équipe

| Membre | Responsabilité proposée — à confirmer |
|---|---|
| Maeva QUENUM | Sources, inventaire et matrice questions × sources |
| Chantal CAMARA | Qualité, conformité et définitions |
| Stéphane DOMI | Pipelines, chargement et traçabilité |
| Ludovic TUEKAM | Modèle décisionnel et analyse des seuils |
| Steve Landry NONO | Coordination, dépôt, tickets, checkpoints et journal |

Les responsabilités sont proposées et ne préjugent pas de l'accord des membres. Chacun contribue à l'analyse, à la documentation et aux revues.

## 3. Démarche méthodologique

**Décision → question analytique → termes à définir → besoin mesurable → données idéales → sources vérifiées.** Nous ne partons pas du catalogue pour inventer ensuite des questions. Chaque question doit changer une décision selon sa réponse.

Pour chaque source : relever le producteur, le mode d'accès, le grain, l'emprise, la période réellement couverte, la mise à jour, la volumétrie, les clés, la licence et les données personnelles. Une information inconnue est notée **« non vérifiée »**, jamais supposée.

## 4. Livrables et calendrier

| Date | Livrable |
|---|---|
| 16 novembre 2026 | Analyses individuelles, fiches et inventaire de sources, glossaire v0 (8 termes minimum), matrice v0 |
| 17 novembre 2026 | Spécification v1 en FOAD |
| 18 novembre 2026 | Rendu de la spécification |
| 9 décembre 2026 | Entrepôt en étoile historisé et testé |
| 11 décembre 2026 | Entrepôt final et soutenance |

## 5. Organisation documentaire

- `docs/analyse/` : analyses individuelles, conformes au template de l'exercice 1 ;
- `docs/collectif/` : propositions de questions collectives et argumentaire ;
- `docs/sources/` : fiches, inventaire et matrice ;
- `docs/glossaire.md` : définitions métier et divergences ;
- `docs/decisions/` : journal des arbitrages.

## 6. Convention de travail Git

Créer un ticket par tâche, travailler sur une branche dédiée, produire des commits courts et explicites **en français**, ouvrir une pull request, demander une relecture et fusionner après validation. Les analyses individuelles doivent être relues, appropriées et **commitées par chaque membre depuis son propre compte**, conformément à l'énoncé. Les brouillons préparés collectivement ne constituent pas une preuve de contribution individuelle.

Exemples de commits : `docs(analyse): rédiger mon analyse de la commande` ; `docs(sources): documenter la source BDIFF` ; `docs(glossaire): préciser la notion de départ de feu`.

## 7. Hypothèses et limites à vérifier

- La disponibilité et la compatibilité temporelle des archives de danger et d'incendies ;
- L'échelle géographique réelle des données de danger ;
- La définition d'un « feu de forêt » et le risque de confondre feu, départ de feu et intervention ;
- Les coûts et capacités de mobilisation du SDIS, potentiellement absents de l'open data ;
- La possibilité de comparer des territoires de tailles et surfaces forestières différentes ;
- Les effets des données manquantes et des changements de codes géographiques.

## 8. État d'avancement

**Préparation documentaire :** en cours. **Choix définitif des rôles, questions, sources et seuils :** à valider par le groupe. **Résultats d'analyse :** non produits à ce stade.

## 9. Références pédagogiques

Marine PROST, HETIC 2026–2027 : « Exercice 1 — De la commande aux données — Occitanie », « Template analyse de la commande », « Exercice 2 — Fiche d'identité des sources », « Le glossaire du projet » et support UE01.A — C1.
