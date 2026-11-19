# Fiche source — Archives Météo des forêts (2024, 2025, 2026)

**Producteur :** Météo-France — **portail :** [data.gouv.fr](https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets).  
**Licence affichée :** Licence Ouverte 2.0 (voir le catalogue et le manifeste d'extraction).  
**Questions :** Q2, Q3 et Q4. **Statut : fichier effectivement téléchargé et profilé pour le schéma, les dates, les codes et les doublons ; sémantique des échéances à vérifier.**

## Traçabilité

Le [manifeste](../../../datasets/public/meteo_des_forets/manifest.json) donne pour chaque archive : URL stable, identifiant de ressource, date de collecte, taille, empreinte SHA-256 et en-têtes observés. Le [rapport de profilage](../../resultats/profilage_sources_v1.md) est produit par le script d'audit.

| Année | Lignes | Départements | Dates distinctes | Dates min/max | Doublons département × date |
|---|---:|---:|---:|---|---:|
| 2024 | 11 520 | 96 | 120 | 03/06–30/09 | 0 |
| 2025 | 11 520 | 96 | 120 | 03/06–30/09 | 0 |
| 2026 | 12 576 | 96 | 131 | 28/05–05/10 | 0 |

Chaque fichier couvre les **13 départements de la région Occitanie**, dont le **31**. Les dates sont propres à leur année. Ces résultats sont ceux du profilage automatique des fichiers présents dans le dépôt.

## Colonnes réellement présentes

- 'date' : date de référence du fichier, à qualifier comme émission/validité.
- 'num_dep' : code département, conserver comme chaîne.
- 'niveau_j1' et 'niveau_j2' : niveaux codés de 1 à 4 observés ; préciser la valeur prévisionnelle applicable à chaque journée.
- 'nom_dep' (2024/2026) et 'dep_nom' (2025) : même rôle présumé, à harmoniser.

**Écart détecté :** les fichiers 2024 et 2025 sont séparés par virgule ; 2026 par point-virgule. Le pipeline lit chaque délimiteur depuis le manifeste. Aucun calcul Q2 ne doit appliquer arbitrairement J1 à la colonne 'date'.

## Jointures / usages admissibles

- Dénombrer les **observations météo par département et date de référence**, leur répartition et leur disponibilité : exploitable pour l'audit.
- Calculer le **nombre de journées de surveillance par niveau**, ou la **couverture des journées de feu**, nécessite d'abord de fixer la date de validité de la prévision et son échéance.
- Le grain cible est département × jour valide × échéance ; ce n'est **pas** un signal météorologique communal.

**Responsables de revue proposés, avis non encore enregistrés :** Maeva (catalogue), Chantal (qualité/attribution), Stéphane (extraction), Ludovic (interprétation KPI).
