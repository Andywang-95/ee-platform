import pytest
from django.urls import reverse

from apps.parts.models import Part
from config.views import HealthView

pytestmark = pytest.mark.django_db(databases=['default', 'parts'])


def test_health_reports_ok_and_part_count(client):
    Part.objects.create(id=1, part_number='RES-0402-10K', table_name='R')

    response = client.get(reverse('health'))

    assert response.status_code == 200
    assert response.json() == {
        'status': 'ok',
        'platform_db': True,
        'parts_db': True,
        'part_count': 1,
    }


def test_health_reports_error_when_parts_db_is_unreachable(client, monkeypatch):
    monkeypatch.setattr(HealthView, '_count_parts', staticmethod(lambda: None))

    response = client.get(reverse('health'))

    assert response.status_code == 503
    assert response.json()['status'] == 'error'
    assert response.json()['parts_db'] is False


def test_openapi_schema_is_served(client):
    assert client.get(reverse('schema')).status_code == 200
