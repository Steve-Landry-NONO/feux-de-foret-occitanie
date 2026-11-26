# Prévenir et détecter les feux de forêt en Occitanie
### Aide à la décision pour le SDIS 31 — saison 2027

![Statut](https://img.shields.io/badge/Cadrage-valid%C3%A9-238636) ![Sources](https://img.shields.io/badge/Sources-%C3%A0_v%C3%A9rifier-orange) ![Projet](https://img.shields.io/badge/HETIC-MD5-blue)

> **Projet pédagogique HETIC — Mastère Data & IA, UE01 Stratégie Business Data-Driven (2026–2027).** Encadrement : Marine PROST. Le commanditaire est celui du cas pédagogique, la **direction du SDIS 31 (Haute-Garonne)** ; il ne s'agit pas d'une mission opérationnelle mandatée par le SDIS.

## Espaces de travail et suivi

| Espace | Accès | Utilisation |
|---|---|---|
| **GitHub** | [Dépôt du projet](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie) · [Issues](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/issues) · [Pull requests](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/pulls) | Code, documentation versionnée, tickets, revues et preuves de contribution |
| **Trello** | [Tableau de suivi HETIC UE01](https://trello.com/b/TqnYAupj/hetic-ue01-feux-de-for%C3%AAt-pilotage-%C3%A9quipe) | Répartition des tâches, jalons, blocages et avancement |
| **Google Drive du groupe** | [Dossier collaboratif MD5](https://drive.google.com/drive/folders/1SLx__GbAFq-2ZqFKY0MmccqqbGxK6tnG?usp=sharing) | Documents partagés, supports et éventuels fichiers de travail |

**Convention :** chaque carte technique Trello référence son Issue GitHub ; chaque PR référence l'Issue correspondante. Le dépôt reste la source de vérité pour le code et les livrables versionnés. Ne pas confondre le Drive pédagogique et le Drive collectif.

## Démarrage avec un assistant IA

Lire [AGENTS.md](AGENTS.md), le [guide de contribution](CONTRIBUTING.md), le [contexte projet](docs/pilotage/CONTEXTE.md), l’[état daté](docs/pilotage/PROJECT_STATUS.md), la [roadmap](docs/pilotage/ROADMAP.md) et les [prompts de démarrage](docs/accompagnement/README.md). Les tickets et PR en direct priment sur les instantanés. Onboarding : #19–#24.

## Sources de données et documentation externe

Les liens ci-dessous proviennent de l'[inventaire des sources](docs/sources/inventaire.md). **Ils désignent des sources candidates ou des pages de documentation, et non des jeux de données déjà validés ou profilés.**

| Source | Lien | Statut documentaire |
|---|---|---|
| BDIFF — incendies de forêts en France | [Fiche data.gouv.fr](https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff) | Métadonnées consultées ; fichiers, dates et grain à vérifier |
| Archives de la Météo des forêts | [Fiche data.gouv.fr](https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets/informations) | Métadonnées consultées ; couverture effective et schéma à vérifier |
| Météo des forêts — explication des niveaux | [Météo-France](https://meteofrance.com/meteo-des-forets) | Documentation méthodologique, pas table de faits |
| Contexte national des feux | [Notre Environnement](https://www.notre-environnement.gouv.fr/themes/risques/article/les-feux-de-forets) | Documentation de contexte |
| Référentiels INSEE, couverture IGN, moyens SDIS, Gaspar / Prométhée | [Inventaire et points à vérifier](docs/sources/inventaire.md) | URL exacte / accès / usage encore à identifier |

**Point bloquant prioritaire :** le chevauchement temporel entre les observations d'incendies et les archives météo reste à démontrer avant de calculer les indicateurs croisés. Voir [actions de faisabilité A1–A4](docs/suivi/actions-faisabilite.md) et [matrice questions × sources](docs/sources/matrice.md).

## Atelier KPI — 19 novembre 2026

**Équipe :** Steve Landry NONO, Maeva QUENUM, Chantal CAMARA, Stéphane DOMI et Ludovic TUEKAM. Aucun numéro de groupe n'est attribué dans les documents de référence ; les rendus sont identifiés par les membres.

- [Polycopié et atelier : dossier de travail A–F](docs/kpi/atelier-01-2026-11-19.md) — **propositions à valider, calculs réels non effectués**.
- [Journal des décisions](docs/decisions/journal.md) — trace de la séance et des points ouverts.
- [Dossier Drive de l'atelier](https://drive.google.com/drive/folders/1iMk2890zeldg9ekIcnssBmdgeEZ9YF-J) · [PDF de travail](https://drive.google.com/file/d/1j4hxjy7fNwOo7PNqR98vMszcQa1c3QMd/view?usp=drivesdk) · [Notebook de calcul](https://drive.google.com/file/d/1BLCglG8rLckMRBjhg0h9lfeXwXxPI6pb/view?usp=drivesdk) · [Cours](https://drive.google.com/file/d/18yw2Zou93xKSQ50-SXAaYbuRR_S_3-HL/view?usp=drivesdk) · [Énoncé](https://drive.google.com/file/d/1K7vTtiQt3VEOidCSQe_DkUXvmRlVzEm-/view?usp=drivesdk) · [Drive projet Feux de Forêt](https://drive.google.com/drive/folders/1hmXnuUVU_Uj0LLo5ZTkJaSwenAip6jI2).
- **À remettre le 19/11 :** `Atelier1_KPI_Equipe_Michel_Marine.pdf` et `Atelier1_calcul_Equipe_Michel_Marine.ipynb` (ou .xlsx), avec les noms des cinq membres. L'atelier est non noté mais doit être transmis même inachevé.

## Notre mission

La Haute-Garonne prépare la saison des feux de forêt 2027 avec un risque d'activité comparable ou supérieur à 2026. Le SDIS ne peut pas renforcer toutes les patrouilles partout, tout l'été. Il doit répondre à deux décisions :

1. **Où concentrer les moyens humains et financiers** pour prévenir et détecter les départs de feu ?
2. **À quel niveau de la Météo des forêts** déclencher une surveillance renforcée, compte tenu des journées avec et sans départ de feu ?

Notre approche complète ce cadrage par la **capacité réelle de réponse** : délais d'intervention, composition et disponibilité des équipes, engins, équipements et scénarios de départs simultanés. Les résultats devront être confrontés aux autres départements d'Occitanie et aux données nationales, lorsque les sources le permettent.

**Objectif :** transformer une commande opérationnelle en questions mesurables, données traçables, indicateurs explicables et recommandations argumentées. **Nous ne prétendons pas prédire individuellement chaque incendie.**

## Équipe et responsabilités — VALIDÉES

| Membre | Rôle confirmé | Responsabilités principales |
|---|---|---|
| **Steve Landry NONO** | Coordination / chef de projet | Planning, GitHub, tickets, points d'avancement, journal des décisions, cohérence des livrables |
| **Maeva QUENUM** | Référente sources | Recherche des producteurs, fiches d'identité, inventaire et matrice questions × sources |
| **Chantal CAMARA** | Référente qualité et conformité | Glossaire, définitions, contrôles qualité, licences, données personnelles et traçabilité |
| **Stéphane DOMI** | Référent pipelines | Collecte, ingestion, transformations, reproductibilité, tests et historisation |
| **Ludovic TUEKAM** | Référent modèle décisionnel | Modélisation, indicateurs, scénarios de seuil et restitution analytique |

**Règle d'équipe :** les rôles structurent la responsabilité, mais **les analyses, les revues et la qualité finale sont collectives**. Chaque étudiant contribue sous son propre compte GitHub.

## Questions décisionnelles — VALIDÉES POUR LE CADRAGE

| ID | Question | Décision visée |
|---|---|---|
| **Q1** | Quels secteurs présentent la plus forte fréquence de départs de feu, rapportée à l'exposition forestière ? | Prioriser les territoires |
| **Q2** | Quelle part des journées avec départ de feu serait couverte par chaque seuil de la Météo des forêts ? | Choisir le seuil d'activation |
| **Q3** | Combien de journées de surveillance renforcée chaque seuil imposerait-il ? | Arbitrer la mobilisation et le budget |
| **Q4** | Les résultats sont-ils stables dans le temps et comparables à ceux d'Occitanie et de France ? | Adapter ou généraliser la règle |
| **Q5** | Où les délais et capacités de première intervention sont-ils insuffisants ? | Prépositionner et renforcer les équipes |
| **Q6** | Quels effectifs, compétences et engins faut-il pour couvrir plusieurs départs simultanés ? | Dimensionner les renforts et le matériel |

Les questions sont **validées comme périmètre analytique**. Leur faisabilité, les seuils chiffrés et les recommandations dépendront des données réellement accessibles. Voir [l'argumentaire collectif](docs/collectif/questions-retenues-proposition.md).

## Méthode

```text
Commande du SDIS 31
       ↓
Décisions à éclairer (territoires, seuil, moyens)
       ↓
Questions analytiques Q1 à Q6
       ↓
Définitions et données idéales (grain, période, fraîcheur, géographie)
       ↓
Inventaire et fiches des sources réellement examinées
       ↓
Contrôles qualité, rapprochements et historisation
       ↓
Modèle décisionnel, indicateurs et scénarios
       ↓
Recommandations argumentées et limites
```

### Principes de rigueur
- **Danger météorologique ≠ départ de feu observé** : l'indice ne garantit ni l'occurrence ni l'absence d'un incendie.
- **Surveillance sans feu ≠ dépense inutile** : elle peut répondre à un risque réel.
- **Intervention ≠ événement incendie** : vérifier les identifiants, doublons et définitions.
- **Disponibilité supposée ≠ disponibilité prouvée** : les données opérationnelles SDIS peuvent être internes.
- **Comparaison territoriale** : vérifier les périodes, les grains, les référentiels et les dénominateurs (notamment la surface forestière).
- **Coût estimé ≠ coût constaté** : documenter les hypothèses de simulation.

## Structure du dépôt

```text
.
├── README.md
└── docs/
    ├── analyse/
    │   ├── commande-steve-landry-nono.md
    │   ├── commande-maeva-quenum.md
    │   ├── commande-chantal-camara.md
    │   ├── commande-stephane-domi.md
    │   └── commande-ludovic-tuekam.md
    ├── collectif/
    │   └── questions-retenues-proposition.md
    ├── specification/
    │   └── specification-v1-2026-11-17.md
    ├── suivi/
    │   └── actions-faisabilite.md
    ├── sources/
    │   ├── inventaire.md
    │   └── matrice.md
    ├── glossaire.md
    └── decisions/
        └── journal.md
```

**Rendu du 17 novembre :** [spécification v1](docs/specification/specification-v1-2026-11-17.md), proposée à la relecture collective. Elle détaille les indicateurs, grains, contrôles et limites ; aucun résultat chiffré n'est produit. La revue de métadonnées ne remplace pas l'examen des fichiers bruts. Les vérifications restantes sont planifiées dans le [suivi A1–A4](docs/suivi/actions-faisabilite.md).

**État documentaire :** les analyses sont les versions de référence du cadrage, attribuées nominativement à leurs responsables ; **elles ont été initialement préparées via le compte de coordination**. Chaque membre doit encore les relire, se les approprier et produire ses propres commits. Le [glossaire](docs/glossaire.md) est un référentiel de travail ; l'[inventaire](docs/sources/inventaire.md) et la [matrice](docs/sources/matrice.md) distinguent les **métadonnées consultées et les sources candidates** ; aucun fichier métier brut n'a encore été vérifié.

## Jalons pédagogiques

| Date | Attendu |
|---|---|
| **16/11/2026** | Analyses individuelles, fiches et inventaire des sources, glossaire initial (8 termes minimum), matrice initiale |
| **17/11/2026** | Spécification v1 en FOAD |
| **18/11/2026** | Remise de la spécification |
| **09/12/2026** | Entrepôt en étoile historisé et testé |
| **11/12/2026** | Entrepôt final et soutenance |

Ces dates sont les **échéances pédagogiques**, et non des preuves que chaque livrable est terminé.

## Contribuer

1. Accepter l'invitation GitHub et cloner le dépôt : `git clone https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie.git`.
2. Créer une branche par tâche : `git checkout -b docs/analyse-prenom`.
3. Modifier ses fichiers, citer ses sources et signaler ce qui reste à vérifier.
4. Commiter **depuis son propre compte**, avec un message explicite **en français** (ex. `docs(analyse): compléter mon analyse et justifier les données`).
5. Ouvrir une pull request, faire relire, puis fusionner après vérification.

**Convention de validation :** *validé pour le cadrage* signifie que le groupe a retenu un rôle, une question ou une structure de travail ; cela **ne signifie pas** que les données, les chiffres, les sources ou les contributions personnelles sont vérifiés. Les changements importants sont consignés dans le [journal des décisions](docs/decisions/journal.md).

## Références pédagogiques

- Marine PROST, **Exercice 1 — De la commande aux données — Occitanie**.
- **Template analyse de la commande**.
- **Exercice 2 — Fiche d'identité des sources**.
- **Le glossaire du projet**.
- Support de cours **UE01.A — C1 : Du besoin décisionnel à la cartographie des sources**.

---

*Projet étudiant — documents de cadrage validés, résultats et données à produire et vérifier.*
