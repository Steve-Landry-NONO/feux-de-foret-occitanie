"""Qualification BDIFF en lecture seule, sans collecte ni jointure."""
import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

OCC = set('09 11 12 30 31 32 34 46 48 65 66 81 82'.split())
REQUIRED = {'Année', 'Numéro', 'Département', 'Code INSEE', 'Date de première alerte', 'Surface parcourue (m2)'}
TOTAL = 'Surface parcourue (m2)'
ANNEXES = {'Incendies.csv', 'Mention légales.pdf', 'Définitions.pdf'}


def controler(path, entry, year):
    path = Path(path)
    r = {'fichier': path.name, 'annee': year, 'erreurs': {}, 'provenance_tls': 'NON_VALIDEE', 'validation_collective': 'EN_ATTENTE'}
    errors = Counter()
    try:
        raw = path.read_bytes()
        r['sha256'] = hashlib.sha256(raw).hexdigest()
        r['integrite'] = 'NON_CONTROLEE' if entry is None else 'CONFORME' if entry.get('sha256') == r['sha256'] else 'ECHEC'
        if r['integrite'] == 'ECHEC': errors['BDF-05'] += 1
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            names = z.namelist()
            if set(names) != ANNEXES or len(names) != len(ANNEXES) or z.testzip():
                raise ValueError('Structure ZIP ou CRC invalide')
            r['annexes_sha256'] = {n: hashlib.sha256(z.read(n)).hexdigest() for n in sorted(ANNEXES - {'Incendies.csv'})}
            if any(not z.read(n).startswith(b'%PDF-') for n in r['annexes_sha256']): raise ValueError('Signature PDF invalide')
            reader = csv.reader(io.StringIO(z.read('Incendies.csv').decode('utf-8-sig')), delimiter=';', strict=True)
            count, filters, header = next(reader), next(reader), next(reader)
            if not REQUIRED <= set(header) or len(set(header)) != len(header): raise ValueError('Colonnes manquantes ou dupliquées')
            r['colonnes'] = header
            expected = {f'Date de première alerte, de : {year}-01-01 00:00:00', f"Date de première alerte, jusqu'à : {year}-12-31 23:59:00", 'Région administrative : OCCITANIE', 'Type de feu : F'}
            if not expected <= set(filters): errors['BDF-04_filtres'] += 1
            declared = re.search(r':\s*(\d+)\s*$', count[0]) if len(count) == 1 else None
            rows = list(reader)
            r['lignes'] = len(rows)
            if not declared or int(declared.group(1)) != len(rows): errors['BDF-06_effectif'] += 1
            if not rows: errors['BDF-06_vide'] += 1
            missing, deps, keys, dates = Counter(), Counter(), Counter(), []
            surfaces = [c for c in header if c.endswith('(m2)')]
            r['unite_surface'] = 'm2'
            r['surfaces'] = {c: {'vides': 0, 'zeros': 0, 'invalides': 0, 'negatives': 0, 'somme': Decimal(0)} for c in surfaces}
            coherence = Counter()
            for values in rows:
                if len(values) != len(header): errors['BDF-06_largeur'] += 1; continue
                row = dict(zip(header, (v.strip() for v in values)))
                missing.update(c for c,v in row.items() if not v)
                key = (row['Année'], row['Numéro'])
                if not key[1]: errors['BDF-01_identifiant_vide'] += 1
                else: keys[key] += 1
                if key[0] != str(year): errors['BDF-04_annee'] += 1
                dep, commune = row['Département'], row['Code INSEE']
                deps[dep] += 1
                if dep not in OCC or not re.fullmatch(r'[0-9]{5}', commune) or not commune.startswith(dep): errors['BDF-07_territoire'] += 1
                try:
                    d = datetime.strptime(row['Date de première alerte'], '%Y-%m-%d %H:%M:%S')
                    dates.append(d.date().isoformat())
                    if d.year != year: errors['BDF-04_date'] += 1
                except ValueError: errors['BDF-02_date'] += 1
                nums = {}
                for c in surfaces:
                    v, s = row[c], r['surfaces'][c]
                    if not v:
                        s['vides'] += 1
                        if c == TOTAL: errors['BDF-02_surface_totale'] += 1
                        continue
                    try:
                        n = Decimal(v.replace(',', '.'))
                        if not n.is_finite(): raise InvalidOperation
                    except InvalidOperation:
                        s['invalides'] += 1; errors['BDF-03_surface_invalide'] += 1; continue
                    if n < 0: s['negatives'] += 1; errors['BDF-03_surface_negative'] += 1; continue
                    s['zeros'] += int(n == 0); s['somme'] += n; nums[c] = n
                if TOTAL in nums:
                    for c,n in nums.items():
                        if c != TOTAL and n > nums[TOTAL]: coherence[c] += 1
            errors['BDF-01_doublons'] = sum(n-1 for n in keys.values())
            r.update(identifiants_uniques=len(keys), departements=dict(sorted(deps.items())), dates=[min(dates),max(dates)] if dates else [], valeurs_manquantes={c:missing[c] for c in header}, composantes_superieures_total=dict(coherence))
            for s in r['surfaces'].values(): s['somme'] = str(s['somme'])
    except (OSError, ValueError, UnicodeError, zipfile.BadZipFile, csv.Error, StopIteration, RuntimeError) as exc:
        errors['BDF-06_lecture'] += 1; r['detail_lecture'] = str(exc)
    r['erreurs'] = dict(errors)
    r['statut'] = 'ECHEC' if any(errors.values()) else 'NON_CONTROLE' if r.get('integrite') == 'NON_CONTROLEE' else 'CONFORME_SUR_REGLES_BLOQUANTES'
    return r


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('archives', nargs='+', type=Path)
    p.add_argument('--manifest', type=Path)
    p.add_argument('--commit-source', required=True)
    a = p.parse_args()
    entries = None if a.manifest is None else {e['fichier']:e for e in json.loads(a.manifest.read_text())['extractions']}
    results = [controler(f, None if entries is None else entries.get(f.name, {}), int(re.search(r'(\d{4})\.zip$', f.name).group(1))) for f in a.archives]
    print(json.dumps({'date_execution':datetime.now(timezone.utc).date().isoformat(),'commit_source':a.commit_source,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'resultats':results},ensure_ascii=False,indent=2))
    return 1 if any(r['statut']=='ECHEC' for r in results) else 2 if any(r['statut']=='NON_CONTROLE' for r in results) else 0


if __name__ == '__main__':
    raise SystemExit(main())
