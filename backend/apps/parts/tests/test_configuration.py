import pytest

from apps.parts.configuration import FIELD_LABELS, PART_TYPES, REMARK_FIELD, TYPE_FIELD
from apps.parts.models import Part

MODEL_FIELDS = {field.name for field in Part._meta.get_fields()}


def test_labelled_fields_exist_on_the_model():
    assert set(FIELD_LABELS) <= MODEL_FIELDS
    assert {TYPE_FIELD, REMARK_FIELD} <= MODEL_FIELDS


@pytest.mark.parametrize('part_type', PART_TYPES.values(), ids=PART_TYPES.keys())
def test_configured_fields_have_labels(part_type):
    configured = (
        set(part_type.list_fields)
        | set(part_type.search_fields)
        | set(part_type.filter_fields)
        | set(part_type.editable_fields)
        | {field for field, _ in part_type.label_overrides}
    )

    assert configured <= set(FIELD_LABELS)


def test_type_specific_label_overrides_the_shared_one():
    assert PART_TYPES['R'].label_of('value') == '阻值'
    assert PART_TYPES['R'].label_of('package') == '封裝'
