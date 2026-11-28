#!/usr/bin/env python3
"""Audit explicite des ensembles de journées avec feu disposant de J+1 et J+2.

Le calcul repart des archives versionnées : les fonctions de chargement vérifient
les SHA-256 des fichiers BDIFF et Météo des forêts avant de construire les clés.
Un jour est identifié par (code département, date de première alerte / validité).
"""
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.calculer_scenarios_q2_q3 import (
    BDIFF,
    MDF,
    OUT,
    charger_evenements,
    charger_previsions,
)


def calculer_intersections(index, events, annees=(2024, 2025)):
    """Calcule E, A, B, A∩B et les différences d'ensembles."""
    jours_feu = {
        (str(departement).zfill(2), jour)
        for (departement, jour), nombre in events.items()
        if nombre > 0
    }
    synthese = []
    details = []

    for annee in annees:
        prefixe = str(annee) + "-"
        E = {cle for cle in jours_feu if cle[1].startswith(prefixe)}
        A = {cle for cle in E if (cle[0], cle[1], "J+1") in index}
        B = {cle for cle in E if (cle[0], cle[1], "J+2") in index}
        commun = A & B
        j1_seul = A - B
        j2_seul = B - A
        aucune = E - (A | B)
        hors_cohorte = E - commun
        taux = round(100 * len(commun) / len(E), 2) if E else None

        synthese.append({
            "annee": annee,
            "jours_feu_total_E": len(E),
            "jours_feu_avec_J1_A": len(A),
            "jours_feu_avec_J2_B": len(B),
            "intersection_A_inter_B": len(commun),
            "J1_sans_J2": len(j1_seul),
            "J2_sans_J1": len(j2_seul),
            "sans_J1_ni_J2": len(aucune),
            "jours_feu_hors_cohorte": len(hors_cohorte),
            "taux_jours_feu_dans_cohorte_commune_pct": taux,
        })

        for departement, jour in sorted(E):
            j1 = (departement, jour) in A
            j2 = (departement, jour) in B
            if j1 and j2:
                statut = "J+1_et_J+2"
            elif j1:
                statut = "J+1_seul"
            elif j2:
                statut = "J+2_seul"
            else:
                statut = "aucune_echeance"
            details.append({
                "annee": annee,
                "departement": departement,
                "jour": jour,
                "nb_feux_bdiff_type_f": events[(departement, jour)],
                "j1_disponible": int(j1),
                "j2_disponible": int(j2),
                "dans_intersection": int((departement, jour) in commun),
                "statut": statut,
            })

        # Invariants d'ensembles : pas de déduction par minimum des effectifs.
        assert len(A | B) == len(A) + len(B) - len(commun)
        assert len(E) == len(commun) + len(j1_seul) + len(j2_seul) + len(aucune)
        assert hors_cohorte == j1_seul | j2_seul | aucune

    return synthese, details


