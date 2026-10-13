"""Part Configuration: which columns of the shared parts table each part type uses.

The parts table has far more columns than any one part type needs. Everything
the API exposes about a type (list columns, search, filters, editable fields)
comes from here, and the frontend builds its tables and forms from it.

Column names are assumptions until the real schema is available; see
docs/domains/parts-schema-assumptions.md.
"""

from dataclasses import dataclass

TYPE_FIELD = 'table_name'
REMARK_FIELD = 'remark'

# Display name of every column the platform shows, shared by all part types.
FIELD_LABELS = {
    'id': 'ID',
    'part_number': '料號',
    'table_name': '類型',
    'description': '描述',
    'value': '值',
    'tolerance': '誤差',
    'power_rating': '功率',
    'voltage_rating': '耐壓',
    'current_rating': '額定電流',
    'package': '封裝',
    'manufacturer': '製造商',
    'manufacturer_part_number': '製造商料號',
    'schematic_part': 'Symbol',
    'pcb_footprint': 'Footprint',
    'remark': '備註',
}


@dataclass(frozen=True)
class PartType:
    code: str
    label: str
    # Columns of the list table, in display order. Sorting is allowed on these.
    list_fields: tuple[str, ...]
    # Columns the keyword search looks in.
    search_fields: tuple[str, ...]
    # Columns offered as exact-match filters.
    filter_fields: tuple[str, ...]
    # Columns that may be changed through the platform (used from M3).
    editable_fields: tuple[str, ...] = ()
    # Labels that differ from FIELD_LABELS for this type.
    label_overrides: tuple[tuple[str, str], ...] = ()

    def label_of(self, field):
        return dict(self.label_overrides).get(field, FIELD_LABELS[field])


PART_TYPES = {
    part_type.code: part_type
    for part_type in (
        PartType(
            code='R',
            label='電阻',
            list_fields=(
                'part_number',
                'value',
                'tolerance',
                'power_rating',
                'package',
                'manufacturer',
                'description',
            ),
            search_fields=('part_number', 'value', 'description'),
            filter_fields=('tolerance', 'power_rating', 'package', 'manufacturer'),
            editable_fields=('description', 'remark'),
            label_overrides=(('value', '阻值'),),
        ),
        PartType(
            code='C',
            label='電容',
            list_fields=(
                'part_number',
                'value',
                'tolerance',
                'voltage_rating',
                'package',
                'manufacturer',
                'description',
            ),
            search_fields=('part_number', 'value', 'description'),
            filter_fields=('tolerance', 'voltage_rating', 'package', 'manufacturer'),
            editable_fields=('description', 'remark'),
            label_overrides=(('value', '容值'),),
        ),
        PartType(
            code='L',
            label='電感',
            list_fields=(
                'part_number',
                'value',
                'tolerance',
                'current_rating',
                'package',
                'manufacturer',
                'description',
            ),
            search_fields=('part_number', 'value', 'description'),
            filter_fields=('current_rating', 'package', 'manufacturer'),
            editable_fields=('description', 'remark'),
            label_overrides=(('value', '感值'),),
        ),
        PartType(
            code='IC',
            label='IC',
            list_fields=(
                'part_number',
                'manufacturer_part_number',
                'manufacturer',
                'package',
                'description',
            ),
            search_fields=('part_number', 'manufacturer_part_number', 'description'),
            filter_fields=('package', 'manufacturer'),
            editable_fields=('description', 'remark'),
        ),
    )
}
