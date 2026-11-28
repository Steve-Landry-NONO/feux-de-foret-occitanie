# Preuve de l'intersection des journées avec feu — J+1 ET J+2

**Calcul reproductible sur les fichiers versionnés ; les effectifs sont des couples département × jour, pas des dates calendaires uniques.**

## Définition des ensembles

- **E** : ensemble de tous les couples (département, jour) avec au moins un feu BDIFF de type F, agrégés depuis la date de première alerte.
- **A** : sous-ensemble de E pour lequel une prévision J+1 est disponible à la date de validité calculée.
- **B** : sous-ensemble de E pour lequel une prévision J+2 est disponible à la date de validité calculée.
- **A ∩ B** : intersection calculée directement par égalité des clés (département, jour) présentes dans A et B.
- **E privé de (A ∩ B)** : journées avec feu hors de la cohorte commune.

L'intersection n'est jamais estimée par le minimum des deux effectifs. Les écarts A privé de B, B privé de A et E privé de (A union B) sont calculés séparément.

## Résultats calculés

| Année | E : tous les jours feu | A : J+1 | B : J+2 | A ∩ B | J+1 seul | J+2 seul | Ni J+1 ni J+2 | E hors cohorte | Part commune / E |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2024 | 289 | 160 | 159 | 159 | 1 | 0 | 129 | 130 | 55.02 % |
| 2025 | 340 | 208 | 210 | 208 | 0 | 2 | 130 | 132 | 61.18 % |

## Détail des journées non communes

Le CSV détaille chaque clé. J+1_seul appartient à A mais pas à B ; J+2_seul appartient à B mais pas à A ; aucune_echeance n'appartient ni à A ni à B.

