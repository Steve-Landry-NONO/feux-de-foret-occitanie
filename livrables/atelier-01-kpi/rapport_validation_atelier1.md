# Validation de l’atelier KPI 1

**HETIC MD5 · séance du 19 novembre 2026 · Bilel Maïz.** Steve Landry NONO, Maeva QUENUM, Chantal CAMARA, Stéphane DOMI et Ludovic TUEKAM. Revue technique du 28 novembre 2026, avec assistance de Codex. La direction du SDIS 31 est le commanditaire pédagogique.

**Verdict · GO pour une remise pédagogique avec écarts déclarés.** Les trois fichiers documentent un calcul réel et reproductible. L’énoncé accepte une remise inachevée pour retour. La partie E reste partielle au regard des cinq années demandées et les hypothèses de sources appellent une revue humaine. Aucun envoi effectué. [Énoncé officiel](https://drive.google.com/file/d/1K7vTtiQt3VEOidCSQe_DkUXvmRlVzEm-/view)

| Partie | État de la revue |
|---|---|
| A | Décideur, options, question unique, objectif du défi, Haute-Garonne et saison 2027 présentés. La formulation de soutenance reste à relire par le groupe. |
| B | Dix candidats classés, test du doublement, tri motivé et critère RACER fragile des indicateurs retenus. |
| C | Trois questions GQM, arbre vectoriel à trois niveaux, contexte en pointillés, équations et influence des options. |
| D | Trois fiches, source et champs, valeurs, faisabilité, limites et propriétaire. Aucune cible opérationnelle fixée. |
| E | Jointures et sensibilités exécutées. Deux saisons compatibles pour le KPI principal, deux années civiles pour le diagnostic historique. Écart à l’exigence de cinq ans. |
| F | Biais de couverture et de maille, faibles dénominateurs, effets pervers, limites causales et garde-fous documentés. |

## Sources réellement utilisées

- **BDIFF**, portail du ministère de l’Agriculture / IGN. Les deux ZIP Occitanie type F contiennent 413 événements en 2024 et 472 en 2025. Les tailles, SHA-256, structures, critères d’export, dates d’alerte, clés et champs utiles sont contrôlés. Licence Ouverte 2.0 affichée au catalogue. Les deux annexes de mentions légales ont été consultées et n’apportent pas de licence distincte explicite. Le manifeste signale le transport initial sans certificat vérifié. Le point d’accès à l’export a renvoyé l’erreur TLS curl 60, code HTTP 000, lors du contrôle indépendant. La traçabilité locale reste distincte de la provenance par un nouveau téléchargement. [Catalogue BDIFF](https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff) · [Aide à l’export](https://bdiff.agriculture.gouv.fr/aide/recherche)
- **Archives de la Météo des forêts**, Météo-France, Licence Ouverte 2.0. SHA-256 et tailles conformes aux manifestes pour 2024–2026. Les empreintes des trois fichiers téléchargés ont déjà été rapprochées des copies du dépôt lors de la préparation. Le notebook contrôle les codes départementaux après normalisation et les niveaux entiers de 1 à 4. J+1 signifie lendemain et J+2 surlendemain. La colonne d’archive `date` est traitée comme date de référence sous réserve de corroboration avec `Reference_time`. [Catalogue Météo-France](https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets) · [Documentation des données expertisées](https://confluence-meteofrance.atlassian.net/wiki/spaces/OpenDataMeteoFrance/pages/874741792/)
- **Surface - commune**, INSEE/IGN, diffusion Ecolab. Licence Ouverte, identifiant catalogue `fr-lo`. Cliché au 1er janvier 2025 pour les deux années. `geocode_commune` est le code officiel géographique et `valeur` est exprimée en hectares. SHA-256 vérifié et fixé dans le notebook. [Fiche Surface](https://www.data.gouv.fr/datasets/surface) · [CSV utilisé](https://static.data.gouv.fr/resources/surface/20261126-125656/surface-commune.csv) · [Dictionnaire](https://static.data.gouv.fr/resources/surface/20261126-125717/description-des-champs.csv)

Énoncé et PDF initial lus sur Drive, notebook initial récupérable via Drive. Le travail initial prévoyait les jointures sans les exécuter. Le dossier de travail et les calculs exploratoires existants restent traçables dans Git au commit de base `7d55bb2`. Les noms de fichiers suivent le mandat, faute de numéro de groupe donné. L’énoncé utilise un préfixe de groupe. [PDF initial](https://drive.google.com/file/d/1j4hxjy7fNwOo7PNqR98vMszcQa1c3QMd/view) · [Notebook initial](https://drive.google.com/file/d/1BLCglG8rLckMRBjhg0h9lfeXwXxPI6pb/view) · [Cadrage du dépôt](../../docs/kpi/atelier-01-2026-11-19.md)

### Écart aux cinq années

L’API du catalogue météo recense trois fichiers annuels, 2024–2026, et trois ressources auxiliaires. Le fichier annuel 2023 testé à l’emplacement des autres millésimes renvoie HTTP 404. Le service commence en 2023. Même si un fonds complet 2023 est retrouvé, cinq saisons jusqu’à 2026 ne sont pas réalisables pour cet indicateur. Le dépôt présente deux exports BDIFF compatibles. L’archive météo 2026 figure dans les contrôles, hors jointure. Le catalogue BDIFF oriente vers le portail pour exporter les événements. Le défaut TLS empêche de vérifier et récupérer les exports 2021–2023 avec les mêmes filtres. Le repli superficie est donc calculé sur 2024–2025 uniquement et conserve une définition propre. [Dossier de lancement Météo-France](https://meteofrance.fr/sites/meteofrance.fr/files/files/editorial/Dossier_presse_Meteo_des_forets_2023_0.pdf)

## Résultats et contrôles

- **KPI principal.** Cohorte commune de 3 094 journées-départements en Occitanie, dont 119 par an dans le 31. En 2024, le seul feu du 31 est hors cohorte. En 2025, ≥3 J+1 couvre 2/4 jours avec feu pour 10/119 jours activés, soit 50 % de couverture et 8,40 % de charge. ≥2 couvre aussi 2/4 pour 51/119 jours activés. ≥4 couvre 0/4 pour 0/119 jour activé.
- **Sensibilité.** En J+2, la couverture reste 2/4 aux seuils ≥2 et ≥3 et la charge passe à 47 et 10 jours en 2025. Le seuil ≥4 reste à zéro. Au seuil ≥3 J+1, moyenne et médiane de charge valent 5,5 jours sur les deux saisons. Moyenne et médiane de couverture valent 50 % sur une seule année définie. Cette année, 2025, concentre 100 % des jours feu éligibles du 31. Son retrait rend la couverture indéfinie.
- **Fréquence historique complémentaire.** Le rapprochement plusieurs-à-un des cinq feux haut-garonnais vers le cliché des 586 communes n’exclut aucun événement. Base fixe de 630 990 ha de territoire. 2024 donne 1 feu et 0,00158 pour 1 000 ha. 2025 donne 4 feux et 0,00634 pour 1 000 ha. Moyenne et médiane de 0,00396 pour 1 000 ha, avec 80 % des feux en 2025.
- **Tests exécutés.** `python3 -m unittest discover -s tests -v` donne 19/19. `python3 -m py_compile scripts/calculer_scenarios_q2_q3.py` réussit. `python3 scripts/valider_resultats_kpi.py` valide 168 KPI, les dénominateurs et la monotonie. Le notebook recalcule les mêmes 168 lignes à partir des sources et vérifie les identités de comptage, les dénominateurs nuls, les clés 1:1 et le rapprochement communal.
- **Reproductibilité et PDF contrôlés.** Deux exécutions intégrales des huit cellules de code ont réussi, la première avec téléchargement HTTPS, la seconde avec la commande `nbconvert` ci-dessous et le CSV local vérifié. Les cinq tables CSV produites sont identiques octet par octet et le graphique PNG est identique pixel par pixel. Les 12 lignes KPI et les deux lignes historiques extraites du PDF avec `pdftotext -layout` concordent avec les CSV, aux arrondis d’affichage près. Les huit pages A4 ont été rendues par `pdftoppm` et inspectées visuellement, y compris l’arbre, le graphique et les tableaux.
- **À qualifier.** Confirmation écrite de la sémantique de `date`, téléchargement BDIFF avec TLS validé, homogénéité de déclaration entre années, accès à 2021–2023 et revue indépendante. Sous-déclaration, deux saisons et quatre jours feu éligibles dans le 31 limitent l’interprétation. Aucune doctrine SDIS ne découle de la simulation.

## Reproduction

Depuis la racine du dépôt, avec Python 3.10 et l’accès HTTPS à data.gouv.fr pour le référentiel communal. Les deux familles d’archives versionnées restent à leurs emplacements sous `datasets/public/`. L’exécution produit une nouvelle copie dans `/tmp`.

```bash
python3 -m venv .venv-atelier
source .venv-atelier/bin/activate
python -m pip install pandas==2.3.3 matplotlib==3.10.9 ipykernel==7.3.0 nbconvert==7.17.2 nbformat==5.11.1 nbclient==0.11.0
python -m pip check
python -m unittest discover -s tests -v
python -m jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=python3 \
  --ExecutePreprocessor.timeout=120 --output-dir=/tmp \
  --output=Atelier1_calcul_reexecute.ipynb \
  livrables/atelier-01-kpi/Atelier1_calcul_Equipe_Michel_Marine.ipynb
```

En mode hors ligne, récupérer au préalable le CSV Surface depuis le lien ci-dessus et exporter `ATELIER_SURFACE_CSV=/chemin/vers/surface-commune.csv`. Empreinte attendue `e1a5eb3f42d5be506add598a8c838b10872b36013bb05306d0a47c8546a6c347`. Pour exporter les preuves de calcul, définir `ATELIER_PREUVES` vers un dossier de sortie. Le notebook produit les CSV de résultats, jointures, sensibilité, qualité et historique, ainsi que le graphique de charge. Le PDF reprend ces sorties et les complète avec le cadrage et l’arbre.

## Intégration et revue

Branche `atelier/kpi-finalisation-2026-11-19`, avec la branche de la PR n° 3 comme cible de la PR dédiée. Revue indépendante requise sur les conventions météo, la qualité des sources, les calculs et la formulation commune de la décision. Proposition pour le prochain point de pilotage daté du 28/11/2026 : consigner les deux saisons réellement calculées et laisser l’exigence de cinq années ouverte. [Ticket n° 9](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/issues/9) · [PR n° 3](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/pull/3)
