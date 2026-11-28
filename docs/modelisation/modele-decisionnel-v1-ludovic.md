# Proposition de modèle décisionnel V1 — ticket #6

**Auteur :** Ludovic Tuekam — référent modèle décisionnel  
**Statut :** proposition de conception à relire par l'équipe ; non approuvée et non destinée à une mise en production.  
**Périmètre :** questions Q1 à Q6 du cas pédagogique SDIS 31, avec comparaison Occitanie lorsque les sources le permettent.  
**Dépendances :** spécification V1, README, glossaire, fiches BDIFF et Météo des forêts, résultats Q2–Q3 et PR #3.

## 1. Principes de modélisation

1. Définir le grain avant les clés, les relations et les mesures.
2. Séparer les faits incendie, prévision, surface forestière, intervention et engagement de moyens : ils n'ont pas le même grain.
3. Conserver les dates de référence, dates de validité et échéances météo comme des notions distinctes.
4. Conserver les extractions et leurs empreintes ; une correction de source ne doit pas écraser l'historique.
5. Ne pas joindre deux tables de faits directement sans passer par des dimensions conformes et sans vérifier la cardinalité.
6. Ne jamais dupliquer une prévision départementale sur les communes du département.
7. Distinguer zéro, absence d'observation, donnée inconnue et donnée hors période de publication.
8. Ne pas déclarer les données Q5–Q6 disponibles tant que l'accès aux sources opérationnelles SDIS n'est pas établi.

## 2. UML conceptuel

Le diagramme représente les objets métier et les liens candidats. Les liens en pointillés restent des hypothèses tant qu'une clé commune n'a pas été vérifiée.

~~~mermaid
classDiagram
 direction LR
 class Source {
  +id_source
  +producteur
  +diffuseur
  +licence
  +url_catalogue
 }
 class Extraction {
  +id_extraction
  +date_collecte_utc
  +empreinte_sha256
  +url_ressource
  +statut_validation
 }
 class Departement {
  +code_departement
  +libelle
  +millesime
 }
 class Commune {
  +code_insee
  +libelle
  +millesime_cog
  +date_debut_validite
  +date_fin_validite
 }
 class Jour {
  +date_civile
  +annee
  +mois
  +saison
 }
 class Incendie {
  +id_incendie_source
  +date_premiere_alerte
  +surface_parcourue_m2
  +type_feu
 }
 class PrevisionDanger {
  +date_reference_source
  +date_validite
  +echeance
  +niveau_danger
 }
 class SurfaceForet {
  +surface_forestiere_km2
  +millesime
  +source_mesure
 }
 class Intervention {
  +id_intervention
  +date_alerte
  +date_premiere_arrivee
  +centre
 }
 class Engagement {
  +id_engagement
  +type_engin
  +competence
  +debut_engagement
  +fin_engagement
 }
 class Scenario {
  +id_scenario
  +seuil
  +horizon
  +version_regle
 }
 Source "1" --> "0..*" Extraction : publie
 Extraction "1" --> "0..*" Incendie : trace
 Extraction "1" --> "0..*" PrevisionDanger : trace
 Departement "1" --> "0..*" Commune : contient
 Departement "1" --> "0..*" PrevisionDanger : niveau departemental
 Departement "1" --> "0..*" Incendie : localisation agregee
 Commune "1" --> "0..*" Incendie : localisation source
 Commune "1" --> "0..*" SurfaceForet : mesure
 Jour "1" --> "0..*" Incendie : date alerte
 Jour "1" --> "0..*" PrevisionDanger : date validite
 Incendie "0..*" ..> "0..*" Intervention : lien a confirmer
 Intervention "1" --> "0..*" Engagement : mobilise
 Scenario "1" --> "0..*" PrevisionDanger : applique regle
~~~

**Règle de prudence :** l'association Incendie–Intervention n'est pas une relation acquise. Elle nécessite un identifiant commun vérifié ou une méthode de rapprochement géotemporel approuvée et auditée. Une simple proximité de dates et de communes ne suffit pas à affirmer qu'une intervention correspond à un feu.

## 3. Flux brut → transformation → décision

