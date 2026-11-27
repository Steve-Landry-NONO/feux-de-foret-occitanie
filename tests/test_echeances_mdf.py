"""Tests du décalage calendaire MdF : aucun jour d'incendie ne doit utiliser la
prévision publiée le jour même lorsqu'on simule une décision anticipée.
"""
import unittest
from datetime import date
from scripts.valider_echeances_mdf import previsions_ligne

class TestEcheances(unittest.TestCase):
    def test_exemple_haute_garonne(self):
        values=previsions_ligne({
            "date":"2025-06-15","num_dep":"31",
            "niveau_j1":"3","niveau_j2":"4"})
        self.assertEqual(values[0]["date_reference"],"2025-06-15")
        self.assertEqual(values[0]["date_validite"],"2025-06-16")
        self.assertEqual(values[0]["echeance"],"J+1")
        self.assertEqual(values[0]["niveau"],"3")
        self.assertEqual(values[1]["date_validite"],"2025-06-17")
        self.assertEqual(values[1]["echeance"],"J+2")
        self.assertEqual(values[1]["niveau"],"4")

    def test_changement_mois_et_annee(self):
        values=previsions_ligne({
            "date":"2024-12-31","num_dep":"9",
            "niveau_j1":"1","niveau_j2":"2"})
        self.assertEqual(values[0]["date_validite"],"2025-01-01")
        self.assertEqual(values[1]["date_validite"],"2025-01-02")
        self.assertEqual(values[0]["departement"],"09")

    def test_rejet_niveau_inconnu(self):
        with self.assertRaises(ValueError):
            previsions_ligne({"date":"2025-06-15","num_dep":"31",
                              "niveau_j1":"0","niveau_j2":"4"})

if __name__=="__main__":
    unittest.main()
