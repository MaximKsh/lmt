

class AdapterBase:

    def open(self, connection_string):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def begin_transaction(self):
        raise NotImplementedError()

    def commit_transaction(self):
        raise NotImplementedError()

    def rollback_transaction(self):
        raise NotImplementedError()

    def get_migration_history(self):
        raise NotImplementedError()

    def insert_migration(self, directory_migration):
        raise NotImplementedError()

    def delete_migration(self, directory_migration):
        raise NotImplementedError()

    def execute_non_query(self, sql):
        raise NotImplementedError()
