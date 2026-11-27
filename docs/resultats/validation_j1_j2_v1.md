# Validation documentaire et test du décalage J+1 / J+2

**Règle confirmée par Météo-France :** à 17 h un jour J, publication du danger de J+1 (lendemain) et J+2 (surlendemain).

**Différence de libellé restante :** le producteur décrit Reference_time comme date/heure de production ; les archives récupérées ont une colonne date. L'alignement est plausible, mais doit être corroboré explicitement.

## Jointures exploratoires sur date de validité recalculée

| Année | Échéance | Jours départementaux avec feu | Avec prévision | Sans prévision | Jours feu Haute-Garonne | Raccordés Haute-Garonne |
|---|---|---:|---:|---:|---:|---:|
| 2024 | J+1 | 289 | 160 | 129 | 1 | 0 |
| 2024 | J+2 | 289 | 159 | 130 | 1 | 0 |
| 2025 | J+1 | 340 | 208 | 132 | 4 | 4 |
| 2025 | J+2 | 340 | 210 | 130 | 4 | 4 |

**Ces nombres sont des contrôles de raccord, pas encore des résultats Q2–Q3 validés.**

Le scénario métier le plus cohérent est la décision à J-1 après la publication de 17 h, basée sur le niveau_j1 de la veille. Une variante de planification à J-2 peut utiliser niveau_j2 deux jours avant l'intervention. Il faut garder ces variantes distinctes.

**Attention :** ce produit Météo-France vise la sensibilisation grand public, pas le pilotage opérationnel des moyens des SDIS.

Références : https://confluence-meteofrance.atlassian.net/wiki/spaces/OpenDataMeteoFrance/pages/874741792/Donn%2Bes%2Bexpertis%Bes ; https://meteofrance.com/actualites/la-meteo-des-forets-sinformer-sur-le-danger-de-feux

## Contrôles encore ouverts

- Confirmation du champ date / Reference_time auprès du producteur ou dans le descriptif de l'archive.
- Comparaison d'un jour d'archive à une carte datée de Météo-France.
- Validation du périmètre et des scénarios avec le groupe.
- Contrôle indépendant de la provenance TLS des archives BDIFF.
