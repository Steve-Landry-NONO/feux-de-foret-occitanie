# Qualification BDIFF — ticket #14

Base : df65c0bc2b4ff7d808009cbfcaff8cd8ef83774b. Source PR #3 : 479e5d91296a5994eaed304678504cdc05fb3a17. Contrôles locaux sur les archives transmises, SHA conformes au manifeste. Aucun pipeline ni original modifié.

## Résultats

413 et 472 événements, aucun doublon ni identifiant vide, dates et territoires renseignés, surfaces totales renseignées, numériques, finies et non négatives. Unité m² (1 ha = 10 000 m²). Aucun composant individuel supérieur au total. Quatre catégories de surface entièrement vides dans les deux années : ne pas interpréter leurs sommes techniques de zéro comme des surfaces nulles. La somme des catégories disjointes reste à définir. Le format des codes INSEE ne prouve pas leur existence au COG. Seuils proposés, validation collective en attente.

## Provenance et conformité

SHA-256 ne valide pas TLS. La collecte initiale n'a pas validé le certificat. La revue spécifique de Maeva n'a pas été retrouvée : demander sa référence. Les annexes PDF décrivent l'éditeur, les comptes et le RGPD ; aucune clause explicite de licence retrouvée dans les mentions légales selon la lecture locale. La fiche source indique Licence Ouverte 2.0 au catalogue ; confirmer la portée exacte et l'attribution avant redistribution. La date d'alerte correspond à l'information parvenue au CODIS, pas nécessairement au début du feu. Les surfaces sont mesurées ou estimées. Les catégories dépendent de la zone et de la campagne. Absence de recensement ≠ absence réelle d'incendie.

## Reproduction

```sh
git fetch origin refs/pull/3/head
mkdir -p /tmp/bdiff-source
git archive 479e5d91296a5994eaed304678504cdc05fb3a17 datasets/public/bdiff_officiel | tar -x -C /tmp/bdiff-source
python -m unittest discover -s tests -v
python scripts/controler_qualite_bdiff.py /tmp/bdiff-source/datasets/public/bdiff_officiel/bdiff_occitanie_2024.zip /tmp/bdiff-source/datasets/public/bdiff_officiel/bdiff_occitanie_2025.zip --manifest /tmp/bdiff-source/datasets/public/bdiff_officiel/manifest.json --commit-source 479e5d91296a5994eaed304678504cdc05fb3a17 > /tmp/preuve-controles-bdiff.json
```

Preuve JSON : résultats locaux du 27/11/2026 retranscrits lors de la publication. Script publié blob 219df1757d3b9912595d358743d690ceaa36aeda, identique au script local. Six méthodes synthétiques initiales réussies ; code réel 0. Nouvelle exécution locale : 7 méthodes réussies, dont les trois codes CLI 0/1/2 ; contrôle réel code 0, JSON régénéré identique au rapport local initial. Suite complète de main non réexécutée. Comparaison avec main 0c6cc0b072c0d289ce66db8356e0e139a6524b98 : quatre commits documentaires sans chevauchement des fichiers ; PR fusionnable selon GitHub. Codes 0 conformité bloquante, 1 échec, 2 manifeste absent sans échec.

## Contrats à convenir avec Stéphane

REF-01 : COG du millésime retenu, codes texte, unicité, historique des communes, anti-jointures et taux de raccordement ; aucune correction silencieuse. JNT-01 : agrégation des événements au grain département × jour avant jointure, unicité météo par date valide et échéance, cardinalité et effectifs avant/après, anti-jointures, distinction hors saison/lacune. JNT-02 : zéro recensé seulement sur couverture établie, inconnu sinon. Demander à Stéphane les contrats de clés, grain et sorties d'audit ; à Maeva les preuves de provenance et licence ; à Steve les seuils et décisions. Aucun pipeline concurrent. Ticket #14 ouvert.
