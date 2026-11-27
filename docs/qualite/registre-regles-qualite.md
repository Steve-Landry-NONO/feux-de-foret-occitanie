# Registre des règles qualité et conformité — v0

**Ticket :** #14 · **Référente :** Chantal CAMARA · **Version :** v0 du 26/11/2026 · **Statut :** proposition à relire, non validée par l'équipe.

**Provenance :** registre préparé avec l'assistance de Claude à partir de la [spécification v1](../specification/specification-v1-2026-11-17.md) (§ 4 et § 6) et des fichiers Météo des forêts de la PR #3. Les résultats « MDF » proviennent d'une exécution réelle de `scripts/controler_qualite_mdf.py` le 26/11/2026 ; ils sont à réexécuter par Chantal avant validation. Aucun seuil n'est validé tant qu'il n'est pas tracé dans le [journal des décisions](../decisions/journal.md).

## Conventions

- **Criticité :** *Bloquante* (arrêt du calcul concerné) · *Majeure* (calcul possible, limite publiée) · *Information* (suivi).
- **Statut :** *Proposée* · *Exécutée* (test lancé, résultat consigné) · *Validée* (revue humaine et décision au journal) · *Non exécutée*.
- Toujours distinguer **zéro**, **valeur nulle** et **absence de donnée** ; contrôler la **population** (lignes attendues), pas seulement les colonnes.

## A. Archives Météo des forêts (S2) — fichiers `mdf_2024` à `mdf_2026` de la PR #3

| ID | Colonne / population | Dimension | Règle | Justification métier | Méthode | Seuil | Criticité | Action si échec | Résultat observé (26/11/2026) | Statut | Preuve |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MDF-01 | En-têtes | Validité du schéma | Colonnes `date, num_dep, niveau_j1, niveau_j2, nom_dep` présentes, alias documentés | Un schéma changeant casse silencieusement Q2–Q3 | Lecture de l'en-tête, alias `dep_nom → nom_dep` | 0 colonne manquante | Bloquante | Arrêt du chargement, mise à jour de l'alias documentée | 0 manquante ; **2025 utilise `dep_nom`** | Exécutée | Script, sortie JSON |
| MDF-02 | Fichier | Intégrité / traçabilité | SHA-256 identique au `manifest.json` de collecte | Garantir que l'analyse porte sur l'extraction tracée | `hashlib.sha256` | 100 % conforme si manifeste fourni ; empreinte absente = échec ; sans manifeste = non contrôlé | Bloquante | Refuser le fichier, nouvelle collecte datée | 3/3 conformes | Exécutée | Script, manifeste PR #3 |
| MDF-03 | `date` (lignes Occitanie) | Validité | Horodatage ISO 8601 interprétable | Rapprochement par jour impossible sinon | `datetime.fromisoformat` | 0 invalide | Bloquante | Quarantaine, ligne originale conservée | 0 invalide (3 années) | Exécutée | Script |
| MDF-04 | `num_dep × jour` | Unicité | Une seule ligne par département et par jour | Évite le double comptage des jours activés (Q3) | Comptage des clés | 0 doublon | Bloquante | Quarantaine avant agrégation | 0 doublon | Exécutée | Script |
| MDF-05 | `niveau_j1`, `niveau_j2` | Validité du domaine | Valeur dans {1, 2, 3, 4} ; vide compté à part | Le seuil d'activation repose sur ce codage | Comptage vides / hors domaine | 0 vide et 0 hors domaine | Bloquante | Signaler, exclure du calcul concerné | 0 vide, 0 hors domaine | Exécutée | Script (distributions en JSON) |
| MDF-06 | 13 départements × jour publié | Complétude de population | Chaque jour publié couvre les 13 départements d'Occitanie | Un département manquant fausserait les comparaisons Q4 | Ensemble des codes par jour | Population non vide et au moins un jour valide (bloquant) ; 13/13 chaque jour (majeur) | Mixte | Publier les jours incomplets, statut « inconnu » | 120, 120 et 131 jours, tous complets | Exécutée | Script |
| MDF-07 | Calendrier publié | Continuité interne | Aucun jour absent entre la première et la dernière date **présentes dans le fichier** | Un trou interne fausserait le comptage des jours activés | Comparaison au calendrier continu min–max | 0 jour absent | Majeure | Lister les jours, ne pas imputer | 0 absent. Bornes observées : 03/06–30/09 (2024, 2025), 28/05–05/10 (2026) | Exécutée | Script |
| MDF-12 | Période d'étude attendue | Couverture réelle | Comparer les bornes publiées à la période d'étude décidée (A3) : jours hors saison = **absence de publication**, ni zéro ni danger faible | MDF-06 et MDF-07 ne prouvent pas la couverture d'une année entière ni d'une saison de feux | Bornes observées comparées aux bornes attendues | Période attendue à décider | Bloquante pour Q3–Q4 | Statut « non couvert » ; pas d'extrapolation | Couverture limitée à environ 4 mois par an ; 2024 démarre le 03/06 ; bornes variables selon l'année | Non exécutée (période A3 non décidée) | — |
| MDF-08 | `num_dep` | Cohérence de format | Codes département en texte sur 2 caractères | Jointure INSEE/BDIFF fausse si `9 ≠ 09` | Comptage des codes à 1 chiffre | Normalisation `zfill(2)` documentée | Majeure | Normaliser à l'ingestion, tracer la transformation | **1 080 codes sans zéro initial en 2024 et 2025**, 0 en 2026 | Exécutée | Script |
| MDF-09 | `date` | Exactitude temporelle | Une seule heure de publication par jour | Prérequis à la sémantique J+1/J+2 | Heures distinctes par jour | Information | Information | Remonter au producteur | 0 jour à horodatages multiples | Exécutée | Script |
| MDF-10 | `date`, `niveau_j1/j2` | Exactitude / sémantique | Confirmer si `date` est la date d'émission et à quel jour s'applique J1 | Sans cela, la jointure « même date » avec les feux est fausse | Documentation producteur | Confirmation écrite | Bloquante pour Q2 | Pas de KPI croisé publié | Non confirmé | Non exécutée | — |
| MDF-11 | Séparateur CSV | Cohérence de format | Séparateur détecté et tracé par fichier | Un parseur figé sur « , » lit 2026 en une seule colonne | Détection sur l'en-tête | Détection automatique | Majeure | Parseur adaptatif, test dédié | **« , » en 2024–2025, « ; » en 2026** | Exécutée | Script |

