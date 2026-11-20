# Tentative de collecte officielle BDIFF

Source : https://bdiff.agriculture.gouv.fr/incendies ; méthode : formulaire public GET puis lien /incendies/zip.
**Attention :** l'instance GitHub Actions rencontre une anomalie de chaîne TLS sur le site. La lecture utilise ici un contexte sans vérification de certificat ; **le transport n'est donc pas authentifié** et les fichiers restent en quarantaine tant qu'un contrôle indépendant n'est pas réalisé.

- Champ Région Occitanie détecté : valeur HTML '76'
## 2024

- Recherche HTTP 200, URL finale https://bdiff.agriculture.gouv.fr/incendies?if%5BdateAlerteDeb%5D%5Bdate%5D=01%2F01%2F2024&if%5BdateAlerteDeb%5D%5Btime%5D%5Bhour%5D=0&if%5BdateAlerteDeb%5D%5Btime%5D%5Bminute%5D=0&if%5BdateAlerteFin%5D%5Bdate%5D=31%2F12%2F2024&if%5BdateAlerteFin%5D%5Btime%5D%5Bhour%5D=23&if%5BdateAlerteFin%5D%5Btime%5D%5Bminute%5D=59&if%5Bra%5D=76&if%5Bsubmit%5D=
- Nombre indiqué sur page : 413

- ZIP : HTTP 200, content-type application/zip, taille 602878 octets
- Contenu observé : 

~~~json
{
  "fichiers": [
    "Incendies.csv",
    "Mention légales.pdf",
    "Définitions.pdf"
  ],
  "csv": "Incendies.csv",
  "pdfs": [
    "Mention légales.pdf",
    "Définitions.pdf"
  ],
  "criteres_export": "\"Critères de sélection =>\";\"Date de première alerte, de : 2024-01-01 00:00:00\";\"Date de première alerte, jusqu'à : 2024-12-31 23:59:00\";\"Région administrative : OCCITANIE\";\"Type de feu : F\"",
  "champs": [
    "Année",
    "Numéro",
    "Département",
    "Code INSEE",
    "Nom de la commune",
    "Date de première alerte",
    "Surface parcourue (m2)",
    "Surface forêt (m2)",
    "Surface maquis garrigues (m2)",
    "Autres surfaces naturelles hors forêt (m2)",
    "Surfaces agricoles (m2)",
    "Autres surfaces (m2)",
    "Surface autres terres boisées (m2)",
    "Surfaces non boisées naturelles (m2)",
    "Surfaces non boisées artificialisées (m2)",
    "Surfaces non boisées (m2)",
    "Précision des surfaces",
    "Type de peuplement",
    "Nature",
    "Décès ou bâtiments touchés",
    "Nombre de décès",
    "Nombre de bâtiments totalement détruits",
    "Nombre de bâtiments partiellement détruits",
    "Précision de la donnée"
  ],
  "separateur": ";",
  "lignes": 413,
  "annees": [
    "2024"
  ],
  "departements_presents": [
    "09",
    "11",
    "12",
    "30",
    "31",
    "34",
    "46",
    "48",
    "66",
    "81"
  ],
  "dates_alerte_hors_annee": 0,
  "validation_structure": "OK"
}
~~~

- SHA-256 : a4b7bf48dc032788746247f6f4878740b80f43da4b2a3a28c86024bf9259d6a2
## 2025

- Recherche HTTP 200, URL finale https://bdiff.agriculture.gouv.fr/incendies?if%5BdateAlerteDeb%5D%5Bdate%5D=01%2F01%2F2025&if%5BdateAlerteDeb%5D%5Btime%5D%5Bhour%5D=0&if%5BdateAlerteDeb%5D%5Btime%5D%5Bminute%5D=0&if%5BdateAlerteFin%5D%5Bdate%5D=31%2F12%2F2025&if%5BdateAlerteFin%5D%5Btime%5D%5Bhour%5D=23&if%5BdateAlerteFin%5D%5Btime%5D%5Bminute%5D=59&if%5Bra%5D=76&if%5Bsubmit%5D=
- Nombre indiqué sur page : 472

- ZIP : HTTP 200, content-type application/zip, taille 604702 octets
- Contenu observé : 

~~~json
{
  "fichiers": [
    "Incendies.csv",
    "Mention légales.pdf",
    "Définitions.pdf"
  ],
  "csv": "Incendies.csv",
  "pdfs": [
    "Mention légales.pdf",
    "Définitions.pdf"
  ],
  "criteres_export": "\"Critères de sélection =>\";\"Date de première alerte, de : 2025-01-01 00:00:00\";\"Date de première alerte, jusqu'à : 2025-12-31 23:59:00\";\"Région administrative : OCCITANIE\";\"Type de feu : F\"",
  "champs": [
    "Année",
    "Numéro",
    "Département",
    "Code INSEE",
    "Nom de la commune",
    "Date de première alerte",
    "Surface parcourue (m2)",
    "Surface forêt (m2)",
    "Surface maquis garrigues (m2)",
    "Autres surfaces naturelles hors forêt (m2)",
    "Surfaces agricoles (m2)",
    "Autres surfaces (m2)",
    "Surface autres terres boisées (m2)",
    "Surfaces non boisées naturelles (m2)",
    "Surfaces non boisées artificialisées (m2)",
    "Surfaces non boisées (m2)",
    "Précision des surfaces",
    "Type de peuplement",
    "Nature",
    "Décès ou bâtiments touchés",
    "Nombre de décès",
    "Nombre de bâtiments totalement détruits",
    "Nombre de bâtiments partiellement détruits",
    "Précision de la donnée"
  ],
  "separateur": ";",
  "lignes": 472,
  "annees": [
    "2025"
  ],
  "departements_presents": [
    "09",
    "11",
    "12",
    "30",
    "31",
    "32",
    "34",
    "46",
    "48",
    "65",
    "66",
    "81",
    "82"
  ],
  "dates_alerte_hors_annee": 0,
  "validation_structure": "OK"
}
~~~

- SHA-256 : 393f8bc15f9c4c803310eefd94c86cad9b81e8a5bd08440a3f5f1403b5e3f282

**Statut : ZIP officiels récupérés depuis le portail et contrôlés (schéma, année, zone, annexes) ; certificat TLS non vérifié sur le runner, réserve de provenance à lever indépendamment.**
