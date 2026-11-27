import csv
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import collecter_cog_insee as cog


class CollecteCogTest(unittest.TestCase):
    def setUp(self):
        self.communes = ["COM", "DEP", "REG", "TYPECOM", "LIBELLE", "NCC"]
        self.departements = ["DEP", "REG", "LIBELLE", "NCC"]
        self.mouvements = ["DATE_EFF", "MOD", "TYPECOM_AV", "COM_AV", "LIBELLE_AV",
                           "TYPECOM_AP", "COM_AP", "LIBELLE_AP"]
        self.c09 = dict(COM="09001", DEP="09", REG="76", TYPECOM="COM", LIBELLE="A", NCC="A")
        self.c31 = dict(self.c09, COM="31001", DEP="31", LIBELLE="B")
        self.nouveau = dict(self.c09, COM="09002", LIBELLE="C")
        self.externe = dict(self.c09, COM="01001", DEP="01", REG="84")
        self.nom = "v_commune_2024.csv"
        region = patch.object(cog, "DEPARTEMENTS", {"09", "31"})
        effectifs = patch.object(cog, "EXPECTED_NATIONAL", dict(zip(cog.SOURCES, (3, 3, 2))))
        region.start()
        effectifs.start()
        self.addCleanup(region.stop)
        self.addCleanup(effectifs.stop)

    def lire_communes(self, rows, fields=None):
        raw = cog.csv_output(fields or self.communes, rows)
        return cog.read_source(self.nom, raw, "COM", self.communes)

    def test_filtrage_region_et_type_preserve_les_codes_texte(self):
        rows, meta = self.lire_communes([
            self.c31, self.c09, self.externe, dict(self.c09, TYPECOM="COMD"),
        ])
        self.assertEqual([(row["COM"], row["DEP"]) for row in rows], [("09001", "09"), ("31001", "31")])
        self.assertEqual(meta["lignes_nationales"], 4)
        self.assertEqual(meta["lignes_occitanie"], 2)

    def test_rejet_doublon_commune(self):
        with self.assertRaisesRegex(ValueError, "unicité"):
            self.lire_communes([self.c09, self.c09, self.c31])

    def test_rejet_doublon_departement(self):
        raw = b"DEP,REG,LIBELLE,NCC\n09,76,A,A\n09,76,A,A\n"
        with self.assertRaisesRegex(ValueError, "unicité"):
            cog.read_source(cog.SOURCES[2], raw, "DEP", self.departements)

    def test_rejet_code_sans_zero_initial(self):
        with self.assertRaisesRegex(ValueError, "Code ou libellé"):
            self.lire_communes([dict(self.c09, COM="9001"), self.c31, self.externe])

    def test_rejet_couverture_regionale_incomplete(self):
        with self.assertRaisesRegex(ValueError, "Couverture régionale"):
            self.lire_communes([self.c09, self.externe, dict(self.externe, COM="01002")])

    def test_rejet_schema_invalide(self):
        for raw in (b"COM,DEP\n09001,09\n", b"COM,DEP,REG,TYPECOM,LIBELLE,NCC,COM\n",
                    b"COM,DEP,REG,TYPECOM,LIBELLE,NCC\n09001,09,76\n"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                cog.read_source(self.nom, raw, "COM", self.communes)

    def test_collecte_compare_les_millesimes_mouvements_et_empreintes(self):
        def movement(date, before="09001", after="09002", kind="COM"):
            return dict(zip(self.mouvements, (date, "32", kind, before, "A", kind, after, "C")))

        files = {
            cog.SOURCES[0]: cog.csv_output(self.communes, [self.c09, self.c31, self.externe]),
            cog.SOURCES[1]: cog.csv_output(self.communes, [
                self.nouveau, dict(self.c31, LIBELLE="B2"), self.externe]),
            cog.SOURCES[2]: b"DEP,REG,LIBELLE,NCC\n09,76,A,A\n31,76,B,B\n",
            "v_mvt_commune_2025.csv": cog.csv_output(self.mouvements, [
                movement("2024-01-01"), movement("2025-01-01"),
                movement("2025-01-01", kind="COMD"), movement("2025-01-02"),
                movement("2024-10-01", "01001", "01002"),
            ]),
        }
        with tempfile.TemporaryDirectory() as directory, patch.object(cog, "load_archives", return_value=(files, [])):
            output = Path(directory) / "sortie"
            cog.main(["--entrees", directory, "--sortie", str(output), "--date-collecte-utc", "2026-11-27T20:00:00Z"])
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["codes_communs"], 1)
            self.assertEqual(manifest["ecarts"], {"apparu": 1, "disparu": 1, "attribut_modifie": 1})
            for file, digest in manifest["sorties_sha256"].items():
                self.assertEqual(hashlib.sha256((output / file).read_bytes()).hexdigest(), digest)
            csv_text = (output / "mouvements_communes_2024_2025.csv").read_text()
            rows = list(csv.DictReader(io.StringIO(csv_text)))
            self.assertEqual([(row["DATE_EFF"], row["COM_AV"], row["COM_AP"]) for row in rows],
                             [("2025-01-01", "09001", "09002")])
            files["v_mvt_commune_2025.csv"] = b"DATE_EFF,MOD\n2025-01-01,32\n"
            with self.assertRaisesRegex(ValueError, "Colonnes attendues"):
                cog.collect(Path(directory), Path(directory) / "invalide", "2026-11-27T20:00:00Z")
            self.assertFalse((Path(directory) / "invalide").exists())

    def test_interface_workflow_sans_argument(self):
        with patch.object(cog, "collect") as run:
            cog.main([])
        run.assert_called_once_with(None, Path("datasets/public/insee_cog_2025"), None)

    def test_interface_workflow_echec_diagnostic_et_code_non_nul(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "docs/resultats/diagnostic_insee_v0.md"
            with patch.object(cog, "FAILURE_REPORT", report), patch.object(cog, "collect", side_effect=OSError("HTTP 504")):
                with self.assertRaises(SystemExit) as error:
                    cog.main([])
            self.assertEqual(error.exception.code, 1)
            self.assertIn("HTTP 504", report.read_text())


if __name__ == "__main__":
    unittest.main()
