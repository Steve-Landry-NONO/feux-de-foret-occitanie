# Suivi de faisabilité — actions A1 à A4

**Création :** 17 novembre 2026, à la suite de la revue du coordinateur transmise par Chantal.  
**Statut global :** plan documentaire proposé ; aucune action de vérification réalisée par cette mise à jour. Les responsabilités ci-dessous suivent les rôles du README et restent à confirmer par l'équipe. Aucun contact externe n'est effectué. Une **mise à jour des contrôles réellement exécutés le 19/11** figure en fin de document ; ce texte historique décrit l'état du 17/11.

La [spécification v1](../specification/specification-v1-2026-11-17.md) reste provisoire. Les corrections C1–C3 portent sur le document ; A1–A4 concernent la faisabilité réelle.

| Action | Priorité | Pilotage proposé | Travail à réaliser | Résultat et critère de clôture | État |
|---|---|---|---|---|---|
| A1 — Chevauchement BDIFF / météo | Haute | Maeva et Stéphane ; revue Chantal et Ludovic | Ouvrir les ressources exactes ; relever dates min/max, jours manquants, territoires, clés, niveaux, émission et échéance | Table source × ressource × territoire × dates × grain, références d'extraction ; décision justifiée Q2 et Q3 croisés calculables ou non | En cours : météo profilée, BDIFF primaire à récupérer et échéance météo à valider |
| A2 — Repli Q5–Q6 | Haute | Steve pour l'accès ; Ludovic pour les scénarios ; Chantal pour la conformité | Vérifier accès et réutilisation des horodatages, intervalles d'engagement, disponibilités, compétences, engins et coûts ; documenter les absences | Tableau données disponibles / absentes / non vérifiées, décision du groupe sur simulation ou non-calcul, hypothèses et limites ; aucun délai cible ou budget inventé | À faire |
| A3 — Période d'étude | Moyenne | Ludovic et Stéphane ; revue collective | Après A1, choisir les fenêtres par indicateur et traiter les années incomplètes | Périodes retenues et exclusions justifiées ; Q1 peut différer de Q2–Q3 ; 2022 exclue de toute analyse de seuil sans météo correspondante | À faire, dépend d'A1 |
| A4 — Fiches de sources, exercice 2 | Haute | Maeva ; Chantal pour qualité/licences ; Stéphane pour profilage | Documenter chaque ressource retenue et actualiser inventaire et matrice après inspection | Fiches avec producteur/diffuseur, URL exacte, format, grain, période réelle, fraîcheur, emprise, clés, licence fichier, données personnelles, limites, date et responsable de vérification | En cours : fiches météo et source Esri provisoire rédigées, fiches individuelles et autres sources à compléter |

## Ordre de traitement proposé

Commencer A1 et l'identification des ressources A4 ; examiner l'accès opérationnel A2 en parallèle si l'équipe le décide. Arrêter A3 après examen des fichiers. Le coordinateur fixera les échéances ; aucune date de réalisation n'est inventée ici.

## Convention de statut des sources

- **Candidate :** ressource pressentie, non inspectée.
- **Métadonnées consultées :** fiche ou page lue ; fichiers et conditions effectives non validés.
- **Fichier examiné :** ressource ouverte, schéma et couverture relevés ; exploitation pas encore nécessairement admissible.
- **Exploitable pour un indicateur :** contrôles et conditions d'usage documentés, grain et période compatibles avec cet indicateur.
- **Écartée pour un indicateur :** motif documenté ; ne signifie pas inutilité pour tout le projet.

Ne changer un statut qu'avec une preuve et une date. Distinguer une donnée absente d'une donnée dont l'accès reste inconnu. Ne pas présenter une simulation proposée comme déjà autorisée ou réalisée.

## Preuves à joindre lors de la clôture

Pour chaque action, ajouter les références des fichiers ou documents examinés, la date, l'auteur effectif du contrôle, les observations et la décision. Une table vide ou une fiche de catalogue seule ne clôt pas une vérification de données. La disponibilité de dates de feux n'est pas établie par cette contribution et n'exige pas, à elle seule, un chevauchement avec la météo.

[Retour à la spécification](../specification/specification-v1-2026-11-17.md) · [Journal](../decisions/journal.md)


## Mise à jour vérifiée — 19 novembre 2026

Les documents de spécification du 17 novembre restent des **propositions historiques**. Les vérifications suivantes ont effectivement été exécutées depuis :

- **A1 — partiellement réalisé :** archives Météo-France 2024–2026 téléchargées et profilées ; 96 départements dont les 13 d'Occitanie, dates réelles et absence de doublons département × date établies. Incendies 2024 en provenance d'une couche secondaire Esri dérivée de BDIFF (413 événements d'Occitanie) ; les services 2025 testés répondent 404. L'export **BDIFF original** et l'interprétation des échéances météorologiques manquent, donc **A1 non clos**.
- **A2 — non clos :** pas d'accès SDIS confirmé aux horodatages d'arrivée, engagements, compétences, disponibilités ni aux coûts.
- **A3 — en attente :** les périodes des trois archives météo sont connues, mais la fenêtre commune **admissible** pour Q2/Q3 doit attendre le BDIFF original et la sémantique J+1/J+2.
- **A4 — partiellement réalisé :** [fiche Météo des forêts](../sources/fiches/meteo_des_forets_2024_2026.md) et [fiche de la source incendie secondaire](../sources/fiches/incendies_arcgis_derive_bdiff.md) créées avec preuves d'extraction et limites. Les fiches **personnelles des cinq étudiants**, l'IGN et l'INSEE restent à instruire.

**Preuves :** [rapport de profilage](../resultats/profilage_sources_v1.md), [modèle UML V0](../modelisation/modeles-de-donnees-v0.md), [PR #3](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/pull/3) et Issues [#4–#8](https://github.com/Steve-Landry-NONO/feux-de-foret-occitanie/issues).

**Une revue par les membres reste attendue.** Les noms indiqués dans les notebooks et fiches désignent des responsabilités proposées, pas des validations déjà effectuées.
