"""Tests d'intégration de la CLI MDF sur archives synthétiques."""
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.controler_qualite_mdf import OCCITANIE


class TestCodesSortieMdf(unittest.TestCase):
    def test_codes_sortie(self):
        with tempfile.TemporaryDirectory() as dossier:
            archive = Path(dossier) / "mdf.csv.gz"
            texte = "date,num_dep,niveau_j1,niveau_j2,nom_dep\n" + "".join(
                f"2026-06-01,{dep},1,2,x\n" for dep in sorted(OCCITANIE)
            )
            archive.write_bytes(gzip.compress(texte.encode()))
            manifeste = Path(dossier) / "manifest.json"
            sha = hashlib.sha256(archive.read_bytes()).hexdigest()
            for empreinte, code, statut in (
                (sha, 0, "CONFORME_SUR_REGLES_BLOQUANTES"),
                ("0" * 64, 1, "ECHEC"),
                (None, 2, "NON_CONTROLE"),
            ):
                with self.subTest(code=code):
                    args = [sys.executable, "scripts/controler_qualite_mdf.py", str(archive)]
                    if empreinte is not None:
                        manifeste.write_text(json.dumps({"extractions": [{"fichier": archive.name, "sha256": empreinte}]}))
                        args += ["--manifest", str(manifeste)]
                    resultat = subprocess.run(args, capture_output=True, text=True)
                    self.assertEqual(resultat.returncode, code, resultat.stderr)
                    self.assertEqual(json.loads(resultat.stdout)["resultats"][0]["statut"], statut)
