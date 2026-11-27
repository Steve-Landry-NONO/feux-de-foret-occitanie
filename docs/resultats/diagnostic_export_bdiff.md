# Inspection du portail BDIFF : recherche de l'export officiel

Cette inspection ne télécharge pas de données de tiers et ne modifie pas le portail.

- URL finale : https://bdiff.agriculture.gouv.fr/incendies
- HTTP : 200
- Taille HTML : 99114
- ATTENTION : validation du certificat HTTPS désactivée pour ce diagnostic de lecture uniquement (à ne pas utiliser pour la collecte de données).

## Formulaires (noms publics des champs)

~~~json
[
  {
    "action": null,
    "method": "get",
    "inputs": [
      {
        "id": "selectCriteres"
      },
      {
        "name": "if[idIncendie]",
        "type": "text",
        "id": "if_idIncendie"
      },
      {
        "name": "if[dateAlerteDeb][date]",
        "type": "text",
        "value": "01/01/2025",
        "id": "if_dateAlerteDeb_date"
      },
      {
        "type": "button"
      },
      {
        "name": "if[dateAlerteDeb][time][hour]",
        "id": "if_dateAlerteDeb_time_hour"
      },
      {
        "name": "if[dateAlerteDeb][time][minute]",
        "id": "if_dateAlerteDeb_time_minute"
      },
      {
        "name": "if[dateAlerteFin][date]",
        "type": "text",
        "value": "31/12/2025",
        "id": "if_dateAlerteFin_date"
      },
      {
        "type": "button"
      },
      {
        "name": "if[dateAlerteFin][time][hour]",
        "id": "if_dateAlerteFin_time_hour"
      },
      {
        "name": "if[dateAlerteFin][time][minute]",
        "id": "if_dateAlerteFin_time_minute"
      },
      {
        "name": "if[periodeDeb][jour]",
        "id": "if_periodeDeb_jour"
      },
      {
        "name": "if[periodeDeb][mois]",
        "id": "if_periodeDeb_mois"
      },
      {
        "name": "if[periodeFin][jour]",
        "id": "if_periodeFin_jour"
      },
      {
        "name": "if[periodeFin][mois]",
        "id": "if_periodeFin_mois"
      },
      {
        "name": "if[periodeAnnees][anneeDeb]",
        "id": "if_periodeAnnees_anneeDeb"
      },
      {
        "name": "if[periodeAnnees][anneeFin]",
        "id": "if_periodeAnnees_anneeFin"
      },
      {
        "name": "if[heureDeb]",
        "type": "number",
        "id": "if_heureDeb"
      },
      {
        "name": "if[heureFin]",
        "type": "number",
        "id": "if_heureFin"
      },
      {
        "name": "if[surfaceDeInc]",
        "id": "if_surfaceDeInc"
      },
      {
        "name": "if[surfaceDe]",
        "type": "text",
        "id": "if_surfaceDe"
      },
      {
        "name": "if[surfaceA]",
        "type": "text",
        "id": "if_surfaceA"
      },
      {
        "name": "if[surfaceAInc]",
        "id": "if_surfaceAInc"
      },
      {
        "name": "if[fr]",
        "type": "checkbox",
        "value": "1",
        "id": "if_fr"
      },
      {
        "name": "if[zone]",
        "id": "if_zone"
      },
      {
        "name": "if[ra]",
        "id": "if_ra"
      },
      {
        "type": "text",
        "id": "if_deprts_value_autocomplete"
      },
      {
        "name": "if[deprts][value]",
        "type": "hidden",
        "id": "if_deprts_value"
      },
      {
        "name": "if[commune]",
        "type": "text",
        "id": "if_commune"
      },
      {
        "type": "text",
        "value": "...",
        "id": "if_bbox_state"
      },
      {
        "type": "button",
        "id": "if_bbox_btn_delete"
      },
      {
        "type": "button",
        "id": "if_bbox_btn_add"
      },
      {
        "name": "if[bbox][value]",
        "type": "hidden",
        "id": "if_bbox_value"
      },
      {
        "name": "if[submit]",
        "type": "submit",
        "id": "if_submit"
      },
      {
        "name": "if[submitDefault]",
        "type": "submit",
        "id": "if_submitDefault"
      }
    ]
  }
]
~~~

## Liens associés à téléchargement / export / CSV / zip

- CSV : https://bdiff.agriculture.gouv.fr/incendies/zip

## Boutons et entrées apparentées

- Filtrer