| Année | Département | Jour | Feux BDIFF type F | Statut |
|---:|---:|---|---:|---|
| 2024 | 09 | 2024-02-05 | 1 | aucune_echeance |
| 2024 | 11 | 2024-01-01 | 1 | aucune_echeance |
| 2024 | 11 | 2024-01-09 | 1 | aucune_echeance |
| 2024 | 11 | 2024-01-18 | 2 | aucune_echeance |
| 2024 | 11 | 2024-01-24 | 1 | aucune_echeance |
| 2024 | 11 | 2024-01-26 | 1 | aucune_echeance |
| 2024 | 11 | 2024-02-03 | 1 | aucune_echeance |
| 2024 | 11 | 2024-02-04 | 1 | aucune_echeance |
| 2024 | 11 | 2024-02-07 | 3 | aucune_echeance |
| 2024 | 11 | 2024-02-15 | 1 | aucune_echeance |
| 2024 | 11 | 2024-02-20 | 1 | aucune_echeance |
| 2024 | 11 | 2024-02-24 | 1 | aucune_echeance |
| 2024 | 11 | 2024-02-29 | 1 | aucune_echeance |
| 2024 | 11 | 2024-03-08 | 1 | aucune_echeance |
| 2024 | 11 | 2024-03-13 | 1 | aucune_echeance |
| 2024 | 11 | 2024-03-18 | 1 | aucune_echeance |
| 2024 | 11 | 2024-03-19 | 1 | aucune_echeance |
| 2024 | 11 | 2024-03-21 | 1 | aucune_echeance |
| 2024 | 11 | 2024-03-25 | 1 | aucune_echeance |
| 2024 | 11 | 2024-03-27 | 1 | aucune_echeance |
| 2024 | 11 | 2024-03-29 | 1 | aucune_echeance |
| 2024 | 11 | 2024-04-03 | 1 | aucune_echeance |
| 2024 | 11 | 2024-04-06 | 1 | aucune_echeance |
| 2024 | 11 | 2024-04-11 | 1 | aucune_echeance |
| 2024 | 11 | 2024-04-16 | 2 | aucune_echeance |
| 2024 | 11 | 2024-04-17 | 1 | aucune_echeance |
| 2024 | 11 | 2024-04-19 | 1 | aucune_echeance |
| 2024 | 11 | 2024-04-20 | 2 | aucune_echeance |
| 2024 | 11 | 2024-04-23 | 1 | aucune_echeance |
| 2024 | 11 | 2024-04-24 | 1 | aucune_echeance |
| 2024 | 11 | 2024-05-19 | 1 | aucune_echeance |
| 2024 | 11 | 2024-05-24 | 1 | aucune_echeance |
| 2024 | 11 | 2024-05-26 | 1 | aucune_echeance |
| 2024 | 11 | 2024-05-30 | 1 | aucune_echeance |
| 2024 | 11 | 2024-06-03 | 2 | aucune_echeance |
| 2024 | 11 | 2024-06-04 | 2 | J+1_seul |
| 2024 | 11 | 2024-10-03 | 1 | aucune_echeance |
| 2024 | 11 | 2024-10-05 | 1 | aucune_echeance |
| 2024 | 11 | 2024-10-09 | 1 | aucune_echeance |
| 2024 | 11 | 2024-10-11 | 1 | aucune_echeance |
| 2024 | 11 | 2024-10-17 | 1 | aucune_echeance |
| 2024 | 11 | 2024-10-21 | 2 | aucune_echeance |
| 2024 | 11 | 2024-11-04 | 1 | aucune_echeance |
| 2024 | 11 | 2024-11-19 | 2 | aucune_echeance |
| 2024 | 11 | 2024-11-23 | 2 | aucune_echeance |
| 2024 | 11 | 2024-11-30 | 1 | aucune_echeance |
| 2024 | 11 | 2024-12-06 | 1 | aucune_echeance |
| 2024 | 11 | 2024-12-10 | 1 | aucune_echeance |
| 2024 | 11 | 2024-12-21 | 1 | aucune_echeance |
| 2024 | 30 | 2024-01-27 | 1 | aucune_echeance |
| 2024 | 30 | 2024-01-28 | 1 | aucune_echeance |
| 2024 | 30 | 2024-02-19 | 1 | aucune_echeance |
| 2024 | 30 | 2024-03-02 | 1 | aucune_echeance |
| 2024 | 30 | 2024-03-19 | 1 | aucune_echeance |
| 2024 | 30 | 2024-03-23 | 2 | aucune_echeance |
| 2024 | 30 | 2024-04-13 | 1 | aucune_echeance |
| 2024 | 30 | 2024-05-26 | 1 | aucune_echeance |
| 2024 | 30 | 2024-05-30 | 1 | aucune_echeance |
| 2024 | 30 | 2024-10-20 | 1 | aucune_echeance |
| 2024 | 30 | 2024-12-28 | 1 | aucune_echeance |
| 2024 | 31 | 2024-02-03 | 1 | aucune_echeance |
| 2024 | 34 | 2024-01-18 | 1 | aucune_echeance |
| 2024 | 34 | 2024-01-23 | 1 | aucune_echeance |
| 2024 | 34 | 2024-01-25 | 1 | aucune_echeance |
| 2024 | 34 | 2024-01-27 | 1 | aucune_echeance |
| 2024 | 34 | 2024-01-30 | 1 | aucune_echeance |
| 2024 | 34 | 2024-02-04 | 2 | aucune_echeance |
| 2024 | 34 | 2024-02-05 | 2 | aucune_echeance |
| 2024 | 34 | 2024-02-07 | 1 | aucune_echeance |
| 2024 | 34 | 2024-02-08 | 2 | aucune_echeance |
| 2024 | 34 | 2024-02-11 | 1 | aucune_echeance |
| 2024 | 34 | 2024-02-19 | 1 | aucune_echeance |
| 2024 | 34 | 2024-02-20 | 1 | aucune_echeance |
| 2024 | 34 | 2024-02-21 | 1 | aucune_echeance |
| 2024 | 34 | 2024-02-24 | 2 | aucune_echeance |
| 2024 | 34 | 2024-03-13 | 1 | aucune_echeance |
| 2024 | 34 | 2024-03-15 | 2 | aucune_echeance |
| 2024 | 34 | 2024-03-19 | 1 | aucune_echeance |
| 2024 | 34 | 2024-03-20 | 1 | aucune_echeance |
| 2024 | 34 | 2024-03-21 | 2 | aucune_echeance |
| 2024 | 34 | 2024-03-23 | 2 | aucune_echeance |
| 2024 | 34 | 2024-03-24 | 1 | aucune_echeance |
| 2024 | 34 | 2024-04-18 | 5 | aucune_echeance |
| 2024 | 34 | 2024-04-19 | 1 | aucune_echeance |
| 2024 | 34 | 2024-04-20 | 1 | aucune_echeance |
| 2024 | 34 | 2024-04-24 | 1 | aucune_echeance |
| 2024 | 34 | 2024-05-31 | 1 | aucune_echeance |
| 2024 | 34 | 2024-10-03 | 2 | aucune_echeance |
| 2024 | 34 | 2024-10-05 | 1 | aucune_echeance |
| 2024 | 34 | 2024-10-15 | 1 | aucune_echeance |
| 2024 | 34 | 2024-11-07 | 1 | aucune_echeance |
| 2024 | 34 | 2024-12-05 | 1 | aucune_echeance |
| 2024 | 34 | 2024-12-07 | 2 | aucune_echeance |
| 2024 | 34 | 2024-12-14 | 1 | aucune_echeance |
| 2024 | 34 | 2024-12-20 | 1 | aucune_echeance |
| 2024 | 34 | 2024-12-24 | 1 | aucune_echeance |
| 2024 | 34 | 2024-12-29 | 1 | aucune_echeance |
| 2024 | 48 | 2024-01-08 | 1 | aucune_echeance |
| 2024 | 48 | 2024-01-29 | 1 | aucune_echeance |
| 2024 | 48 | 2024-02-03 | 4 | aucune_echeance |
| 2024 | 48 | 2024-02-07 | 1 | aucune_echeance |
| 2024 | 48 | 2024-02-08 | 2 | aucune_echeance |
| 2024 | 48 | 2024-03-16 | 1 | aucune_echeance |
| 2024 | 48 | 2024-03-22 | 1 | aucune_echeance |
| 2024 | 48 | 2024-03-23 | 1 | aucune_echeance |
| 2024 | 48 | 2024-04-05 | 1 | aucune_echeance |
| 2024 | 48 | 2024-04-06 | 1 | aucune_echeance |
| 2024 | 48 | 2024-04-14 | 1 | aucune_echeance |
| 2024 | 48 | 2024-04-23 | 1 | aucune_echeance |
| 2024 | 66 | 2024-01-01 | 1 | aucune_echeance |
| 2024 | 66 | 2024-01-08 | 1 | aucune_echeance |
| 2024 | 66 | 2024-01-09 | 1 | aucune_echeance |
| 2024 | 66 | 2024-01-21 | 1 | aucune_echeance |
| 2024 | 66 | 2024-02-06 | 2 | aucune_echeance |
| 2024 | 66 | 2024-02-10 | 1 | aucune_echeance |
| 2024 | 66 | 2024-02-14 | 1 | aucune_echeance |
| 2024 | 66 | 2024-02-20 | 3 | aucune_echeance |
| 2024 | 66 | 2024-02-21 | 2 | aucune_echeance |
| 2024 | 66 | 2024-03-13 | 1 | aucune_echeance |
| 2024 | 66 | 2024-03-23 | 1 | aucune_echeance |
| 2024 | 66 | 2024-04-04 | 1 | aucune_echeance |
| 2024 | 66 | 2024-04-11 | 1 | aucune_echeance |
| 2024 | 66 | 2024-04-13 | 1 | aucune_echeance |
| 2024 | 66 | 2024-04-14 | 1 | aucune_echeance |
| 2024 | 66 | 2024-04-17 | 1 | aucune_echeance |
| 2024 | 66 | 2024-04-20 | 2 | aucune_echeance |
| 2024 | 66 | 2024-04-27 | 1 | aucune_echeance |
| 2024 | 66 | 2024-11-27 | 1 | aucune_echeance |
| 2024 | 66 | 2024-11-30 | 1 | aucune_echeance |
| 2024 | 81 | 2024-04-08 | 1 | aucune_echeance |
| 2025 | 09 | 2025-02-20 | 1 | aucune_echeance |
| 2025 | 09 | 2025-03-06 | 1 | aucune_echeance |
| 2025 | 09 | 2025-03-07 | 1 | aucune_echeance |
| 2025 | 09 | 2025-11-14 | 1 | aucune_echeance |
| 2025 | 09 | 2025-12-11 | 1 | aucune_echeance |
| 2025 | 09 | 2025-12-18 | 1 | aucune_echeance |
| 2025 | 11 | 2025-01-16 | 1 | aucune_echeance |
| 2025 | 11 | 2025-02-03 | 2 | aucune_echeance |
| 2025 | 11 | 2025-02-14 | 1 | aucune_echeance |
| 2025 | 11 | 2025-02-19 | 1 | aucune_echeance |
| 2025 | 11 | 2025-02-26 | 1 | aucune_echeance |
| 2025 | 11 | 2025-03-01 | 1 | aucune_echeance |
| 2025 | 11 | 2025-03-02 | 1 | aucune_echeance |
| 2025 | 11 | 2025-03-06 | 1 | aucune_echeance |
| 2025 | 11 | 2025-03-15 | 2 | aucune_echeance |
| 2025 | 11 | 2025-03-18 | 1 | aucune_echeance |
| 2025 | 11 | 2025-03-28 | 2 | aucune_echeance |
| 2025 | 11 | 2025-04-06 | 1 | aucune_echeance |
| 2025 | 11 | 2025-04-07 | 1 | aucune_echeance |
| 2025 | 11 | 2025-04-08 | 1 | aucune_echeance |
| 2025 | 11 | 2025-04-18 | 1 | aucune_echeance |
| 2025 | 11 | 2025-04-21 | 1 | aucune_echeance |
| 2025 | 11 | 2025-04-24 | 1 | aucune_echeance |
| 2025 | 11 | 2025-04-26 | 1 | aucune_echeance |
| 2025 | 11 | 2025-05-08 | 1 | aucune_echeance |
| 2025 | 11 | 2025-05-13 | 2 | aucune_echeance |
| 2025 | 11 | 2025-05-18 | 2 | aucune_echeance |
| 2025 | 11 | 2025-05-22 | 1 | aucune_echeance |
| 2025 | 11 | 2025-05-25 | 2 | aucune_echeance |
| 2025 | 11 | 2025-05-30 | 2 | aucune_echeance |
| 2025 | 11 | 2025-05-31 | 1 | aucune_echeance |
| 2025 | 11 | 2025-10-06 | 1 | aucune_echeance |
| 2025 | 11 | 2025-10-07 | 2 | aucune_echeance |
| 2025 | 11 | 2025-10-13 | 1 | aucune_echeance |
| 2025 | 11 | 2025-10-26 | 1 | aucune_echeance |
| 2025 | 11 | 2025-10-28 | 1 | aucune_echeance |
| 2025 | 11 | 2025-11-03 | 4 | aucune_echeance |
| 2025 | 11 | 2025-11-05 | 1 | aucune_echeance |
| 2025 | 11 | 2025-11-13 | 1 | aucune_echeance |
| 2025 | 11 | 2025-11-21 | 1 | aucune_echeance |
| 2025 | 11 | 2025-11-22 | 2 | aucune_echeance |
| 2025 | 11 | 2025-11-23 | 2 | aucune_echeance |
| 2025 | 11 | 2025-12-18 | 1 | aucune_echeance |
| 2025 | 11 | 2025-12-31 | 1 | aucune_echeance |
| 2025 | 12 | 2025-04-01 | 1 | aucune_echeance |
| 2025 | 12 | 2025-04-30 | 1 | aucune_echeance |
| 2025 | 30 | 2025-01-13 | 1 | aucune_echeance |
| 2025 | 30 | 2025-01-19 | 1 | aucune_echeance |
| 2025 | 30 | 2025-04-08 | 1 | aucune_echeance |
| 2025 | 30 | 2025-05-30 | 1 | aucune_echeance |
| 2025 | 30 | 2025-10-07 | 1 | aucune_echeance |
| 2025 | 30 | 2025-10-10 | 1 | aucune_echeance |
| 2025 | 30 | 2025-10-17 | 1 | aucune_echeance |
| 2025 | 30 | 2025-10-26 | 1 | aucune_echeance |
| 2025 | 34 | 2025-01-10 | 2 | aucune_echeance |
| 2025 | 34 | 2025-01-11 | 1 | aucune_echeance |
| 2025 | 34 | 2025-01-18 | 1 | aucune_echeance |
| 2025 | 34 | 2025-01-19 | 1 | aucune_echeance |
| 2025 | 34 | 2025-02-05 | 1 | aucune_echeance |
| 2025 | 34 | 2025-02-06 | 2 | aucune_echeance |
| 2025 | 34 | 2025-02-07 | 1 | aucune_echeance |
| 2025 | 34 | 2025-02-16 | 1 | aucune_echeance |
| 2025 | 34 | 2025-02-26 | 1 | aucune_echeance |
| 2025 | 34 | 2025-03-01 | 1 | aucune_echeance |
| 2025 | 34 | 2025-03-04 | 2 | aucune_echeance |
| 2025 | 34 | 2025-03-05 | 1 | aucune_echeance |
| 2025 | 34 | 2025-03-17 | 1 | aucune_echeance |
| 2025 | 34 | 2025-04-10 | 1 | aucune_echeance |
| 2025 | 34 | 2025-05-06 | 1 | aucune_echeance |
| 2025 | 34 | 2025-05-08 | 1 | aucune_echeance |
| 2025 | 34 | 2025-05-15 | 1 | aucune_echeance |
| 2025 | 34 | 2025-05-20 | 1 | aucune_echeance |
| 2025 | 34 | 2025-05-27 | 2 | aucune_echeance |
| 2025 | 34 | 2025-05-28 | 2 | aucune_echeance |
| 2025 | 34 | 2025-10-02 | 2 | J+2_seul |
| 2025 | 34 | 2025-10-06 | 3 | aucune_echeance |
| 2025 | 34 | 2025-10-07 | 1 | aucune_echeance |
| 2025 | 34 | 2025-10-09 | 2 | aucune_echeance |
| 2025 | 34 | 2025-10-10 | 2 | aucune_echeance |
| 2025 | 34 | 2025-10-11 | 2 | aucune_echeance |
| 2025 | 34 | 2025-10-12 | 2 | aucune_echeance |
| 2025 | 34 | 2025-10-13 | 1 | aucune_echeance |
| 2025 | 34 | 2025-10-17 | 1 | aucune_echeance |
| 2025 | 34 | 2025-10-18 | 3 | aucune_echeance |
| 2025 | 34 | 2025-10-19 | 1 | aucune_echeance |
| 2025 | 34 | 2025-10-20 | 2 | aucune_echeance |
| 2025 | 34 | 2025-10-25 | 1 | aucune_echeance |
| 2025 | 34 | 2025-10-26 | 1 | aucune_echeance |
| 2025 | 34 | 2025-10-27 | 3 | aucune_echeance |
| 2025 | 34 | 2025-10-28 | 2 | aucune_echeance |
| 2025 | 34 | 2025-10-30 | 1 | aucune_echeance |
| 2025 | 34 | 2025-11-01 | 1 | aucune_echeance |
| 2025 | 34 | 2025-11-03 | 1 | aucune_echeance |
| 2025 | 34 | 2025-11-11 | 1 | aucune_echeance |
| 2025 | 34 | 2025-11-18 | 1 | aucune_echeance |
| 2025 | 34 | 2025-11-19 | 1 | aucune_echeance |
| 2025 | 34 | 2025-11-23 | 1 | aucune_echeance |
| 2025 | 34 | 2025-11-27 | 1 | aucune_echeance |
| 2025 | 34 | 2025-11-28 | 3 | aucune_echeance |
| 2025 | 34 | 2025-11-29 | 1 | aucune_echeance |
| 2025 | 34 | 2025-11-30 | 1 | aucune_echeance |
| 2025 | 34 | 2025-12-01 | 2 | aucune_echeance |
| 2025 | 34 | 2025-12-14 | 1 | aucune_echeance |
| 2025 | 46 | 2025-04-11 | 1 | aucune_echeance |
| 2025 | 48 | 2025-02-15 | 1 | aucune_echeance |
| 2025 | 48 | 2025-03-05 | 1 | aucune_echeance |
| 2025 | 48 | 2025-03-07 | 1 | aucune_echeance |
| 2025 | 48 | 2025-04-01 | 1 | aucune_echeance |
| 2025 | 48 | 2025-04-05 | 1 | aucune_echeance |
| 2025 | 48 | 2025-05-16 | 1 | aucune_echeance |
| 2025 | 48 | 2025-10-02 | 1 | J+2_seul |
| 2025 | 48 | 2025-10-08 | 1 | aucune_echeance |
| 2025 | 48 | 2025-10-09 | 1 | aucune_echeance |
| 2025 | 48 | 2025-10-17 | 1 | aucune_echeance |
| 2025 | 65 | 2025-02-20 | 1 | aucune_echeance |
| 2025 | 65 | 2025-03-06 | 1 | aucune_echeance |
| 2025 | 66 | 2025-03-22 | 1 | aucune_echeance |
| 2025 | 66 | 2025-03-29 | 2 | aucune_echeance |
| 2025 | 66 | 2025-03-31 | 1 | aucune_echeance |
| 2025 | 66 | 2025-10-05 | 1 | aucune_echeance |
| 2025 | 66 | 2025-10-08 | 1 | aucune_echeance |
| 2025 | 66 | 2025-10-23 | 1 | aucune_echeance |
| 2025 | 66 | 2025-10-28 | 1 | aucune_echeance |
| 2025 | 66 | 2025-11-15 | 1 | aucune_echeance |
| 2025 | 66 | 2025-11-19 | 1 | aucune_echeance |
| 2025 | 66 | 2025-11-23 | 1 | aucune_echeance |
| 2025 | 66 | 2025-11-28 | 1 | aucune_echeance |
| 2025 | 66 | 2025-12-31 | 1 | aucune_echeance |
| 2025 | 81 | 2025-04-01 | 1 | aucune_echeance |
| 2025 | 82 | 2025-03-31 | 1 | aucune_echeance |
| 2025 | 82 | 2025-05-02 | 1 | aucune_echeance |
| 2025 | 82 | 2025-10-15 | 1 | aucune_echeance |

