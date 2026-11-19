# Catalogue de collecte des données — v0 (19 novembre 2026)

**Statut : recherche documentaire.** Les fiches publiques ont été consultées ; aucune ligne issue d'un fichier brut n'a été profilée dans cette contribution. Ce catalogue complète l'[inventaire](inventaire.md), la [matrice Q1–Q6](matrice.md) et le [suivi A1–A4](../suivi/actions-faisabilite.md). Il ne remplace pas les fiches individuelles demandées par Marine PROST.

## 1. Principe : une source sert une question, pas l'inverse

- **Q1 — Priorités territoriales :** événements d'incendie + surface forestière + géographie communale, sur une période comparable.
- **Q2 — Seuil météo :** journées **avec feu observé** + danger Météo des forêts au **département × jour** et à échéance fixe.
- **Q3 — Mobilisation :** jours activés par seuil ; distinguer jours sans feu *observé* et jours sans donnée. Les coûts de patrouille ne sont pas fournis par les budgets SDIS globaux.
- **Q4 — Comparaisons :** indicateurs reproductibles sur plusieurs périodes et territoires homogènes.
- **Q5 — Délais :** événements/alertes/arrivées géolocalisés et horodatés (données SDIS à confirmer).
- **Q6 — Simultanéité :** intervalles d'engagement, compétences, véhicules et disponibilités (données SDIS à confirmer).

## 2. Socle prioritaire (à ouvrir en premier)

