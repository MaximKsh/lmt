import sqlite3
from datetime import datetime

from core.adapter_base import AdapterBase
from core.models import HistoryMigration


class Adapter(AdapterBase):

    def __init__(self):
        self.conn = None
        self.cur = None

    def open(self, connection_string):
        self.conn = sqlite3.connect(connection_string)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()

    def begin_transaction(self):
        pass

    def commit_transaction(self):
        self.conn.commit()

    def rollback_transaction(self):
        self.conn.rollback()

    def get_migration_history(self):
        try:
            rows = self.cur.execute("""
                SELECT 
                  number,
                  directory,
                  script_hash,
                  executed_time
                FROM migrations
                ORDER BY number;
            """)
            migrations = []
            for row in rows:
                migrations.append(HistoryMigration(
                    row[0],
                    row[1],
                    row[2],
                    row[3]
                ))
            return migrations
        except:
            self.cur.execute('''CREATE TABLE migrations 
                (number integer, directory text, script_hash text, executed_time text)''')
            return []

    def insert_migration(self, directory_migration):
        t = (directory_migration.number,
             directory_migration.directory_name,
             directory_migration.script_hash,
             datetime.utcnow())
        self.cur.execute('INSERT INTO migrations(number, directory, script_hash, executed_time) VALUES (?, ?, ?, ?)', t)

    def delete_migration(self, directory_migration):
        t = (directory_migration.number, )
        self.cur.execute('DELETE FROM migrations WHERE number = ?', t)

    def execute_non_query(self, sql):
        for statement in sql.split(';'):
            self.cur.execute(statement)
