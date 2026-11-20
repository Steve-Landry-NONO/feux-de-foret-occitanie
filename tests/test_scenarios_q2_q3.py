"""Tests des métriques Q2–Q3 sur exemples déterministes, sans fuite de dates."""
import unittest
from collections import Counter
from scripts.calculer_scenarios_q2_q3 import evaluer, indicateurs

class TestScenariosQ2Q3(unittest.TestCase):
    def setUp(self):
        # 2 jours éligibles pour J+1/J+2, et un jour ne possédant que J+1 :
        # le dernier ne doit figurer dans AUCUN dénominateur comparatif.
        self.index={
          ("31","2025-06-05","J+1"):3,
          ("31","2025-06-05","J+2"):2,
          ("31","2025-06-06","J+1"):2,
          ("31","2025-06-06","J+2"):4,
          ("31","2025-06-07","J+1"):4,
        }
        self.feux=Counter({("31","2025-06-05"):2,
                           ("31","2025-06-06"):0,
                           ("31","2025-06-07"):1})
        self.jours=evaluer(self.index,self.feux)

    def test_cohorte_strictement_commune(self):
        self.assertEqual(len(self.jours),2)
        self.assertEqual({r["jour"] for r in self.jours},
                         {"2025-06-05","2025-06-06"})

    def test_un_jour_avec_deux_feux_compte_une_fois(self):
        r=indicateurs(self.jours,2025,"31","J+1",3)
        self.assertEqual(r["jours_avec_feu_observe"],1)
        self.assertEqual(r["feux_observes_type_f"],2)
        self.assertEqual(r["jours_feu_couverts"],1)
        self.assertEqual(r["jours_surveillance"],1)
        self.assertEqual(r["couverture_feu_pct"],100.0)

    def test_seuils_niches_et_sans_feu_observe(self):
        s2=indicateurs(self.jours,2025,"31","J+1",2)
        s3=indicateurs(self.jours,2025,"31","J+1",3)
        s4=indicateurs(self.jours,2025,"31","J+1",4)
        self.assertEqual([s2["jours_surveillance"],s3["jours_surveillance"],s4["jours_surveillance"]],[2,1,0])
        self.assertEqual(s2["jours_surveillance_sans_feu_observe"],1)
        self.assertEqual(s4["jours_feu_non_couverts"],1)

    def test_deux_echeances_ont_meme_denominateur(self):
        a=indicateurs(self.jours,2025,"31","J+1",3)
        b=indicateurs(self.jours,2025,"31","J+2",3)
        self.assertEqual(a["jours_eligibles"],b["jours_eligibles"])
        self.assertEqual(a["jours_avec_feu_observe"],b["jours_avec_feu_observe"])
        self.assertEqual(a["jours_surveillance"],1)
        self.assertEqual(b["jours_surveillance"],1)
        self.assertEqual(b["jours_feu_couverts"],0)

    def test_aucun_feu_ne_produit_pas_100_pct(self):
        arr=[dict(r,nb_feux_observes_type_f=0,jour_avec_feu_observe=0) for r in self.jours]
        r=indicateurs(arr,2025,"31","J+1",2)
        self.assertIsNone(r["couverture_feu_pct"])
        self.assertEqual(r["jours_surveillance_sans_feu_observe"],2)

if __name__=="__main__":
    unittest.main()
