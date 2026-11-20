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

- SHA-256 : a7d5dc57706146adbcf271c71acc2bca381e247d0d475c50729025286b27ee11
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

- SHA-256 : 78e6dc6c306bc8a6beef1f69df9d3efaf1fc071387806f723d1441f5aa38d063

**Statut : fichiers téléchargés techniquement, à mettre en quarantaine avant publication.**