~~~mermaid
flowchart TD
 A[Sources publiques et sources SDIS autorisees] --> B[Extraction versionnee]
 B --> C[Manifestes : URL, date, licence, SHA-256]
 C --> D[Profilage : schema, grain, periode, couverture]
 D --> E{Qualite et cles admissibles ?}
 E -- Non --> F[Quarantaine ou indicateur non calculable]
 E -- Oui --> G[Normalisation des dates et codes]
 G --> H[Dedoublonnage selon identifiants documentes]
 H --> I[Agregation au grain cible]
 I --> J[Tests de cardinalite et de non-multiplication]
 J --> K[Tables de faits historisees et dimensions conformes]
 K --> L[Calculs Q1 a Q6 et scenarios]
 L --> M[Restitution avec denominateurs, exclusions et limites]
 F --> M
~~~

Une jointure n'est publiée que si le grain, les clés, la cardinalité attendue, les doublons et les non-raccordés sont documentés.

## 4. Schéma décisionnel — constellation de faits

Le modèle est une constellation : plusieurs tables de faits partagent les mêmes dimensions conformes.

~~~mermaid
erDiagram
 DIM_DEPARTEMENT ||--o{ F_PREVISION_DANGER : departement
 DIM_DATE ||--o{ F_PREVISION_DANGER : validite
 DIM_DATE ||--o{ F_PREVISION_DANGER : reference
 DIM_ECHEANCE ||--o{ F_PREVISION_DANGER : horizon
 DIM_EXTRACTION ||--o{ F_PREVISION_DANGER : provenance

 DIM_DEPARTEMENT ||--o{ F_JOUR_FEU : departement
 DIM_DATE ||--o{ F_JOUR_FEU : jour_feu
 DIM_EXTRACTION ||--o{ F_JOUR_FEU : provenance

 DIM_COMMUNE ||--o{ F_FEU_ANNEE : commune
 DIM_ANNEE ||--o{ F_FEU_ANNEE : annee
 DIM_EXTRACTION ||--o{ F_FEU_ANNEE : provenance

 DIM_COMMUNE ||--o{ F_SURFACE_FORET : commune
 DIM_ANNEE ||--o{ F_SURFACE_FORET : millesime
 DIM_EXTRACTION ||--o{ F_SURFACE_FORET : provenance

 DIM_DEPARTEMENT ||--o{ F_SCENARIO_SURVEILLANCE : departement
 DIM_DATE ||--o{ F_SCENARIO_SURVEILLANCE : validite
 DIM_ECHEANCE ||--o{ F_SCENARIO_SURVEILLANCE : horizon
 DIM_SCENARIO ||--o{ F_SCENARIO_SURVEILLANCE : scenario

 DIM_CENTRE ||--o{ F_INTERVENTION : centre
 DIM_DATE ||--o{ F_INTERVENTION : alerte
 DIM_DATE ||--o{ F_INTERVENTION : arrivee

 DIM_INTERVENTION ||--o{ F_ENGAGEMENT : intervention
 DIM_RESSOURCE ||--o{ F_ENGAGEMENT : ressource
 DIM_DATE ||--o{ F_ENGAGEMENT : debut
 DIM_DATE ||--o{ F_ENGAGEMENT : fin
~~~

### 4.1 Dimensions conformes

| Dimension | Clé technique | Attributs utiles | Historisation |
|---|---|---|---|
| DIM_DATE | date_key | date civile, année, mois, jour, saison | Calendrier stable ; rôle joué pour validité, référence, alerte, arrivée, début et fin |
| DIM_ANNEE | annee_key | année civile, année de campagne | Une ligne par année |
| DIM_DEPARTEMENT | departement_key | code département en texte, libellé, millésime | SCD2 si les attributs territoriaux évoluent |
| DIM_COMMUNE | commune_key | code INSEE en texte, libellé, département, millésime COG, validité | SCD2 ; ne pas fusionner deux millésimes sans table de correspondance |
| DIM_ECHEANCE | echeance_key | J+1 ou J+2, décalage en jours | Dimension statique |
| DIM_EXTRACTION | extraction_key | source, URL, date de collecte, SHA-256, statut TLS, version du traitement | Append-only ; une extraction n'est jamais écrasée |
| DIM_SCENARIO | scenario_key | seuil, horizon, version de règle, hypothèse, statut de validation | Nouvelle version à chaque changement de règle |
| DIM_CENTRE | centre_key | identifiant et libellé du centre, secteur | À construire uniquement avec une source SDIS autorisée |
| DIM_RESSOURCE | ressource_key | identifiant pseudonymisé, type d'engin, compétence, capacité | Historisation des changements de disponibilité et de caractéristiques |
| DIM_INTERVENTION | intervention_key | identifiant opérationnel, type, statut | À construire uniquement si les données sont accessibles et diffusable |

Les codes département et commune restent des chaînes : les zéros initiaux ne doivent jamais disparaître. Pour les communes, le code INSEE seul n'est pas toujours une clé historique suffisante ; le millésime COG et les dates de validité sont conservés.

### 4.2 Tables de faits et grains

| Fait | Grain exact — une ligne représente | Mesures principales | Questions |
|---|---|---|---|
| F_PREVISION_DANGER | Département × date de validité × échéance × date de référence / extraction | niveau de danger, indicateur de validité | Q2, Q3, Q4 |
| F_JOUR_FEU | Département × date de première alerte locale | nombre de feux type F distincts, indicateur jour avec feu, statut de couverture BDIFF | Q2, Q3, Q4 |
| F_FEU_ANNEE | Commune × année × extraction BDIFF | nombre de feux distincts, surfaces parcourues agrégées si pertinentes | Q1, Q4 |
| F_SURFACE_FORET | Commune × millésime forestier × source / extraction | surface forestière en km², statut de mesure | Q1, Q4 |
| F_SCENARIO_SURVEILLANCE | Département × date de validité × échéance × seuil × version de scénario | jour activé, jour avec feu couvert, jour activé sans feu observé | Q2, Q3, Q4 |
| F_INTERVENTION | Une intervention opérationnelle identifiée | délai alerte-arrivée, statut, secteur | Q5 |
| F_ENGAGEMENT | Une ressource engagée sur un intervalle d'intervention | début, fin, durée, type de moyen, compétence | Q6 |

**Point d'attention sur la prévision historisée :** la date de validité ne suffit pas à identifier une prévision. Il faut conserver la date de référence (heure de production) et l'extraction. Deux prévisions successives peuvent viser le même jour de validité ; elles ne doivent pas être fusionnées ou écrasées.

**Point d'attention sur l'incendie :** plusieurs événements le même jour dans un département donnent plusieurs incendies dans F_FEU_ANNEE, mais une seule journée avec feu dans F_JOUR_FEU. Ces mesures ne sont pas interchangeables.

### 4.3 Historisation

- **Sources et extractions :** conserver chaque extraction avec URL, horodatage, licence, empreinte SHA-256, résultat des contrôles et version du script.
- **Prévisions :** conserver les versions successives ; clé métier candidate = département + date de validité + échéance + date de référence. Une correction de prévision crée une nouvelle observation.
- **BDIFF :** conserver l'identifiant source de l'incendie et l'identifiant d'extraction. Une mise à jour de la base ne doit pas effacer l'état antérieur.
- **Communes :** historiser les libellés, rattachements et codes selon les millésimes COG (SCD type 2).
- **Surfaces forestières :** conserver le millésime et la source de mesure ; une surface inconnue n'est jamais remplacée par zéro.
- **Scénarios :** versionner le seuil, l'horizon et la règle ; un résultat ancien doit rester reproductible avec la version de scénario qui l'a produit.
- **Interventions et engagements :** conserver les horodatages originaux, le fuseau, les corrections et les statuts de qualité ; aucune donnée personnelle inutile dans le modèle analytique.

## 5. Registre des jointures

| Jointure candidate | Clés et cardinalité attendue | Statut observé | Risque principal | Contrôle obligatoire |
|---|---|---|---|---|
| Incendie → F_JOUR_FEU | département + date ; plusieurs incendies vers un jour (N:1) | Testé dans le script BDIFF : identifiants d'événements contrôlés puis agrégation département-jour | Compter les feux comme des journées | Comparer nombre d'événements et nombre de clés distinctes |
| F_JOUR_FEU → F_PREVISION_DANGER J+1 | département + date de validité + horizon J+1 + version de prévision ; au plus 1 prévision par clé sélectionnée | Test technique disponible ; alias date / Reference_time encore à confirmer | Décalage de date, doublons, mauvaise version | Vérifier la clé unique, la période et le nombre de non-raccordés |
| F_JOUR_FEU → F_PREVISION_DANGER J+2 | mêmes clés avec horizon J+2 | Test technique disponible ; alias date / Reference_time encore à confirmer | Mélanger J+1 et J+2 | Calculer séparément les ensembles puis leur intersection réelle |
| J+1 ↔ J+2 | département + date de validité | Intersection à documenter par le rapport d'audit dédié | Déduire l'intersection du minimum des effectifs | Publier A, B, A∩B, A privé de B et B privé de A |
| Commune → département | code département + millésime COG ; N:1 | À vérifier avec le référentiel INSEE | Mauvais rattachement historique | Contrôler les codes orphelins et les changements de communes |
| F_FEU_ANNEE → F_SURFACE_FORET | commune + année / millésime compatible ; 1:1 après contrôle | À vérifier ; source IGN et COG non profilées dans ce lot | Multiplier les feux ou utiliser une surface non comparable | Unicité commune-millésime, couverture et unité km² |
| F_INTERVENTION → incendie | identifiant source commun ; cardinalité à déterminer | Bloqué : identifiant commun non établi | Faux rapprochement d'une intervention à un feu | Ne pas joindre avant preuve d'identifiant ou protocole validé |
| F_ENGAGEMENT → intervention | identifiant intervention ; 1:N attendu | Non testé : données SDIS non accessibles/confirmées | Double compte des moyens et chevauchements d'intervalles | Unicité, intervalles, fuseau, ressources simultanément indisponibles |

### 5.1 Règles anti-duplication

1. Agréger les événements BDIFF au département × jour avant la jointure météo.
2. Vérifier l'unicité de la prévision par département × validité × échéance × référence retenue.
3. Sélectionner une échéance déterminée par le scénario ; ne pas choisir a posteriori J+1 ou J+2 selon le résultat le plus favorable.
4. Pour une comparaison commune, calculer explicitement l'intersection des couples département-jour disposant des deux échéances.
5. Contrôler le nombre de lignes avant et après chaque jointure ; toute multiplication inexpliquée bloque le KPI.
6. Ne pas relier directement deux faits à des grains différents ; agréger d'abord au grain commun ou utiliser une table de correspondance validée.

## 6. Traçabilité des questions Q1–Q6

| Question | Faits et dimensions | Mesure / formule proposée | Source attendue | État et limite |
|---|---|---|---|---|
| Q1 — Où prioriser les secteurs ? | F_FEU_ANNEE, F_SURFACE_FORET, DIM_COMMUNE, DIM_ANNEE | Feux distincts / (surface forestière en km² × années complètes observées) ; publier aussi le nombre brut de feux | BDIFF + IGN + INSEE COG | BDIFF disponible ; surfaces IGN et COG à collecter/profiler |
| Q2 — Quel seuil couvre les jours avec feu ? | F_JOUR_FEU, F_PREVISION_DANGER, DIM_ECHEANCE, DIM_SCENARIO | Numérateur : jours avec feu et niveau de l'horizon choisi ≥ seuil ; dénominateur : jours avec feu de la cohorte admissible, en affichant sa taille | BDIFF + archives Météo des forêts | Résultats exploratoires ; sémantique de la colonne d'archive date à confirmer |
| Q3 — Combien de jours de surveillance ? | F_PREVISION_DANGER, F_SCENARIO_SURVEILLANCE | Nombre de département-jours avec niveau ≥ seuil ; distinguer les jours avec feu observé et sans feu observé | Archives Météo des forêts + BDIFF | Proxy en journées-département ; pas de coût financier ni de preuve d'inefficacité |
| Q4 — Les résultats sont-ils stables ? | Faits Q1–Q3 + dimensions date, territoire, extraction | Recalcul des mêmes mesures par année, saison et territoire sur une fenêtre commune ; publier effectifs et exclusions | BDIFF, Météo des forêts, IGN, INSEE | Comparabilité à établir par source et millésime |
| Q5 — Quels sont les délais de première intervention ? | F_INTERVENTION, DIM_CENTRE, DIM_DATE | Délai = première arrivée − alerte ; médiane et P90 sur les interventions ayant deux horodatages valides ; publier n | Données opérationnelles SDIS autorisées | Accès et définition des horodatages non confirmés |
| Q6 — Les moyens couvrent-ils plusieurs départs simultanés ? | F_ENGAGEMENT, DIM_RESSOURCE, DIM_INTERVENTION, DIM_DATE | Par intervalle : besoin simulé − ressources disponibles, plafonné à zéro ; distinguer engins et compétences | Disponibilités et engagements SDIS | Données non confirmées ; les dates d'incendie seules ne mesurent pas la simultanéité |

## 7. Définitions de cohortes et d'indicateurs Q2–Q3

Pour une année donnée, toutes les clés sont des couples (département, jour) :

- **E** : journées départementales avec au moins un feu BDIFF type F.
- **A** : clés de E pour lesquelles J+1 est disponible.
- **B** : clés de E pour lesquelles J+2 est disponible.
- **I = A ∩ B** : clés de E disposant simultanément des deux échéances.
- **Jours feu hors cohorte** : nombre de clés de E privées de I. C'est un volume ; il n'a pas de dénominateur.
- **Taux de jours feu hors cohorte** : nombre de clés de E privées de I / nombre de clés de E. Dénominateur : toutes les journées départementales avec feu BDIFF.
- **Taux de couverture de cohorte feu** : nombre de clés de I / nombre de clés de E. Il mesure la part des journées avec feu qui entrent dans la cohorte commune.
- **Couverture conditionnelle au seuil s et horizon h** : nombre de clés de I dont le niveau prévu à l'horizon h est supérieur ou égal à s / nombre de clés de I. Le dénominateur est la cohorte commune avec feu, identique pour comparer les seuils et les horizons.
- **Taux de disponibilité météo global** : nombre de couples département-jour attendus avec les deux échéances valides / nombre de couples département-jour où la publication est attendue. Le calendrier attendu doit être défini à partir des règles officielles et de la période de publication ; il ne doit pas être remplacé par le seul intervalle min/max observé.

La définition complète et la preuve exécutable de A, B et A∩B sont publiées dans [l'audit d'intersection J+1/J+2](../resultats/intersection_j1_j2_feux.md), avec le détail des clés non communes dans le CSV associé.

## 8. Sources, statut et limites

| Source | Champs utiles observés / attendus | Usage | Limite à conserver |
|---|---|---|---|
| BDIFF officiel type F 2024–2025 | Année, Numéro, Département, Code INSEE, Date de première alerte, surfaces et dommages | Incendie, jour avec feu, Q1–Q4 | Manifeste : transport TLS initial non vérifié indépendamment |
| Météo des forêts 2024–2026 | Archive : date, num_dep, niveau_j1, niveau_j2, nom du département | Prévisions départementales, Q2–Q4 | La documentation producteur nomme Reference_time ; l'équivalence avec date reste à confirmer |
| INSEE COG | Codes, libellés, rattachements et millésimes | Conformation des communes et départements | Collecte officielle à finaliser |
| IGN | Surface forestière et millésime | Dénominateur Q1 | Ressource et méthode d'intersection géographique à profiler |
| SDIS 31 | Alertes, arrivées, interventions, centres, ressources et intervalles d'engagement | Q5–Q6 | Accès, autorisation, schéma et règles de diffusion non confirmés |

La documentation primaire Météo-France décrit une information départementale pour J+1 et J+2, diffusée à 17 h pendant la saison, et les niveaux 1 à 4. Elle précise aussi que le produit est destiné à la sensibilisation du public, et non à remplacer l'assistance opérationnelle spécialisée des SIS. Les scénarios Q2–Q3 restent donc pédagogiques.

Références : [documentation technique Météo-France — Météo des forêts](https://confluence-meteofrance.atlassian.net/wiki/spaces/OpenDataMeteoFrance/pages/874741792/Donn%2Bes%2Bexpertis%Bes) ; [explication Météo-France, mise à jour 23 juillet 2026](https://meteofrance.com/actualites/la-meteo-des-forets-sinformer-sur-le-danger-de-feux).

## 9. Checklist ticket #6

- [x] Diagramme conceptuel Mermaid et liens candidats.
- [x] Diagramme du flux brut → transformation → décision.
- [x] Constellation de faits et dimensions avec grains explicités.
- [x] Historisation des sources, extractions, prévisions, territoires et scénarios.
- [x] Registre des jointures, cardinalités attendues, statuts et risques.
- [x] Traçabilité Q1–Q6 vers faits, mesures et sources.
- [ ] Faire relire les grains et cardinalités par Stéphane et Steve.
- [ ] Faire confirmer les définitions et les limites par Chantal.
- [ ] Finaliser les ressources INSEE/IGN et leur couverture.
- [ ] Confirmer l'accès et le schéma des données opérationnelles SDIS pour Q5–Q6.

**Aucune validation humaine n'est présumée.** Cette V1 est une proposition structurée à soumettre au groupe ; les points non vérifiés restent explicitement ouverts.
