from django.contrib.auth.models import User

from apps.parts.models import Part
from config.db_routers import PartsRouter

router = PartsRouter()


def test_part_reads_and_writes_go_to_parts_db():
    assert router.db_for_read(Part) == 'parts'
    assert router.db_for_write(Part) == 'parts'


def test_platform_models_use_default_db():
    assert router.db_for_read(User) is None
    assert router.db_for_write(User) is None


def test_nothing_migrates_into_parts_db():
    assert router.allow_migrate('parts', 'auth') is False
    assert router.allow_migrate('parts', 'parts', model_name='part') is False


def test_platform_db_migrations_are_not_blocked():
    assert router.allow_migrate('default', 'auth') is None
