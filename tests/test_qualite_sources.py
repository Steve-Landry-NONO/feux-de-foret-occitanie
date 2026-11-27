"""Tests des transformations minimales avant calcul de KPI.

Ils portent sur les dates et les codes des fichiers réellement versionnés.
Ils ne valent pas validation de la sémantique des prévisions Météo-France.
"""
import unittest
from scripts.profiler_et_joindre_donnees import jour, dep, meteo


class TestClesEtQualite(unittest.TestCase):
    def test_date_iso(self):
        self.assertEqual(jour("2024-06-03"), "2024-06-03")
        self.assertEqual(jour("03/06/2024"), "2024-06-03")
        self.assertIsNone(jour("valeur inconnue"))

    def test_codes_departement_en_texte(self):
        self.assertEqual(dep("9"), "09")
        self.assertEqual(dep("31"), "31")
        self.assertEqual(dep("2A"), "2A")

    def test_meteo_reelle_et_unicite(self):
        profil, index, _ = meteo()
        self.assertEqual(len(profil), 3)
        for ligne in profil:
            self.assertEqual(ligne["departements_occitanie"], 13)
            self.assertEqual(ligne["dates_invalides"], 0)
            self.assertEqual(ligne["doublons_depart_jour"], 0)
            self.assertGreater(ligne["dates_distinctes"], 0)
            self.assertTrue(ligne["date_min"])
            self.assertTrue(ligne["date_max"])
        self.assertIn(("2024", "31", "2024-06-03"), index)
        self.assertIn(("2025", "31", "2025-06-03"), index)


if __name__ == "__main__":
    unittest.main()