| ID | Source et accès | Ce que l'on cherche | Grain/temps à contrôler | Q | État |
|---|---|---|---|---|---|
| S01 | [BDIFF — catalogue](https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff) ; [application officielle](https://bdiff.agriculture.gouv.fr/incendies) | Feux, date, commune, surface, identifiant événement | Catalogue affiche 2006–2022, application présente aussi des années récentes ; possibilité d'export à confirmer | Q1, Q2, Q4 | Métadonnées consultées ; fichier non obtenu |
| S02 | [Archives Météo des forêts](https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets) : **mdf.2024, mdf.2025, mdf.2026**, documentation et géométrie des départements | Niveau de danger, émission/validité/échéance | Département × jour supposé, clés et couverture à confirmer sur les trois CSV.GZ | Q2, Q3, Q4 | Ressources annuelles repérées ; fichiers non ouverts |
| S03 | [COG INSEE](https://www.data.gouv.fr/datasets/code-officiel-geographique-1) et [passage historique des codes](https://www.data.gouv.fr/datasets/table-de-passage-des-codes-communes-vers-le-millesime-en-vigueur-du-cog) | Codes et millésimes des communes et départements | Commune × millésime ; respecter les changements historiques | Q1, Q4, Q5 | Fiches repérées ; fichiers non ouverts |
| S04 | [Masque Forêt IGN](https://www.data.gouv.fr/datasets/masque-foret) ; [BD Forêt V2](https://www.data.gouv.fr/datasets/bd-foret-r) | Dénominateur forestier, composition et surface | Polygones × millésime ; **choisir et documenter le référentiel retenu**, ne pas mélanger les surfaces | Q1, Q4 | Candidats ; extractions et unités non vérifiées |
| S05 | [Interventions réalisées par les SIS (DGSCGC)](https://www.data.gouv.fr/datasets/interventions-realisees-par-les-services-d-incendie-et-de-secours) | Volume annuel départemental, comparaison nationale | À relever sur CSV ; **agrégat statistique, pas un journal horodaté des interventions** | Q4 ; contexte Q5 | Fiche et exports CSV repérés ; fichiers non ouverts |

## 3. Enrichissements pertinents (seulement si les indicateurs le justifient)

| ID | Source vérifiable | Utilisation possible | Q | Prudence |
|---|---|---|---|---|
| S06 | [Météo-France — climatologie quotidienne](https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-quotidiennes) | Pluie, température, vent : comprendre les conditions de danger | Q2, Q4 | Mesures par **station** : pas de valeur départementale directe sans méthode |
| S07 | [EFFIS / Copernicus](https://forest-fire.emergency.copernicus.eu/applications/data-and-services) | Surfaces brûlées, tendances européennes et indice FWI | Q1, Q4 | Détections/indicateurs non interchangeables avec les événements BDIFF ou la Météo des forêts |
| S08 | [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/download/) | Points chauds satellitaires, couverture historique complémentaire | Q1, Q4 | **Point chaud ≠ départ de feu certifié** ; accès aux archives soumis à identification |
| S09 | [Comptes des SDIS 2012–2025](https://www.data.gouv.fr/datasets/comptes-des-sdis-2012-2025) | Contexte budgétaire pour comparer les territoires | Q3, Q4, Q6 | Comptes globaux ≠ coût incrémental du dispositif renforcé |
| S10 | [OCS GE IGN](https://www.data.gouv.fr/datasets/ocs-ge) | Occupation/utilisation du sol et voisinage des espaces boisés | Q1, Q4 | Jointure spatiale et millésimes nécessaires |
| S11 | [GASPAR / Géorisques](https://www.georisques.gouv.fr/donnees/bases-de-donnees/procedures-administratives-relatives-aux-risques) | Présence de dispositifs de prévention et de documents réglementaires | Q1, Q4 | Indicateur administratif ; **ne mesure ni forêt ni incendie** |
| S12 | [Zones d'obligation de débroussaillement](https://www.data.gouv.fr/datasets/zones-impactees-par-les-obligations-legales-de-debroussaillement) | Exposition et prévention selon emprise réellement couverte | Q1 | Couverture locale et réglementation/millésime à vérifier |
| S13 | [ADMIN EXPRESS COG IGN](https://www.data.gouv.fr/datasets/admin-express-admin-express-cog-admin-express-cog-carto-admin-express-cog-carto-pe-admin-express-cog-carto-plus-pe) | Polygones pour cartes et surfaces, référentiel territorial | Q1, Q4 | Ne pas substituer les codes postaux aux codes INSEE |
| S14 | [Contours des feux — Hérault 2025](https://www.data.gouv.fr/datasets/contours-des-feux-de-forets-dans-lherault-en-2025) | Cas départemental de contrôle géospatial | Q1, Q4 | Ne couvre **pas** la Haute-Garonne ; recouvrements BDIFF à dédoublonner |
| S15 | [Pyronear — images de départs de feux 2024](https://www.data.gouv.fr/datasets/images-de-departs-de-feux-sdis-2024) | Annexe possible sur détection par images | Hors cœur Q1–Q6 | Très volumineux ; priorité basse et pas de nouvel objectif de computer vision sans décision |
| S16 | [Accessibilité physique des forêts](https://www.data.gouv.fr/datasets/accessibilite-physique-des-forets-1) | Hypothèses de prépositionnement et accessibilité | Q5 | Accessibilité forestière générique ≠ temps d'arrivée d'un engin SDIS |
| S17 | [Copernicus — indicateurs de danger climatique](https://cds.climate.copernicus.eu/datasets/sis-tourism-fire-danger-indicators?tab=overview) | Stress-test climatique, évolution de danger | Q4 | FWI projeté ≠ niveau officiel Météo des forêts ; hors besoin minimal |
| S18 | [BD TOPO/transport — IGN](https://www.data.gouv.fr/datasets/admin-express-admin-express-cog-admin-express-cog-carto-admin-express-cog-carto-pe-admin-express-cog-carto-plus-pe) | Référentiel géographique de base pour une future étude de trajet | Q5 | Le lien pointe **uniquement vers Admin Express** ; identifier une ressource routière BD TOPO avant emploi |

## 4. Points de jonction à investiguer

| Jointure candidate | Grain cible | Condition vérifiable | Risque de faux résultat |
|---|---|---|---|
| BDIFF × MdF | département × date **de validité**, échéance météo fixe | Date de feu disponible, historique commun, danger non dupliqué | Jointure vide, multiplication des feux |
| BDIFF × COG | code commune source × millésime | Codes en texte, gestion des changements | Faux rattachement territorial |
| Feux × forêt IGN | commune × année (après intersection spatiale) | Surface forestière non nulle, définition et millésime cohérents | Ratio biaisé |
| SIS annuels × COG département | département × année | Même campagne statistique / définition | Comparaison trompeuse |
| Interventions × engagements SDIS | identifiant intervention, intervalles temporels | Clés réelles, début/fin, disponibilité et confidentialité | Simultanéité simulée présentée comme observée |

**Alerte majeure A1 :** les pages BDIFF et MdF ne prouvent pas à elles seules un historique commun. Ne jamais utiliser un indice Copernicus/IFM comme s'il était un niveau MdF, et ne pas compter un point chaud FIRMS comme un feu enregistré.

## 5. Mode de collecte reproductible

1. Consulter la fiche officielle et ouvrir une **ressource physique** ; noter le nom, la version, la date et la licence.
2. Pour les catalogues data.gouv.fr, utiliser [le script de collecte](../../scripts/collecter_data_gouv.py) sur un poste connecté ; commencer par le mode inventaire.
3. Télécharger en dehors du dépôt Git : `data/raw/` ; conserver SHA-256, taille, URL et date dans `docs/annexes/registre-extractions.jsonl` ou un registre local si le contenu est sensible.
4. Exécuter `notebooks/01` et `02` avant de tenter le notebook des jointures ; compléter les fiches de sources individuelles sous les comptes des membres concernés.
5. Ne passer de « métadonnées consultées » à « fichier examiné » que lorsque son contenu, son schéma et sa couverture ont effectivement été contrôlés.

**Limite de cette mise à jour :** aucune ressource brute n'a pu être téléchargée dans l'environnement d'exécution ici. Les statuts restent donc « repérée » ou « métadonnées consultées ». Les responsables de revue sont à confirmer avec le groupe.