## B. Incendies BDIFF (S1), référentiels et jointures — à exécuter

| ID | Population | Dimension | Règle | Seuil proposé | Criticité | Action si échec | Statut |
|---|---|---|---|---|---|---|---|
| BDF-01 | Événements | Unicité | Identifiant d'événement unique dans sa source | 0 doublon | Bloquante | Quarantaine, analyse avant agrégation | Non exécutée |
| BDF-02 | Date, commune, surface | Complétude des valeurs | Date et territoire présents pour tout événement retenu | Taux publié ; seuil à décider en équipe | Majeure | Exclusion du calcul, motif et nombre publiés | Non exécutée |
| BDF-03 | Surface | Validité | Surface ≥ 0, unité documentée | 0 valeur négative | Bloquante | Signaler, original conservé | Non exécutée |
| BDF-04 | Années | Couverture | Années réellement présentes rapprochées de la couverture affichée | Écart documenté | Majeure | Mise à jour de l'inventaire | Non exécutée (#5) |
| REF-01 | Codes commune / département | Intégrité référentielle | 100 % des codes raccordés au COG INSEE du millésime retenu | 100 % ou table de correspondance | Bloquante | Statut « non rapproché » | Non exécutée (#8) |
| JNT-01 | Jointure feux × météo | Cardinalité | Effectifs avant/après identiques ; pas de multiplication | Écart = 0 | Bloquante | Bloquer la publication | Non exécutée |
| JNT-02 | Département × jour | Cohérence entre sources | « Jour sans feu » seulement si la couverture de collecte est établie | Statut inconnu sinon | Majeure | Distinguer zéro et inconnu | Non exécutée |
| SDIS-01 | Interventions | Cohérence temporelle | Arrivée ≥ alerte ; fin ≥ début après gestion du fuseau | 0 incohérence non expliquée | Majeure | Ne pas corriger silencieusement | Non exécutée (accès non confirmé) |

## C. Conformité et gouvernance

| ID | Objet | Règle | Preuve attendue | Statut |
|---|---|---|---|---|
| CNF-01 | Licence S1, S2 | Licence vérifiée **au niveau de la ressource réutilisée**, attribution rédigée | URL de la ressource, date, mention d'attribution | Licence Ouverte 2.0 affichée au catalogue ; ressource non vérifiée |
| CNF-02 | Code vs données | La licence MIT du dépôt ne couvre pas les données | Mention dans le README des données | Proposée |
| CNF-03 | Données personnelles | Aucun nom, contact ou identifiant personnel dans le dépôt public | Revue des colonnes avant commit | MDF : aucune colonne personnelle constatée ; SDIS : à revoir |
| CNF-04 | Minimisation | Seules les variables utiles aux Q1–Q6 sont demandées et versionnées | Liste des champs justifiés par question | Proposée |
| CNF-05 | Traçabilité | Chaque transformation (alias, `zfill`, séparateur) est documentée et testée | Script, test, entrée au journal | Partielle : MDF-01, 08, 11 |
| CNF-06 | Données confidentielles | Pas de donnée opérationnelle SDIS ni de secret dans les captures et exports | Relecture de la PR | Proposée |

## Reproduire

```sh
python scripts/controler_qualite_mdf.py \
  datasets/public/meteo_des_forets/mdf_2024.csv.gz \
  datasets/public/meteo_des_forets/mdf_2025.csv.gz \
  datasets/public/meteo_des_forets/mdf_2026.csv.gz \
  --manifest datasets/public/meteo_des_forets/manifest.json
```

**Reproductibilité :**

- **Depuis la branche de contribution**, seuls les tests unitaires sont reproductibles : `python -m unittest discover -s tests -v`. Ils utilisent des fichiers synthétiques et vérifient le contrôle, pas les données.
- **Le contrôle sur les données réelles** (résultats MDF ci-dessus) n'est pas reproductible depuis `main`. Les fichiers `datasets/public/meteo_des_forets/` et `manifest.json` existent seulement dans la PR #3, non fusionnée. Pour le reproduire, récupérer la PR avec `git fetch origin pull/3/head:pr3`, puis extraire les fichiers sans changer de branche.
- **Code de sortie :** le script renvoie 1 si une règle bloquante échoue, 2 si le manifeste n'est pas fourni et aucun échec bloquant n'est détecté, 0 si les règles bloquantes exécutables sont conformes. Le JSON contient le SHA-256 calculé de chaque archive et le SHA du commit source fourni via `--commit-source`. Les résultats historiques ci-dessus restent à réexécuter avec cette version.

## Décisions demandées au chef de projet

1. Valider les criticités et les seuils proposés (aucun seuil statistique n'est fixé pour BDF-02).
2. Confirmer l'emplacement `docs/qualite/` et l'intégration du script dans la chaîne de la PR #3.
3. Désigner qui obtient la confirmation MDF-10 auprès de Météo-France.

## Vérification des corrections du 27/11/2026

Exécution locale : `python -m unittest discover -s tests -v` — 7 tests réussis, 0 échec, 0 erreur (0,006 s). Les empreintes Git des fichiers exécutés correspondent aux blobs publiés : script `431e055e9f7a3205dad847d2fa3fdcd075c24000`, tests `f92134b3cf28a32d99c6b5efade0475b75593dcf`. Cette vérification porte uniquement sur les tests synthétiques de la contribution ; les archives réelles restent à contrôler et la preuve JSON reste à produire.

## Qualification technique — 27/11/2026

La qualification est distincte de l'approbation collective. Une règle exécutée peut être CONFORME ou NON CONFORME ; NON CONTROLEE signifie que la preuve nécessaire manque. VALIDEE COLLECTIVEMENT exige une décision au journal. Aucun seuil proposé ci-dessous n'est déclaré approuvé.

| Règle | Résultat technique sur les trois archives | Validation collective |
|---|---|---|
| MDF-01, 02, 03, 04, 05 | Exécutées, conformes aux seuils proposés | En attente |
| MDF-06, 07 | Exécutées, conformes sur le calendrier publié uniquement | En attente |
| MDF-08 | Exécutée : écart de format en 2024–2025 (1080 codes par archive), normalisation proposée | En attente |
| MDF-09 | Exécutée, aucun jour à horodatages multiples | En attente |
| MDF-11 | Exécutée, séparateurs détectés ; alias 2025 documenté | En attente |
| MDF-10, 12 | Non contrôlées : sémantique et période attendue non établies | En attente |
| BDF, REF, JNT, SDIS | Non contrôlées dans cette qualification | En attente |

### Preuves et reproduction

- [Rapport JSON](preuve-controles-mdf.json), blob Git `07d2f844d568b97519737f22519d38521a23061c`, SHA-256 `78a09983cd494e049b415bd796c2370839c593f46d92cb845f779661f76934bf`.
- Source PR #3 : commit `479e5d91296a5994eaed304678504cdc05fb3a17`. Manifeste blob `d27b2ca388421077ddf613adbf47e2a782ba76a0`. Les archives du ZIP fourni ont été comparées aux blobs GitHub.
- Script : blob `431e055e9f7a3205dad847d2fa3fdcd075c24000`, commit fcbc22d.
- Tests : blobs `f92134b3cf28a32d99c6b5efade0475b75593dcf` et `5455aa1928a6bbf0968156ff1df6e0afca10a11f`.
- Exécution locale assistée le 27/11/2026 : 7 méthodes initiales réussies (0,008 s), puis 8 méthodes réussies (2,198 s), 0 erreur et 0 échec. Le test CLI vérifie les codes 0, 1, 2 et les statuts JSON correspondants.
- Contrôles réels : code retour 0, trois archives conformes aux règles bloquantes exécutables ; sortie identique octet pour octet au JSON versionné. Aucun jour absent dans les bornes publiées, ce qui ne démontre pas la couverture de la période d'étude.

Depuis la branche de contribution, récupérer les fichiers du commit source dans un répertoire séparé (sans fusion) :

```sh
git fetch origin refs/pull/3/head
git archive 479e5d91296a5994eaed304678504cdc05fb3a17 datasets/public/meteo_des_forets | tar -x -C /tmp
python -m unittest discover -s tests -v
python scripts/controler_qualite_mdf.py /tmp/datasets/public/meteo_des_forets/mdf_2024.csv.gz /tmp/datasets/public/meteo_des_forets/mdf_2025.csv.gz /tmp/datasets/public/meteo_des_forets/mdf_2026.csv.gz --manifest /tmp/datasets/public/meteo_des_forets/manifest.json --commit-source 479e5d91296a5994eaed304678504cdc05fb3a17 > /tmp/preuve-controles-mdf.json
```

### Suite proposée, sans chantier concurrent

| Périmètre | Contrôles à préparer | Coordination préalable |
|---|---|---|
| BDIFF (#4, #5) | SHA, grain, identifiant unique, dates, territoire, surface et unité, exhaustivité, valeurs nulles, licence de la ressource | Maeva fournit les extractions identifiées ; Stéphane confirme le grain et les transformations |
| Référentiels (#8) | Millésime COG, codes texte, unicité, correspondances historiques, couverture des clés et non-raccordés | Maeva confirme la source ; Stéphane fournit les clés du pipeline |
| Jointures (A1, A3) | Cardinalité avant/après, anti-jointures, chevauchement réel, échéance météo, distinction zéro/inconnu, absence de multiplication | Stéphane prépare les jeux intermédiaires ; Ludovic valide les besoins KPI ; Steve arbitre la période |
| Conformité | Licence au niveau ressource, attribution, minimisation et absence de données personnelles | Chantal prépare la revue sur les ressources confirmées |

Livrables attendus : manifeste et SHA source, règles et seuils proposés, tests synthétiques, rapport réel et limites, puis revue humaine. Ne pas lancer de pipeline parallèle ni modifier les branches des autres membres. Le #14 reste ouvert. Décisions attendues : seuils et criticités, A3, MDF-10, coordination des prochains contrôles.
