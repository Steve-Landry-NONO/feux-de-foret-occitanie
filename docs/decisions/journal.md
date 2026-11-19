# Journal des décisions

| Date | Objet | Décision | Justification | Statut |
|---|---|---|---|---|
| 2026-11-17 | Région et commanditaire | Occitanie, commande pédagogique SDIS 31 (Haute-Garonne) | Sujet attribué au groupe | **Validé** |
| 2026-11-17 | Répartition des responsabilités | Steve : coordination ; Maeva : sources ; Chantal : qualité et conformité ; Stéphane : pipelines ; Ludovic : modélisation | Répartition explicitement confirmée par le responsable de coordination | **Validé** |
| 2026-11-17 | Questions du cadrage | Q1 à Q6 retenues, incluant délais d'intervention, effectifs et moyens matériels | Couvrir les deux arbitrages de la commande et leur faisabilité opérationnelle | **Validé pour le cadrage** |
| 2026-11-17 | Revue de pertinence | Chaque question est reliée à une décision opérationnelle | Vérification méthodologique du caractère décisionnel | **Effectuée** |
| 2026-11-17 | Sources, définitions, indicateurs et coûts | Conserver le statut « à vérifier » tant qu'aucune donnée n'a été contrôlée | Éviter toute validation fictive | **En cours** |
| 2026-11-17 | Contributions personnelles | Chaque étudiant doit relire et commiter son analyse sous son compte | Exigence de l'exercice 1 ; fichiers initialement préparés par la coordination | **À réaliser / vérifier** |

**Portée :** la validation du cadrage et des rôles est consignée à la demande du responsable de coordination ; elle ne constitue ni une preuve de vote formel des cinq membres ni une validation de données non examinées.

## Contribution documentaire du 17 novembre 2026 — à relire

La contribution transmise par Chantal CAMARA et restructurée avec l'assistance de ChatGPT (Codex) ajoute la [spécification v1](../specification/specification-v1-2026-11-17.md), issue du document de rendu transmis. L'inventaire, la matrice Q1–Q6 et le README sont alignés sur cette proposition.

- **Constat documentaire :** les fiches BDIFF et archives météo ont été consultées ; les données brutes ne sont pas vérifiées.
- **Réserve :** le chevauchement temporel des sources reste à démontrer.
- **Propositions méthodologiques :** séparer les grains communal et départemental, documenter l'échéance météo, distinguer zéro et absence de données, distinguer multiplicité journalière et simultanéité.
- **Statut :** soumis à relecture via pull request ; aucune validation collective, personnelle des cinq analyses ou opérationnelle n'est ajoutée par cette contribution.

Les responsabilités existantes sont conservées. Les arbitrages sur les périodes, les ressources retenues et la faisabilité de Q5–Q6 restent à consigner après revue.

## Retour de revue du coordinateur — 17 novembre 2026

Revue transmise par Chantal : avis favorable sous réserve des corrections documentaires C1–C3 ; nouvelle revue du diff attendue avant fusion. Cet avis n'est pas enregistré comme une approbation GitHub ni comme une validation des données.

**Provenance et responsabilité :** Chantal CAMARA, référente qualité et conformité, a transmis le document de rendu et demandé son adaptation au dépôt. Le document transmis déclare une assistance de Claude à la rédaction ; la restructuration en spécification v1, la revue des pages publiques et les corrections documentaires ont été réalisées avec l'assistance de ChatGPT (Codex). Cette contribution est soumise à la relecture de Chantal et du groupe ; elle ne constitue ni une rédaction personnelle sans assistance ni une validation des données ou des analyses individuelles.

| Point | Modification documentaire | Statut |
|---|---|---|
| C1 | Provenance et nature de l'assistance explicitées dans la spécification et le journal | Correction proposée ; à relire |
| C2 | Répertoires specification et suivi ajoutés à l'arborescence du README | Correction proposée ; à relire |
| C3 | Licences affichées distinguées des licences des fichiers ; aucune donnée ou calcul déclaré validé | Revue documentaire effectuée ; vérifications métier à faire |
| A1–A4 | [Plan distinct de suivi](../suivi/actions-faisabilite.md), avec résultats attendus et rôles proposés | Planifiées dans le dépôt, non réalisées |

Les commits de correction décrivent l'assistance à la rédaction ; ils ne certifient pas l'appropriation personnelle du texte par un membre. La fusion et la revue finale restent distinctes de cette mise à jour.

## Mise à jour du 19 novembre 2026 — collecte réelle et modèle de données V0

**Contexte :** après la validation documentaire de la PR #2, la coordination a préparé et exécuté la première collecte publique et les notebooks d'exploration sur la branche de [PR #3](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/pull/3). Les modifications de ce jour sont des travaux techniques de coordination, avec assistance IA ; elles ne remplacent pas les commits ni les validations personnelles des autres membres.

| Décision / constat | Justification et preuve | État |
|---|---|---|
| Conserver le **SDIS 31** comme point de décision et l'Occitanie comme comparateur | [Questions Q1–Q6](../collectif/questions-retenues-proposition.md) | **Périmètre inchangé** |
| Versionner les archives météo ouvertes et de petite taille | Fichiers 2024–2026, manifeste SHA-256 et licence affichée, [rapport](../resultats/profilage_sources_v1.md) | **Collecte exécutée** |
| Distinguer **raccord technique** et **KPI métier** | 2024 : source incendie Esri dérivée, sans validation de date J1/J2 ni exhaustivité BDIFF | **Point de vigilance maintenu** |
| Ne pas publier des données secondaires dont la redistribution est non qualifiée | Conditions d'usage de la couche Esri non établies | **Bruts hors du dépôt** |
| Rendre visible un échec de collecte | ArcGIS 2025 HTTP 404 ; INSEE HTTP 504, [diagnostic](../resultats/diagnostic_insee_v0.md) | **Bloqué, non masqué** |
| Produire UML conceptuel, flux et schéma étoile **en V0** | [Document de modélisation](../modelisation/modeles-de-donnees-v0.md) rattaché aux six questions | **Proposé à la revue** |
| Préserver l'historique Git, réintégrer les évolutions de main sans force-push | Synchronisation de branche via GitHub Actions | **Effectuée** |
| Faire relire la PR avant intégration dans main | [Issues #4 à #8](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/issues), PR #3 prête pour relecture | **Revue attendue, fusion non réalisée** |

**Aucune approbation de Maeva, Chantal, Stéphane ou Ludovic n'est présumée dans ce journal.** Les décisions de modèle et les KPI doivent être finalisés sur preuve après les véritables retours des membres.
