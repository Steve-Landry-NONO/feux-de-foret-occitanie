# Incendies BDIFF Occitanie — profilage des exports 2024 et 2025

**Source : ZIP du portail officiel BDIFF, filtrés sur Occitanie et « Type de feu : F ».**
**Réserve :** le certificat du portail n'a pas été validé par le runner ; l'authenticité du transport reste à corroborer.

## 1. Qualité des événements extraits

| Année | Événements | Dont Haute-Garonne (31) | Départements avec feux | Première alerte | Dernière alerte | Doublons n° BDIFF |
|---|---:|---:|---:|---|---|---:|
| 2024 | 413 | 1 | 10 | 2024-01-01 | 2024-12-29 | 0 |
| 2025 | 472 | 4 | 13 | 2025-01-10 | 2025-12-31 | 0 |

## 2. Jointure exploratoire avec les archives météo (département × date brute)

| Année | Jours départementaux avec feu | Correspondance météo même date | Sans correspondance | Jours avec feu (31) | Correspondance météo (31) |
|---|---:|---:|---:|---:|---:|
| 2024 | 289 | 161 | 128 | 1 | 0 |
| 2025 | 340 | 208 | 132 | 4 | 4 |

**Ne pas interpréter ces correspondances comme une sensibilité d'un seuil de danger :** nous n'avons pas fixé la date de validité des prévisions J+1/J+2. Les archives météo n'existent que sur une partie de l'année ; les feux hors saison ne représentent pas une erreur de jointure.

## 3. Traçabilité et limites

- [Manifestes ZIP, SHA-256, filtres et état TLS](../../datasets/public/bdiff_officiel/manifest.json).
- [Rapport JSON détaillé](profilage_bdiff_officiel_v1.json) : colonnes, nombres par département, réserves.
- Les originaux contiennent un CSV, un PDF de mentions légales et un PDF de définitions ; ne pas modifier les ZIP.
- Pour Q1, les surfaces forestières IGN restent nécessaires et les communes devront être alignées aux millésimes INSEE.
- Pour Q2/Q3, confirmer la sémantique J1/J2 et l'exhaustivité de chaque campagne, avant de calculer les KPI.

**Relectures à obtenir :** Maeva (BDIFF et licences), Chantal (qualité), Stéphane (pipeline), Ludovic (KPI).
