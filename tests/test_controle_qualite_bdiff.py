import csv
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.controler_qualite_bdiff import controler, TOTAL


class TestBDIFF(unittest.TestCase):
    def run_case(self, rows, manifest=True, bad_hash=False, annex=True, cli=False):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'bdiff_2024.zip'
            s = io.StringIO()
            w = csv.writer(s, delimiter=';')
            w.writerow([f'Nombre : {len(rows)}'])
            w.writerow(['Critères de sélection =>','Date de première alerte, de : 2024-01-01 00:00:00',"Date de première alerte, jusqu'à : 2024-12-31 23:59:00",'Région administrative : OCCITANIE','Type de feu : F'])
            w.writerow(['Année','Numéro','Département','Code INSEE','Date de première alerte',TOTAL,'Surface forêt (m2)'])
            w.writerows(rows)
            with zipfile.ZipFile(p,'w') as z:
                z.writestr('Incendies.csv',s.getvalue())
                z.writestr('Définitions.pdf',b'%PDF-1.4')
                if annex: z.writestr('Mention légales.pdf',b'%PDF-1.4')
            entry = None if not manifest else {'sha256': 'bad' if bad_hash else hashlib.sha256(p.read_bytes()).hexdigest()}
            if cli:
                cmd = [sys.executable, 'scripts/controler_qualite_bdiff.py', str(p), '--commit-source', 'synthetique']
                if manifest:
                    m = Path(tmp)/'manifest.json'
                    m.write_text(json.dumps({'extractions':[dict(entry, fichier=p.name)]}))
                    cmd += ['--manifest', str(m)]
                result = subprocess.run(cmd, capture_output=True, text=True)
                return result.returncode, json.loads(result.stdout)['resultats'][0]['statut']
            return controler(p,entry,2024)

    def row(self): return ['2024','1','09','09001','2024-01-01 12:00:00','10','']
    def test_conforme(self):
        r=self.run_case([self.row()]); self.assertEqual(r['statut'],'CONFORME_SUR_REGLES_BLOQUANTES'); self.assertEqual(r['surfaces']['Surface forêt (m2)']['vides'],1)
    def test_integrite(self):
        self.assertEqual(self.run_case([self.row()],False)['statut'],'NON_CONTROLE')
        self.assertEqual(self.run_case([self.row()],bad_hash=True)['statut'],'ECHEC')
    def test_doublon(self): self.assertEqual(self.run_case([self.row(),self.row()])['erreurs']['BDF-01_doublons'],1)
    def test_vide(self): self.assertEqual(self.run_case([])['statut'],'ECHEC')
    def test_annexe(self): self.assertEqual(self.run_case([self.row()],annex=False)['statut'],'ECHEC')
    def test_valeurs_invalides(self):
        for i,v in [(0,'2025'),(1,''),(2,'75'),(3,'31001'),(4,'2024-02-30 12:00:00'),(4,'2025-01-01 12:00:00'),(5,''),(5,'-1'),(5,'NaN'),(5,'abc')]:
            with self.subTest(i=i,v=v):
                row=self.row(); row[i]=v; self.assertEqual(self.run_case([row])['statut'],'ECHEC')
    def test_cli(self):
        for manifest, bad, expected in [(True,False,(0,'CONFORME_SUR_REGLES_BLOQUANTES')),(True,True,(1,'ECHEC')),(False,False,(2,'NON_CONTROLE'))]:
            with self.subTest(manifest=manifest,bad=bad):
                self.assertEqual(self.run_case([self.row()],manifest,bad,cli=True),expected)
