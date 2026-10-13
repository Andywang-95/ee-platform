import pytest
from django.db import connections

from apps.parts.models import Part
from config.db_routers import PARTS_DB


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Create the unmanaged parts table, which migrations never do."""
    with django_db_blocker.unblock(), connections[PARTS_DB].schema_editor() as editor:
        editor.create_model(Part)
