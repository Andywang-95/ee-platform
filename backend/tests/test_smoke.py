from django.apps import apps
from django.urls import reverse


def test_parts_app_is_installed():
    assert apps.is_installed('apps.parts')


def test_admin_url_resolves():
    assert reverse('admin:index') == '/admin/'
