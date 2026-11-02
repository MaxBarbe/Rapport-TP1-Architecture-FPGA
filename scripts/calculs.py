#!/usr/bin/env python3
"""Reproduire les calculs du rapport, sans modifier les mesures d'origine."""
import argparse
import csv
import io
import json
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'donnees'


def read(name):
    with (DATA / name).open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def csv_text(headers, rows):
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(headers)
    writer.writerows(rows)
    return stream.getvalue()


def formatted(value):
    return str(value.quantize(D('0.000001')))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verifier les sorties sans les reecrire')
    args = parser.parse_args()

    results = []
    for name, label in [('addition_entiere.csv', 'addition_entiere'),
                        ('addition_flottante.csv', 'addition_flottante')]:
        for row in read(name):
            frequency = D(row['frequence_MHz'])
            total = D(row['puissance_totale_mW'])
            dynamic = D(row['puissance_dynamique_coeur_mW'])
            results.append([label, row['pipeline'], frequency,
                            formatted(total / frequency),
                            formatted(dynamic / frequency * 1000)])

    rounding_differences = []
    for name in ['addition_entiere.csv', 'multiplication.csv', 'filtre_quartus.csv']:
        for row in read(name):
            parts = sum(D(row[key]) for key in ['puissance_dynamique_coeur_mW',
                        'puissance_statique_coeur_mW', 'puissance_ES_mW'])
            difference = D(row['puissance_totale_mW']) - parts
            if abs(difference) > D('0.02'):
                raise ValueError(f'Incoherence des composantes de puissance : {name}')
            if difference:
                rounding_differences.append({'fichier': name, 'pipeline': row.get('pipeline'),
                                             'total_moins_somme_mW': str(difference)})

    readings = read('mesures_brutes.csv')
    powers = []
    for row in readings:
        power = D(row['tension_V']) * D(row['courant_A'])
        if power != D(row['puissance_W']):
            raise ValueError(f'Produit U*I incorrect : {row["photo"]}')
        powers.append(power)

    fps = D(25_000_000) / (800 * 525)
    current = D('0.6')
    voltage = D('5')
    nominal_power = voltage * current
    energy_mj = nominal_power / fps * 1000
    pixels = D(420 * 280)
    isolated_time = pixels / D(100_000_000)
    isolated_energy_mj = D('0.42886') * isolated_time * 1000

    summary = {
        'ecarts_des_valeurs_arrondies': rounding_differences,
        'courant_reference_A': str(current),
        'tension_nominale_V': str(voltage),
        'puissance_nominale_W': str(nominal_power),
        'debit_nominal_images_s': formatted(fps),
        'duree_trame_ms': formatted(1000 / fps),
        'energie_nominale_mJ_image': formatted(energy_mj),
        'conclusion_arrondie_mJ_image': 'environ 50',
        'puissance_instantanee_min_W': str(min(powers)),
        'puissance_instantanee_max_W': str(max(powers)),
        'moyenne_arithmetique_quatre_instantanes_W': str(sum(powers) / len(powers)),
        'duree_filtre_isole_100MHz_ms_conditionnelle': formatted(isolated_time * 1000),
        'energie_filtre_isole_mJ_conditionnelle': formatted(isolated_energy_mj),
        'condition_filtre': 'un pixel par cycle a 100 MHz valides et puissance conforme a cette activite',
        'statut_parallele_et_sans_DSP': 'aucune puissance mesuree disponible',
    }
    outputs = {
        'energies_operateurs.csv': csv_text(
            ['operateur', 'pipeline', 'frequence_MHz',
             'energie_totale_nJ_op_conditionnelle', 'energie_dynamique_pJ_op_conditionnelle'], results),
        'debits_filtre.csv': csv_text(
            ['debit_images_s', 'pixels_image', 'frequence_utile_minimale_MHz', 'duree_image_ms'],
            [[rate, int(pixels), formatted(pixels * rate / 1_000_000),
              formatted(D(1000) / rate)] for rate in [30, 60, 100]]),
        'synthese_calculs.json': json.dumps(summary, ensure_ascii=False, indent=2) + '\n',
    }
    for name, content in outputs.items():
        target = DATA / name
        if args.check:
            if not target.exists() or target.read_text(encoding='utf-8') != content:
                raise ValueError(f'Sortie absente ou differente : {target}')
        else:
            target.write_text(content, encoding='utf-8')
    print('Calculs verifies.' if args.check else 'Tableaux calcules generes.')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
