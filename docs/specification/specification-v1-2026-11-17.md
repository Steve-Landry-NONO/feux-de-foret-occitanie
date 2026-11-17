# Spécification v1 — Prévenir et détecter les feux de forêt en Occitanie
## Aide à la décision pour le SDIS 31 — saison 2027

**Date :** 17 novembre 2026.  
**Statut :** proposition de spécification v1 soumise à relecture collective ; aucune validation finale ni analyse de données brutes revendiquée.  
**Provenance et responsabilité :** Chantal CAMARA, référente qualité et conformité, a transmis le document de rendu et demandé son adaptation au dépôt. Le document transmis déclare une assistance de Claude à la rédaction ; la restructuration en spécification v1, la revue des pages publiques et les corrections documentaires ont été réalisées avec l'assistance de ChatGPT (Codex). Cette contribution est soumise à la relecture de Chantal et du groupe ; elle ne constitue ni une rédaction personnelle sans assistance ni une validation des données ou des analyses individuelles. Les responsabilités de l'équipe restent celles du [README](../../README.md). Ce document développe le rendu transmis et ne remplace pas les analyses individuelles.

## 1. Objet et périmètre

Ce projet pédagogique HETIC (UE01 Stratégie Business Data-Driven, encadrement Marine PROST) traduit la commande du cas SDIS 31 en données, indicateurs et contrôles explicables. Il doit éclairer deux arbitrages : où concentrer la prévention et la détection, et à quel niveau de danger renforcer la surveillance. La capacité d'intervention complète ces arbitrages.

L'étude principale porte sur la Haute-Garonne (31). L'Occitanie constitue un premier cadre comparatif ; la comparaison nationale sera limitée aux territoires disposant de données compatibles. L'hypothèse d'une saison 2027 difficile appartient au cas pédagogique : elle n'est pas une prévision démontrée par ce rendu.

Le livrable du 17 novembre est une **spécification**, pas un tableau de résultats. La remise est prévue le 18 novembre, puis l'entrepôt historisé et testé le 9 décembre et la soutenance le 11 décembre, selon les jalons du dépôt. La conformité exacte au barème devra être confrontée au support pédagogique, non joint ici.

### Contexte documentaire

La synthèse du ministère [S3] situe l'Occitanie parmi cinq régions concentrant 90 % des communes déclarées exposées en 2022. Elle distingue l'exposition, les événements et les surfaces parcourues. Ces informations nationales motivent l'étude, mais ne permettent pas de classer les communes du 31. Les chiffres de contexte ne doivent pas devenir des résultats départementaux.

## 2. Traçabilité avec le cadrage collectif

Les questions ci-dessous reprennent le périmètre [Q1 à Q6](../collectif/questions-retenues-proposition.md).

| ID | Question et décision | Données nécessaires | Sortie attendue | Condition de faisabilité |
|---|---|---|---|---|
| Q1 | Fréquence des départs rapportée à l'exposition forestière ; prioriser les territoires | Événements localisés, surface forestière, géographie historisée | Classement argumenté et carte, avec volumes et dénominateurs | Grain communal et surface compatibles |
| Q2 | Part des journées avec feu couverte par chaque seuil ; choisir un déclenchement | Événements datés et niveaux de danger quotidiens | Tableau de couverture et journées manquées par seuil | Historique commun et date de validité identifiée |
| Q3 | Journées de surveillance par seuil ; arbitrer la mobilisation | Niveaux quotidiens ; événements pour ventiler avec/sans feu ; coûts si accessibles | Nombre de jours activés et, séparément, scénario de coût | Coûts explicités ; absence d'observation distinguée de zéro |
| Q4 | Stabilité temporelle et comparaison territoriale ; apprécier la robustesse | Données et définitions homogènes | Comparaisons par saison et territoire, limites | Même fenêtre et même méthode |
| Q5 | Délais et capacités insuffisants ; prépositionner les moyens | Alerte, arrivée, centres, disponibilité et objectif opérationnel | Distribution des délais et écarts à l'objectif | Accès SDIS et objectif justifié |
| Q6 | Moyens nécessaires pour plusieurs départs simultanés ; dimensionner les renforts | Intervalles d'engagement, équipes, compétences, engins disponibles | Scénarios de charge et déficit de moyens | Accès SDIS ou hypothèses explicitement simulées |

## 3. Sources : preuves disponibles et vérifications restantes

**Revue documentaire effectuée le 17/11/2026. Aucun fichier métier brut n'a été téléchargé ni profilé.** Une fiche consultée prouve une déclaration de métadonnées, pas la complétude des observations.

