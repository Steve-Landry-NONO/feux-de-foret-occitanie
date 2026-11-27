"""Tests du script de contrôle qualité Météo des forêts (ticket #14).

Ils utilisent un petit fichier synthétique : ils vérifient le contrôle,
pas les données réelles de Météo-France.
"""
import gzip
import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.controler_qualite_mdf import code_dep, controler, jour, statut

OCC = ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"]


def fichier(lignes, sep=","):
    entete = sep.join(["date", "num_dep", "niveau_j1", "niveau_j2", "nom_dep"])
    texte = "\n".join([entete] + [sep.join(l) for l in lignes]) + "\n"
    f = tempfile.NamedTemporaryFile(suffix=".csv.gz", delete=False)
    f.write(gzip.compress(texte.encode("utf-8")))
    f.close()
    return f.name


class TestControleMdf(unittest.TestCase):
    def test_normalisations(self):
        self.assertEqual(code_dep("9"), "09")
        self.assertEqual(code_dep("2a"), "2A")
        self.assertEqual(str(jour("2024-06-03T14:50:06Z")), "2024-06-03")
        self.assertIsNone(jour("inconnu"))

    def test_fichier_conforme_avec_point_virgule(self):
        lignes = [["2026-06-01T14:50:00Z", d, "2", "1", "x"] for d in OCC]
        p = fichier(lignes, sep=";")
        r = controler(p, {Path(p).name: hashlib.sha256(Path(p).read_bytes()).hexdigest()})
        self.assertEqual(r["separateur"], ";")
        self.assertEqual(r["MDF-06_jours_population_incomplete"], {})
        self.assertEqual(statut(r), "CONFORME_SUR_REGLES_BLOQUANTES")

    def test_detecte_doublon_hors_domaine_et_departement_manquant(self):
        lignes = [["2024-06-03T14:50:00Z", d.lstrip("0"), "1", "1", "x"] for d in OCC[1:]]
        lignes.append(["2024-06-03T14:50:00Z", "31", "5", "1", "x"])
        r = controler(fichier(lignes), None)
        self.assertEqual(r["MDF-04_doublons_dep_jour"], 1)
        self.assertEqual(r["MDF-05_niveau_j1_hors_domaine"], 1)
        self.assertEqual(r["MDF-06_jours_population_incomplete"], {"2024-06-03": ["09"]})
        self.assertEqual(statut(r), "ECHEC")

    def test_manifeste_absent_ou_incomplet(self):
        p = fichier([["2026-06-01", d, "2", "1", "x"] for d in OCC])
        self.assertEqual(statut(controler(p, None)), "NON_CONTROLE")
        self.assertEqual(statut(controler(p, {})), "ECHEC")
        self.assertEqual(statut(controler(p, {Path(p).name: None})), "ECHEC")
        self.assertEqual(statut(controler(p, {Path(p).name: "0" * 64})), "ECHEC")

    def test_population_vide(self):
        for lignes in ([], [["2026-06-01", "75", "2", "1", "x"]]):
            with self.subTest(lignes=lignes):
                self.assertEqual(statut(controler(fichier(lignes), None)), "ECHEC")

    def test_calendrier_invalide(self):
        p = fichier([["invalide", d, "2", "1", "x"] for d in OCC])
        self.assertEqual(statut(controler(p, None)), "ECHEC")

    def test_niveaux_vides(self):
        for i in (2, 3):
            lignes = [["2026-06-01", d, "2", "1", "x"] for d in OCC]
            lignes[0][i] = " "
            p = fichier(lignes)
            manifest = {Path(p).name: hashlib.sha256(Path(p).read_bytes()).hexdigest()}
            self.assertEqual(statut(controler(p, manifest)), "ECHEC")


if __name__ == "__main__":
    unittest.main()
