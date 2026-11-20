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
  "premieres_lignes_csv": [
    "\"Nombre d'incendies suivant les critères de sélection : 413\"",
    "\"Critères de sélection =>\";\"Date de première alerte, de : 2024-01-01 00:00:00\";\"Date de première alerte, jusqu'à : 2024-12-31 23:59:00\";\"Région administrative : OCCITANIE\";\"Type de feu : F\"",
    "Année;Numéro;Département;\"Code INSEE\";\"Nom de la commune\";\"Date de première alerte\";\"Surface parcourue (m2)\";\"Surface forêt (m2)\";\"Surface maquis garrigues (m2)\";\"Autres surfaces naturelles hors forêt (m2)\";\"Surfaces agricoles (m2)\";\"Autres surfaces (m2)\";\"Surface autres terres boisées (m2)\";\"Surfaces non boisées naturelles (m2)\";\"Surfaces non boisées artificialisées (m2)\";\"Surfaces non boisées (m2)\";\"Précision des surfaces\";\"Type de peuplement\";Nature;\"Décès ou bâtiments touchés\";\"Nombre de décès\";\"Nombre de bâtiments totalement détruits\";\"Nombre de bâtiments partiellement détruits\";\"Précision de la donnée\"",
    "2024;5;\"66\";\"66043\";\"Casteil\";\"2024-01-01 12:02:00\";2000;2000;0;0;0;0;;;;;\"Estimées\";;\"Involontaire (particulier)\";\"Non\";;;;\"\"",
    "2024;20474;\"11\";\"11322\";\"Roquefort-des-Corbières\";\"2024-01-01 20:42:00\";100;10;90;0;0;0;;;;;\"Mesurées\";\"1\";;\"Non\";;;;\"\""
  ],
  "champs": [
    "Nombre d'incendies suivant les critères de sélection : 413"
  ],
  "separateur": ";",
  "lignes": 415,
  "extrait_annees": [],
  "extrait_departements": [],
  "premiere_ligne_extrait": {
    "noms_champs": [
      "Nombre d'incendies suivant les critères de sélection : 413",
      null
    ]
  }
}
~~~

- SHA-256 : 4c8181dad5a210adfecd64935235fafe66c3f2eb2cc3de21675809a113ae9222
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
  "premieres_lignes_csv": [
    "\"Nombre d'incendies suivant les critères de sélection : 472\"",
    "\"Critères de sélection =>\";\"Date de première alerte, de : 2025-01-01 00:00:00\";\"Date de première alerte, jusqu'à : 2025-12-31 23:59:00\";\"Région administrative : OCCITANIE\";\"Type de feu : F\"",
    "Année;Numéro;Département;\"Code INSEE\";\"Nom de la commune\";\"Date de première alerte\";\"Surface parcourue (m2)\";\"Surface forêt (m2)\";\"Surface maquis garrigues (m2)\";\"Autres surfaces naturelles hors forêt (m2)\";\"Surfaces agricoles (m2)\";\"Autres surfaces (m2)\";\"Surface autres terres boisées (m2)\";\"Surfaces non boisées naturelles (m2)\";\"Surfaces non boisées artificialisées (m2)\";\"Surfaces non boisées (m2)\";\"Précision des surfaces\";\"Type de peuplement\";Nature;\"Décès ou bâtiments touchés\";\"Nombre de décès\";\"Nombre de bâtiments totalement détruits\";\"Nombre de bâtiments partiellement détruits\";\"Précision de la donnée\"",
    "2025;41;\"34\";\"34065\";\"Cazedarnes\";\"2025-01-10 11:22:00\";79;79;0;0;0;0;;;;;\"Mesurées\";\"1\";\"Malveillance\";\"Non\";;;;\"\"",
    "2025;37;\"34\";\"34301\";\"Sète\";\"2025-01-10 21:48:00\";98;98;0;0;0;0;;;;;\"Mesurées\";\"1\";\"Malveillance\";\"Non\";;;;\"\""
  ],
  "champs": [
    "Nombre d'incendies suivant les critères de sélection : 472"
  ],
  "separateur": ";",
  "lignes": 474,
  "extrait_annees": [],
  "extrait_departements": [],
  "premiere_ligne_extrait": {
    "noms_champs": [
      "Nombre d'incendies suivant les critères de sélection : 472",
      null
    ]
  }
}
~~~

- SHA-256 : 6aae450a69230eff21e75d54f0c57377d370e5c2f0376b4702d012b2ebd8ab8e

**Statut : fichiers téléchargés techniquement, à mettre en quarantaine avant publication.**