| ID | Référence | Constat documentaire | Réserve à lever |
|---|---|---|---|
| S1 | [BDIFF sur data.gouv.fr](https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff) | Fiche publiée par l'IGN, licence affichée : Licence Ouverte 2.0 ; données décrites depuis 2006 et agrégation communale | Couverture affichée 2006–2022 malgré une description évoquant l'année antérieure et une mise à jour du 13/12/2025 ; vérifier millésimes, granularité temporelle et champs réels |
| S2 | [Archives Météo des forêts](https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets/informations) | Météo-France, licence affichée : Licence Ouverte 2.0 ; couverture annoncée depuis le 03/06/2024, départementale ; mise à jour affichée le 05/10/2026 | Dates réellement renseignées, schéma, codes et échéances à contrôler dans les ressources |
| S3 | [Les feux de forêts — notre-environnement](https://www.notre-environnement.gouv.fr/themes/risques/article/les-feux-de-forets) | Synthèse du ministère, mise à jour le 14/09/2026 | Source de contexte ; ne fournit pas ici les observations nécessaires aux jointures |
| S4 | [Météo des forêts — Météo-France](https://meteofrance.com/meteo-des-forets) | Information de danger départementale à quatre niveaux, pour le lendemain et le surlendemain | Choisir une échéance constante et conserver la date d'émission pour éviter d'utiliser une information indisponible au moment de la décision |

**Blocage prioritaire :** les couvertures explicitement affichées de S1 et S2 ne se chevauchent pas. Cela ne prouve pas l'absence de données récentes dans BDIFF ; cela interdit de présumer le rapprochement possible. Q2 et la ventilation avec/sans feu de Q3 resteront non calculables tant qu'un historique commun n'est pas vérifié. Q3 peut néanmoins compter les jours d'activation à partir de la météo seule.

Les référentiels INSEE, la surface forestière IGN, Gaspar et les données SDIS restent **candidats à examiner**. Gaspar ne remplace pas une surface forestière mesurée. Prométhée peut être étudiée en complément historique, mais sa couverture, ses définitions et les éventuels recouvrements avec BDIFF doivent être vérifiés avant usage ; ne pas additionner deux bases sans dédoublonnage. Le flux météo courant n'est pas un substitut automatique aux archives.

## 4. Définitions, grain et règles de rapprochement

Les règles suivantes sont des **propositions de projet** à confronter aux producteurs et à faire relire par le groupe. Elles complètent le [glossaire](../glossaire.md).

- **Événement retenu :** un incendie conforme au périmètre documentaire du producteur ; conserver l'identifiant source et distinguer événement et intervention.
- **Journée avec feu :** département × date avec au moins un événement distinct retenu. Plusieurs événements restent une seule journée avec feu.
- **Jour sans feu observé :** zéro événement sur une journée dont la couverture de collecte est établie. Sans preuve de couverture, le statut reste inconnu.
- **Danger :** faible, modéré, élevé, très élevé. Le codage analytique ordinal proposé 1 à 4 doit être rapproché du codage effectif de S2.
- **Jour activé :** jour où le niveau est supérieur ou égal au seuil testé. Il s'agit d'une règle simulée, pas de la règle actuelle du SDIS.
- **Temps :** distinguer date d'émission, date de validité et échéance météo. Documenter le fuseau des horodatages ; retenir Europe/Paris pour l'agrégation locale après conversion justifiée.
- **Géographie :** conserver les codes administratifs sous forme de texte et leur millésime. Une valeur départementale ne devient pas une mesure communale par simple duplication.

**Deux grains analytiques sont nécessaires :** commune × année pour Q1 si les données le permettent ; département × jour pour Q2–Q3. Q4 réutilise ces grains sur des fenêtres comparables. Les interventions et engagements de ressources restent à leur grain propre pour Q5–Q6.

### Chaîne de transformation proposée

1. Conserver chaque extraction brute, sa date, son URL, sa licence et son empreinte.
2. Décrire les colonnes et mesurer la couverture réelle avant toute jointure.
3. Normaliser les dates, unités et codes sans effacer les valeurs d'origine.
4. Dédupliquer selon une clé documentée ; isoler les cas ambigus.
5. Agréger les événements au département × jour avant de les joindre à la météo.
6. Construire un calendrier des jours attendus et qualifier les manques.
7. Produire les indicateurs seulement sur les fenêtres admissibles et publier les exclusions.

La jointure météo doit avoir au plus une ligne par département, date de validité et échéance retenue. Sinon, elle peut multiplier artificiellement le nombre de feux.

## 5. Indicateurs et formules proposées

Soit D l'ensemble des journées d'un territoire sur la période commune avec couverture incendie et météo jugée exploitable. Pour chaque jour j, F(j) vaut 1 s'il existe au moins un feu retenu, sinon 0 ; L(j) est le niveau de danger. Un jour non couvert n'entre pas dans D et son exclusion est comptabilisée.

| Indicateur | Définition de calcul | Précaution |
|---|---|---|
| Q1 — fréquence annuelle normalisée | Nombre d'événements distincts / nombre d'années complètes observées / surface forestière en km² | Exprimer en feux par km² forestier et par an ; surface nulle ou inconnue : non calculable ; publier aussi les volumes |
| Q2 — couverture au seuil s | Nombre de jours de D avec F=1 et L≥s / nombre de jours de D avec F=1 | Dénominateur nul : non calculable ; ne pas confondre jours avec feu et nombre de feux |
| Q2 — jours manqués | Nombre de jours de D avec F=1 et L<s | Présenter le volume en plus du pourcentage |
| Q3 — jours activés | Nombre de jours météo valides avec L≥s | Annoncer la fenêtre météo ; pour le comparer à Q2, recalculer sur D |
| Q3 — activation sans feu observé | Nombre de jours de D avec F=0 et L≥s | Ne prouve pas l'inutilité du renforcement |
| Q3 — coût simulé | Somme des coûts supplémentaires des ressources mobilisées sur les jours activés | Sans coûts documentés : publier les jours, pas un montant inventé |
| Q4 — stabilité | Recalcul des indicateurs par saison et territoire sur un périmètre homogène | Afficher effectifs et exclusions ; historique court : conclusion limitée |
| Q5 — délai de première arrivée | Horodatage de première arrivée − horodatage d'alerte | Définition à confirmer ; médiane et P90 si effectif suffisant ; objectif de délai non inventé |
| Q6 — déficit de moyens | Maximum de 0 et de la différence besoin du scénario − ressources effectivement disponibles | Calcul par compétence et type d'engin ; éviter le double comptage d'une ressource |

Comparer les seuils 1 à 4 comme scénarios analytiques, sans recommander arbitrairement un taux de couverture « acceptable ». Ce taux et les contraintes budgétaires devront être explicités par le cas pédagogique ou les interlocuteurs.

**Point de vigilance sur 2022 :** l'année peut documenter Q1 et les séries historiques d'incendies si disponibles. Elle ne peut pas évaluer un seuil météo avec les seules archives annoncées depuis 2024. L'analyse avec/sans 2022 concerne donc uniquement les séries qui la couvrent.

**Point de vigilance sur la simultanéité :** plusieurs départs dans une journée mesurent une multiplicité journalière. La simultanéité nécessite des intervalles d'engagement qui se chevauchent ; dates seules insuffisantes. Sans ces intervalles, Q6 reste un scénario, pas une mesure de saturation observée.

## 6. Qualité, conformité et traçabilité

| Contrôle | Règle proposée | Traitement d'une anomalie |
|---|---|---|
| Unicité | Identifiant événement unique dans sa source ; clé météo unique après sélection d'échéance | Mettre en quarantaine, analyser avant agrégation |
| Complétude | Date, territoire et niveau requis pour le rapprochement | Exclure du calcul concerné, publier nombre et motif |
| Validité | Dates interprétables, niveaux appartenant au domaine documenté, surfaces non négatives | Conserver l'original et signaler l'erreur |
| Intégrité géographique | Codes raccordés au référentiel et millésime | Table de correspondance traçable ou statut non rapproché |
| Cohérence temporelle | Arrivée ≥ alerte ; fin ≥ début après gestion justifiée du fuseau | Ne pas corriger silencieusement |
| Jointure | Comparer effectifs avant/après et vérifier la cardinalité | Bloquer la publication si multiplication inexpliquée |
| Couverture | Écart entre calendrier attendu et jours réellement renseignés | Distinguer zéro, inconnu et hors saison |
| Reproductibilité | Version du traitement et empreinte de l'extraction enregistrées | Refaire un chargement sur la même entrée et comparer les sorties |

Aucun seuil de tolérance statistique n'est présenté comme validé. Les clés ambiguës, licences inconnues et incompatibilités de grain doivent être résolues avant utilisation du jeu concerné.

Pour chaque source, renseigner producteur ou diffuseur, URL de ressource, date d'accès, licence, période réellement constatée, champs utilisés, transformations et responsable de la revue. Les licences affichées pour S1 et S2 doivent être vérifiées au niveau des ressources réutilisées ; la licence MIT du code du dépôt ne remplace pas la licence des données.

Pour d'éventuels fichiers SDIS, demander les seules variables utiles, privilégier les effectifs agrégés et exclure noms, contacts et identifiants personnels du dépôt public. Examiner avec le détenteur les conditions d'accès et de diffusion avant intégration. Les captures, exports et liens ne doivent contenir ni secret ni donnée opérationnelle confidentielle.

## 7. Organisation et livrables attendus

| Responsable selon le cadrage | Production attendue | Dépendance |
|---|---|---|
| Steve — coordination | Assemblage, suivi et revue des arbitrages | Retours du groupe et consignes pédagogiques |
| Maeva — sources | Fiches documentaires puis inventaire des ressources réellement ouvertes | Accès et métadonnées producteurs |
| Chantal — qualité et conformité | Glossaire, contrôles, licences et registre des limites | Schémas réels et définitions des producteurs |
| Stéphane — pipelines | Ingestion, transformations, tests et historique des chargements | Sources admissibles |
| Ludovic — modèle décisionnel | Schéma, mesures et scénarios | Grain et couverture confirmés |

Cette répartition rappelle les rôles existants ; elle ne déclare pas ces travaux terminés. Le schéma en étoile détaillé et le choix technique seront proposés après inspection des colonnes ; aucune colonne source inexistante ne doit être supposée.

### Suivi documentaire après revue

La revue du coordinateur, transmise par Chantal le 17 novembre, est favorable sous réserve de C1–C3. La provenance est explicitée, l'arborescence est complétée et les statuts restent provisoires. La correction documentaire ne clôt pas les vérifications de données. Voir le [plan de suivi A1–A4](../suivi/actions-faisabilite.md).

| Question | Données vérifiées disponibles | Données encore non vérifiées | Repli proposé, à arbitrer par le groupe | Limites |
|---|---|---|---|---|
| Q5 | Aucune dans cette contribution | Alerte, arrivée, localisation, centres, effectifs et objectif opérationnel | Si accès insuffisant : scénario pédagogique explicitement simulé, ou indicateur non calculable | Aucun délai cible inventé ; un refus d'accès n'est pas établi |
| Q6 | Aucune dans cette contribution | Dates des feux, intervalles d'engagement, disponibilités, compétences, engins et coûts | Si accès insuffisant : scénario de charge explicitement simulé, ou indicateur non calculable | Dates seules insuffisantes pour mesurer une simultanéité ; aucun budget inventé |

Aucune simulation n'est déclarée autorisée par défaut ni réalisée. Les hypothèses et leur éventuelle validation seront consignées au journal.

### Critères de relecture de la v1

- [x] Relier Q1 à Q6 à une décision et à des données nécessaires.
- [x] Séparer contexte, constats documentaires, hypothèses et résultats à produire.
- [x] Décrire les grains, formules, règles qualité et conditions de non-calcul.
- [x] Signaler l'incertitude du chevauchement BDIFF/météo et la limite de Q6.
- [ ] Ouvrir les fichiers métier, établir leurs schémas et leur couverture réelle.
- [ ] Confirmer la période commune et la version de la prévision météo.
- [ ] Documenter les ressources géographiques et forestières.
- [ ] Statuer sur la faisabilité de Q5–Q6 et les hypothèses de coûts.
- [ ] Faire relire la v1 par le groupe et la confronter au barème pédagogique.

## 8. Bilan du rendu

La v1 définit une méthode vérifiable et les conditions de calcul. **Aucun classement communal, taux de couverture, seuil optimal, montant ou déficit opérationnel n'est encore calculé.** Le prochain jalon décisif consiste à ouvrir les ressources et à vérifier leur compatibilité temporelle. En cas d'absence de chevauchement, conserver l'analyse séparée des incendies et de la météo et déclarer les indicateurs croisés non calculables.

## 9. Références et documents liés

Références externes S1 à S4 : liens en section 3, consultés le 17 novembre 2026. La consultation des pages n'atteste pas une validation des fichiers bruts.

- [Analyse de la commande — Chantal](../analyse/commande-chantal-camara.md).
- [Questions collectives](../collectif/questions-retenues-proposition.md).
- [Inventaire des sources](../sources/inventaire.md).
- [Matrice questions × sources](../sources/matrice.md).
- [Glossaire](../glossaire.md).
- [Journal des décisions](../decisions/journal.md).
