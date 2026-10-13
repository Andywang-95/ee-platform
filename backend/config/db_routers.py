PARTS_DB = 'parts'


def uses_parts_db(model):
    """Unmanaged models of the parts app map to tables in the parts database."""
    return model._meta.app_label == 'parts' and not model._meta.managed


class PartsRouter:
    def db_for_read(self, model, **hints):
        return PARTS_DB if uses_parts_db(model) else None

    def db_for_write(self, model, **hints):
        return PARTS_DB if uses_parts_db(model) else None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # The platform never changes the structure of the parts database.
        if db == PARTS_DB:
            return False
        return None