## Indicateurs : numérateurs et dénominateurs

| Indicateur | Numérateur | Dénominateur | Formule / unité |
|---|---|---|---|
| jours_feu_hors_cohorte | Nombre de clés de E privé de (A ∩ B) | Sans objet : indicateur de volume | Nombre de journées départementales avec feu exclues de la cohorte commune |
| taux_jours_feu_hors_cohorte_pct (complément) | Nombre de clés de E privé de (A ∩ B) | Nombre de clés de E | Part des journées avec feu hors cohorte |
| taux_disponibilite_meteo_pct | Nombre de couples département-jour attendus avec J+1 ET J+2 valides | Nombre de couples département-jour où la publication des deux échéances est attendue selon le calendrier officiel de diffusion | Disponibilité sur la grille attendue ; ne pas calculer tant que cette grille n'est pas formellement définie |
| couverture_conditionnelle_pct (par horizon h et seuil s) | Nombre de clés de A ∩ B avec feu et niveau_h supérieur ou égal à s | Nombre de clés de A ∩ B avec feu | Part des journées avec feu communes couvertes par le seuil ; afficher le dénominateur |
| taux_couverture_cohorte_feu_pct | Nombre de clés de A ∩ B | Nombre de clés de E | Part des journées avec feu BDIFF disposant simultanément des deux échéances |