def ecrire_preuves(synthese, details):
    OUT.mkdir(parents=True, exist_ok=True)
    chemin_csv = OUT / "intersection_j1_j2_feux.csv"
    champs = [
        "annee", "departement", "jour", "nb_feux_bdiff_type_f",
        "j1_disponible", "j2_disponible", "dans_intersection", "statut",
    ]
    with chemin_csv.open("w", encoding="utf-8", newline="") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=champs)
        writer.writeheader()
        writer.writerows(details)

    meta_bdiff = json.loads(BDIFF.read_text(encoding="utf-8"))
    meta_mdf = json.loads(MDF.read_text(encoding="utf-8"))
    sha_bdiff = {str(x["annee"]): x["sha256"] for x in meta_bdiff["extractions"]}
    sha_mdf = {str(x["annee_archive"]): x["sha256"] for x in meta_mdf["extractions"]}

    lignes = [
        "# Preuve de l'intersection des journées avec feu — J+1 ET J+2",
        "",
        "**Calcul reproductible sur les fichiers versionnés ; les effectifs sont des couples département × jour, pas des dates calendaires uniques.**",
        "",
        "## Définition des ensembles",
        "",
        "- **E** : ensemble de tous les couples (département, jour) avec au moins un feu BDIFF de type F, agrégés depuis la date de première alerte.",
        "- **A** : sous-ensemble de E pour lequel une prévision J+1 est disponible à la date de validité calculée.",
        "- **B** : sous-ensemble de E pour lequel une prévision J+2 est disponible à la date de validité calculée.",
        "- **A ∩ B** : intersection calculée directement par égalité des clés (département, jour) présentes dans A et B.",
        "- **E privé de (A ∩ B)** : journées avec feu hors de la cohorte commune.",
        "",
        "L'intersection n'est jamais estimée par le minimum des deux effectifs. Les écarts A privé de B, B privé de A et E privé de (A union B) sont calculés séparément.",
        "",
        "## Résultats calculés",
        "",
        "| Année | E : tous les jours feu | A : J+1 | B : J+2 | A ∩ B | J+1 seul | J+2 seul | Ni J+1 ni J+2 | E hors cohorte | Part commune / E |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in synthese:
        taux = "n.d." if r["taux_jours_feu_dans_cohorte_commune_pct"] is None else str(r["taux_jours_feu_dans_cohorte_commune_pct"]) + " %"
        lignes.append(
            f'| {r["annee"]} | {r["jours_feu_total_E"]} | {r["jours_feu_avec_J1_A"]} | '
            f'{r["jours_feu_avec_J2_B"]} | {r["intersection_A_inter_B"]} | '
            f'{r["J1_sans_J2"]} | {r["J2_sans_J1"]} | {r["sans_J1_ni_J2"]} | '
            f'{r["jours_feu_hors_cohorte"]} | {taux} |'
        )

    lignes += [
        "",
        "## Détail des journées non communes",
        "",
        "Le CSV détaille chaque clé. J+1_seul appartient à A mais pas à B ; J+2_seul appartient à B mais pas à A ; aucune_echeance n'appartient ni à A ni à B.",
        "",
    ]
    ecarts = [x for x in details if x["statut"] != "J+1_et_J+2"]
    if ecarts:
        lignes += [
            "| Année | Département | Jour | Feux BDIFF type F | Statut |",
            "|---:|---:|---|---:|---|",
        ]
        for x in ecarts:
            lignes.append(
                f'| {x["annee"]} | {x["departement"]} | {x["jour"]} | '
                f'{x["nb_feux_bdiff_type_f"]} | {x["statut"]} |'
            )
    else:
        lignes.append("Aucun écart : toutes les journées avec feu disposent des deux échéances.")

    lignes += [
        "",
        "## Indicateurs : numérateurs et dénominateurs",
        "",
        "| Indicateur | Numérateur | Dénominateur | Formule / unité |",
        "|---|---|---|---|",
        "| jours_feu_hors_cohorte | Nombre de clés de E privé de (A ∩ B) | Sans objet : indicateur de volume | Nombre de journées départementales avec feu exclues de la cohorte commune |",
        "| taux_jours_feu_hors_cohorte_pct (complément) | Nombre de clés de E privé de (A ∩ B) | Nombre de clés de E | Part des journées avec feu hors cohorte |",
        "| taux_disponibilite_meteo_pct | Nombre de couples département-jour attendus avec J+1 ET J+2 valides | Nombre de couples département-jour où la publication des deux échéances est attendue selon le calendrier officiel de diffusion | Disponibilité sur la grille attendue ; ne pas calculer tant que cette grille n'est pas formellement définie |",
        "| couverture_conditionnelle_pct (par horizon h et seuil s) | Nombre de clés de A ∩ B avec feu et niveau_h supérieur ou égal à s | Nombre de clés de A ∩ B avec feu | Part des journées avec feu communes couvertes par le seuil ; afficher le dénominateur |",
        "| taux_couverture_cohorte_feu_pct | Nombre de clés de A ∩ B | Nombre de clés de E | Part des journées avec feu BDIFF disposant simultanément des deux échéances |",
        "",
        "**Précision :** taux_disponibilite_meteo_pct porte sur toutes les journées de la grille de publication attendue, avec ou sans feu. Il ne doit pas être confondu avec taux_couverture_cohorte_feu_pct, qui porte uniquement sur les journées BDIFF avec feu. Le calendrier attendu doit être défini à partir des règles de publication et de la période réellement couverte, pas par simple extrapolation des dates min/max.",
        "",
        "## Traçabilité et limites",
        "",
        "- Le script scripts/auditer_intersection_j1_j2.py recharge les sources et réutilise les contrôles SHA-256 des fonctions charger_previsions et charger_evenements.",
        "- BDIFF : SHA-256 2024 " + sha_bdiff.get("2024", "non disponible") + " ; 2025 " + sha_bdiff.get("2025", "non disponible") + ".",
        "- Météo des forêts : SHA-256 2024 " + sha_mdf.get("2024", "non disponible") + " ; 2025 " + sha_mdf.get("2025", "non disponible") + ".",
        "- Hypothèse temporelle toujours à confirmer : la colonne d'archive date est interprétée comme date de référence, puis J+1 = date + 1 jour et J+2 = date + 2 jours.",
        "- Le manifeste BDIFF indique que la vérification TLS du téléchargement n'est pas confirmée ; l'empreinte prouve l'intégrité du fichier versionné, pas à elle seule l'authenticité du transport initial.",
        "- Le produit Météo des forêts est une information de sensibilisation du public ; les scénarios restent pédagogiques et ne constituent pas une doctrine opérationnelle SDIS.",
        "",
        "Exécution UTC : " + datetime.now(timezone.utc).isoformat(),
        "",
        "Détail exhaustif : intersection_j1_j2_feux.csv.",
        "",
    ]
    chemin_md = OUT / "intersection_j1_j2_feux.md"
    chemin_md.write_text("\n".join(lignes), encoding="utf-8")
    print("PASS : intersection explicite calculée et preuves CSV/Markdown produites.")


def main():
    index = charger_previsions()
    events = charger_evenements()
    synthese, details = calculer_intersections(index, events)
    ecrire_preuves(synthese, details)


if __name__ == "__main__":
    main()
