import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.parts.models import Part

pytestmark = pytest.mark.django_db(databases=['default', 'parts'])


def test_seed_parts_creates_every_type_with_and_without_remarks(settings):
    settings.DEBUG = True

    call_command('seed_parts')

    assert set(Part.objects.values_list('table_name', flat=True)) == {'R', 'C', 'L', 'IC'}
    assert Part.objects.filter(remark__isnull=True).exists()
    assert Part.objects.filter(remark__isnull=False).exists()


def test_seed_parts_if_empty_keeps_existing_rows(settings):
    settings.DEBUG = True
    Part.objects.create(id=1, part_number='KEEP-ME', table_name='R')

    call_command('seed_parts', '--if-empty')

    assert list(Part.objects.values_list('part_number', flat=True)) == ['KEEP-ME']


def test_seed_parts_refuses_to_run_without_debug(settings):
    settings.DEBUG = False

    with pytest.raises(CommandError):
        call_command('seed_parts')
