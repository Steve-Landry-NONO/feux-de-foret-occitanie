# Fiche source provisoire — Incendies dérivés de BDIFF (ArcGIS)

**Objectif :** disposer d'une première extraction d'événements datés et géolocalisés pour préparer les analyses Q1, Q2 et Q4.  
**Producteur initial déclaré :** IGNF / Géorisques, données issues de BDIFF.  
**Diffuseur secondaire :** Esri France, couche ArcGIS FeatureServer. **Cette source n'est pas l'export BDIFF d'origine.**

## Ressources identifiées

- [BDIFF — export officiel à vérifier](https://bdiff.agriculture.gouv.fr/incendies).
- [Couche Esri 2024](https://services.arcgis.com/d3voDfTFbHOCRwVR/ArcGIS/rest/services/G%C3%A9orisques___Les_feux_de_For%C3%AAt__2024_/FeatureServer/16).
- [Couche Esri « actuelle » décrite comme 2025](https://services.arcgis.com/d3voDfTFbHOCRwVR/ArcGIS/rest/services/G%C3%A9orisques___Les_feux_de_For%C3%AAt/FeatureServer/14).

**Licence de redistribution de la couche Esri : à vérifier.** Les données élémentaires temporaires ne sont donc pas commitées ; seuls les métadonnées et résultats agrégés de contrôle sont publiés.

## Constats sur les extractions réelles

Au 19 novembre 2026, le script de collecte a récupéré **413 lignes 2024** pour les départements d'Occitanie. Les contrôles ont relevé 413 identifiants retenus et aucune date d'alerte manquante dans cet extrait.

**Pour 2025**, les deux points d'accès Esri testés ont retourné **404** lors de la collecte automatisée. Ce millésime demeure donc **non collecté** ; ce n'est pas la preuve qu'aucun incendie n'a eu lieu. Le [rapport d'audit](../../resultats/profilage_sources_v1.md) indique les données effectivement utilisées.

**Réserve majeure :** le service Esri signale que des enregistrements n'ont pas été repris pour certaines communes historiques. Le millésime 2024, même techniquement consultable, doit être recoupé avec l'export BDIFF officiel avant une estimation de fréquence ou de seuil.

## Colonnes candidates du service

Champs publiés dans le schéma ArcGIS : 'Annee', 'Numero', 'Departement', 'Code_INSEE', 'Nom_de_la_commune', 'Date_de_premiere_alerte', 'Surface_parcourue', 'Surface_foret'. Le script conserve aussi une date convertie dans le fuseau Europe/Paris, à vérifier autour des changements de jour.

**Ne pas confondre** 'Moyens_de_premiere_intervention' avec un historique d'engagement SDIS suffisant pour Q5/Q6.

## Test de jointure

Sur les **289 journées départementales distinctes avec feu dans l'extrait 2024**, **161** possèdent une ligne météo sur la **même date brute** et **128** n'en ont pas. Ces mesures décrivent une compatibilité technique initiale, **pas une couverture de seuil Q2** : la météo n'est disponible que sur la saison et la validité des prévisions J1/J2 reste à confirmer. Un jour absent de la source n'est pas un jour sans feu garanti.

**Revue attendue :** Maeva pour comparer à l'original BDIFF, Chantal pour les licences et limites, Stéphane pour les doublons et Ludovic pour l'analyse des périodes.
