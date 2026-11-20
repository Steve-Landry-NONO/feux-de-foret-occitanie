# Fiche source — Archives Météo des forêts (2024, 2025, 2026)

**Producteur :** Météo-France — **portail :** [data.gouv.fr](https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets).  
**Licence affichée :** Licence Ouverte 2.0 (voir le catalogue et le manifeste d'extraction).  
**Questions :** Q2, Q3 et Q4. **Statut : fichier effectivement téléchargé et profilé pour le schéma, les dates, les codes et les doublons ; **sémantique J+1/J+2 confirmée par Météo-France**, équivalence du nom de colonne de date à corroborer.**

## Traçabilité

Le [manifeste](../../../datasets/public/meteo_des_forets/manifest.json) donne pour chaque archive : URL stable, identifiant de ressource, date de collecte, taille, empreinte SHA-256 et en-têtes observés. Le [rapport de profilage](../../resultats/profilage_sources_v1.md) est produit par le script d'audit.

| Année | Lignes | Départements | Dates distinctes | Dates min/max | Doublons département × date |
|---|---:|---:|---:|---|---:|
| 2024 | 11 520 | 96 | 120 | 03/06–30/09 | 0 |
| 2025 | 11 520 | 96 | 120 | 03/06–30/09 | 0 |
| 2026 | 12 576 | 96 | 131 | 28/05–05/10 | 0 |

Chaque fichier couvre les **13 départements de la région Occitanie**, dont le **31**. Les dates sont propres à leur année. Ces résultats sont ceux du profilage automatique des fichiers présents dans le dépôt.

## Colonnes réellement présentes

- 'date' : date figurant dans l'archive. La [documentation officielle Météo-France](https://confluence-meteofrance.atlassian.net/wiki/spaces/OpenDataMeteoFrance/pages/874741792/Donn%2Bes%2Bexpertis%Bes) définit le champ de production sous le nom **Reference_time** (date et heure de création). **Nous interprétons 'date' comme sa date de référence**, mais le changement de libellé doit encore être confirmé explicitement.
- 'num_dep' : code département, conserver comme chaîne.
- 'niveau_j1' : danger prévu pour le **lendemain de la production**, confirmé par Météo-France ; la carte est habituellement produite à **17 h**.
- 'niveau_j2' : danger prévu pour le **surlendemain de la production**, confirmé par Météo-France.
- Niveaux officiels : **1 faible (vert), 2 modéré (jaune), 3 élevé (orange), 4 très élevé (rouge)**.
- 'nom_dep' (2024/2026) et 'dep_nom' (2025) : même rôle présumé, à harmoniser.

**Écart détecté :** les fichiers 2024 et 2025 sont séparés par virgule ; 2026 par point-virgule. Le pipeline lit chaque délimiteur depuis le manifeste. Pour Q2, **ne pas joindre J+1 au jour de la ligne brute** : sa date cible est 'date + 1 jour' ; pour J+2, 'date + 2 jours'. La [première exécution documentée](../../resultats/validation_j1_j2_v1.md) applique ces décalages tout en conservant une réserve sur l'alias 'date' / 'Reference_time'.

## Jointures / usages admissibles

- Dénombrer les **observations météo par département et date de référence**, leur répartition et leur disponibilité : exploitable pour l'audit.
- Calculer le **nombre de journées de surveillance par niveau**, ou la **couverture des journées de feu**, nécessite d'abord de fixer la date de validité de la prévision et son échéance.
- Le grain cible est département × jour valide × échéance ; ce n'est **pas** un signal météorologique communal.

**Responsables de revue proposés, avis non encore enregistrés :** Maeva (catalogue), Chantal (qualité/attribution), Stéphane (extraction), Ludovic (interprétation KPI).


## Distinction importante pour la soutenance

La [communication officielle de Météo-France](https://meteofrance.com/actualites/la-meteo-des-forets-sinformer-sur-le-danger-de-feux) indique que la Météo des forêts est conçue pour la **sensibilisation du grand public**, et qu'elle **ne remplace pas les dispositifs opérationnels spécialisés destinés aux SDIS**. Notre utilisation des seuils est donc une **simulation pédagogique de décisions**, non une doctrine de surveillance validée par le SDIS 31.

**État de validation :** définitions de J+1/J+2, publication à 17 h et échelle des niveaux **confirmées par la source primaire** ; correspondance du champ d'archive 'date' et de 'Reference_time' encore à corroborer avant validation complète des KPI.
