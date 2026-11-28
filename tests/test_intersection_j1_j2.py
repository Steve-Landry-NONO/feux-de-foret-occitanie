"""Tests unitaires de l'intersection des journées départementales avec feu."""
import unittest
from collections import Counter

from scripts.auditer_intersection_j1_j2 import calculer_intersections


class TestIntersectionJ1J2(unittest.TestCase):
    def test_intersection_reelle_et_ecarts_non_deduits_du_minimum(self):
        index = {
            ("31", "2025-06-01", "J+1"): 3,
            ("31", "2025-06-01", "J+2"): 2,
            ("31", "2025-06-02", "J+1"): 2,
            ("31", "2025-06-03", "J+2"): 4,
        }
        feux = Counter({
            ("31", "2025-06-01"): 2,
            ("31", "2025-06-02"): 1,
            ("31", "2025-06-03"): 1,
            ("31", "2025-06-04"): 1,
        })

        synthese, details = calculer_intersections(index, feux, annees=(2025,))
        r = synthese[0]

        self.assertEqual(r["jours_feu_total_E"], 4)
        self.assertEqual(r["jours_feu_avec_J1_A"], 2)
        self.assertEqual(r["jours_feu_avec_J2_B"], 2)
        self.assertEqual(r["intersection_A_inter_B"], 1)
        self.assertEqual(r["J1_sans_J2"], 1)
        self.assertEqual(r["J2_sans_J1"], 1)
        self.assertEqual(r["sans_J1_ni_J2"], 1)
        self.assertEqual(r["jours_feu_hors_cohorte"], 3)
        self.assertEqual(len(details), 4)

    def test_une_journee_departementale_comptee_une_fois(self):
        index = {
            ("11", "2024-07-01", "J+1"): 2,
            ("11", "2024-07-01", "J+2"): 3,
        }
        feux = Counter({("11", "2024-07-01"): 7})
        synthese, _ = calculer_intersections(index, feux, annees=(2024,))
        self.assertEqual(synthese[0]["jours_feu_total_E"], 1)
        self.assertEqual(synthese[0]["intersection_A_inter_B"], 1)


if __name__ == "__main__":
    unittest.main()
