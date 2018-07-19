class TestingDBSports_Router:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'testingdb_sports':
            return 'testingdb_sports'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'testingdb_sports':
            return 'testingdb_sports'
        return None

    def allow_syncdb(self, db, model):
        # Specify target database with field in_db in 1 - Persona Identification's Meta class
        if hasattr(model._meta, 'testingdb_sports'):
            if model._meta.in_db == db:
                return True
            else:
                return False
        else:
            # Random models that don't specify a database can only go to 'default'
            if db == 'default':
                return True
            else:
                return False