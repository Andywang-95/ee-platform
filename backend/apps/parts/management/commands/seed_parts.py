import random

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.parts.models import Part

RESISTOR_VALUES = ['0R', '10R', '100R', '1K', '4.7K', '10K', '47K', '100K', '1M']
CAPACITOR_VALUES = ['10pF', '100pF', '1nF', '10nF', '100nF', '1uF', '10uF', '100uF']
INDUCTOR_VALUES = ['1uH', '2.2uH', '4.7uH', '10uH', '22uH', '100uH']
PASSIVE_PACKAGES = ['0201', '0402', '0603', '0805', '1206']
ICS = [
    ('STM32F103C8T6', 'MCU ARM Cortex-M3 64KB Flash', 'LQFP48', 'STMicroelectronics'),
    ('TPS54331DR', 'Buck converter 3A 28V', 'SOIC8', 'Texas Instruments'),
    ('LM358DR', 'Dual operational amplifier', 'SOIC8', 'Texas Instruments'),
    ('MAX3232ESE', 'RS-232 transceiver', 'SOIC16', 'Analog Devices'),
    ('W25Q64JVSSIQ', 'SPI NOR flash 64Mbit', 'SOIC8', 'Winbond'),
    ('TLV1117-33', 'LDO regulator 3.3V 800mA', 'SOT223', 'Texas Instruments'),
]
REMARKS = [
    'Preferred part for new designs.',
    'Not recommended for new designs; use the 1% version instead.',
    'Long lead time, check stock before use.',
    'Second source approved.',
]


def passive(part_type, prefix, values, describe, symbol, **ratings):
    for value in values:
        for package in PASSIVE_PACKAGES:
            yield {
                'table_name': part_type,
                'part_number': f'{prefix}-{package}-{value}',
                'description': describe(value, package),
                'value': value,
                'package': package,
                'manufacturer': random.choice(['Yageo', 'Murata', 'TDK', 'Samsung']),
                'schematic_part': symbol,
                'pcb_footprint': f'{part_type}{package}',
                **{name: random.choice(choices) for name, choices in ratings.items()},
            }


def integrated_circuits():
    for number, description, package, manufacturer in ICS:
        yield {
            'table_name': 'IC',
            'part_number': f'IC-{number}',
            'description': description,
            'package': package,
            'manufacturer': manufacturer,
            'manufacturer_part_number': number,
            'schematic_part': f'IC\\{number}',
            'pcb_footprint': package,
        }


def fake_parts():
    yield from passive(
        'R',
        'RES',
        RESISTOR_VALUES,
        lambda value, package: f'RES {value} {package}',
        'DISCRETE\\R',
        tolerance=['1%', '5%'],
        power_rating=['1/16W', '1/10W', '1/8W'],
    )
    yield from passive(
        'C',
        'CAP',
        CAPACITOR_VALUES,
        lambda value, package: f'CAP {value} {package}',
        'DISCRETE\\C',
        tolerance=['5%', '10%', '20%'],
        voltage_rating=['6.3V', '16V', '25V', '50V'],
    )
    yield from passive(
        'L',
        'IND',
        INDUCTOR_VALUES,
        lambda value, package: f'IND {value} {package}',
        'DISCRETE\\L',
        tolerance=['20%'],
        current_rating=['0.5A', '1A', '2A'],
    )
    yield from integrated_circuits()


class Command(BaseCommand):
    help = 'Fill the development parts database with fake parts.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--if-empty',
            action='store_true',
            help='Do nothing when the parts table already has rows.',
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('seed_parts only runs with DEBUG on; it rewrites the parts table.')

        if options['if_empty'] and Part.objects.exists():
            self.stdout.write('Parts table already has data, skipping.')
            return

        # A fixed seed keeps the fake data identical between runs.
        random.seed(0)
        parts = []
        for index, fields in enumerate(fake_parts(), start=1):
            # Roughly one part in three has a remark, so both cases show up in the UI.
            remark = random.choice(REMARKS) if index % 3 == 0 else None
            parts.append(Part(id=index, remark=remark, **fields))

        Part.objects.all().delete()
        Part.objects.bulk_create(parts)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(parts)} parts.'))