**Précision :** taux_disponibilite_meteo_pct porte sur toutes les journées de la grille de publication attendue, avec ou sans feu. Il ne doit pas être confondu avec taux_couverture_cohorte_feu_pct, qui porte uniquement sur les journées BDIFF avec feu. Le calendrier attendu doit être défini à partir des règles de publication et de la période réellement couverte, pas par simple extrapolation des dates min/max.

## Traçabilité et limites

- Le script scripts/auditer_intersection_j1_j2.py recharge les sources et réutilise les contrôles SHA-256 des fonctions charger_previsions et charger_evenements.
- BDIFF : SHA-256 2024 a4b7bf48dc032788746247f6f4878740b80f43da4b2a3a28c86024bf9259d6a2 ; 2025 393f8bc15f9c4c803310eefd94c86cad9b81e8a5bd08440a3f5f1403b5e3f282.
- Météo des forêts : SHA-256 2024 e3f87c1161d30491ec7ad1149e0f8b5b89f3974d34dd3200ecbdd1d41b55115f ; 2025 dd0a095b1744ef7c64e44c3a4560bdbd75a1fcbd7292942ba539c85b79e9e3b0.
- Hypothèse temporelle toujours à confirmer : la colonne d'archive date est interprétée comme date de référence, puis J+1 = date + 1 jour et J+2 = date + 2 jours.
- Le manifeste BDIFF indique que la vérification TLS du téléchargement n'est pas confirmée ; l'empreinte prouve l'intégrité du fichier versionné, pas à elle seule l'authenticité du transport initial.
- Le produit Météo des forêts est une information de sensibilisation du public ; les scénarios restent pédagogiques et ne constituent pas une doctrine opérationnelle SDIS.

Exécution UTC : 2026-11-28T08:30:12.576361+00:00

Détail exhaustif : intersection_j1_j2_feux.csv.
