import psycopg2

from core.adapter_base import AdapterBase
from core.models import HistoryMigration


class Adapter(AdapterBase):

    def __init__(self):
        self.conn = None
        self.cur = None

    def open(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def begin_transaction(self):
        pass

    def commit_transaction(self):
        self.conn.commit()

    def rollback_transaction(self):
        self.conn.rollback()

    def get_migration_history(self):
        try:
            self.cur.execute("""
                SELECT 
                  number,
                  directory,
                  script_hash,
                  executed_time
                FROM migrations
                ORDER BY number;
            """)
            migrations = []
            for row in self.cur:
                migrations.append(HistoryMigration(
                    row[0],
                    row[1],
                    row[2],
                    row[3]
                ))
            return migrations
        except psycopg2.ProgrammingError as e:
            self.conn.reset()
            if e.pgcode == '42P01' and e.pgerror.startswith('ERROR:  relation "migrations" does not exist'):
                self.cur.execute("""
                        CREATE TABLE migrations(
                            number INTEGER PRIMARY KEY,
                            directory TEXT NOT NULL,
                            script_hash TEXT NOT NULL,
                            executed_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT(now() AT TIME ZONE 'UTC')
                        );   
                        CREATE UNIQUE INDEX migrations_directory_uindex ON public.migrations (directory);    
                    """)
                return []
            raise

    def insert_migration(self, directory_migration):
        self.cur.execute("""
            INSERT INTO migrations(number, directory, script_hash)
            VALUES (%s, %s, %s) ;   
        """, (directory_migration.number, directory_migration.directory_name, directory_migration.script_hash))

    def delete_migration(self, directory_migration):
        self.cur.execute("""
            DELETE FROM migrations
            WHERE number = %s   
        """, directory_migration.number)

    def execute_non_query(self, sql):
        self.cur.execute(sql)
