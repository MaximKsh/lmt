from core.utils import get_number_from_name, get_sql_from_directory, get_hash


class HistoryMigration:

    def __init__(self,
                 number,
                 directory_name,
                 script_hash,
                 executed_timestamp):
        self.number = number
        self.directory_name = directory_name
        self.script_hash = script_hash
        self.executed_timestamp = executed_timestamp


class DirectoryMigration:

    def __init__(self,
                 number,
                 directory_name,
                 sql,
                 script_hash):
        self.number = number
        self.directory_name = directory_name
        self.sql = sql
        self.script_hash = script_hash
        
    @staticmethod
    def from_directory(directory_name):
        number = get_number_from_name(directory_name)
        sql = get_sql_from_directory(directory_name)
        sql_hash = get_hash(sql)
        return DirectoryMigration(number, directory_name, sql, sql_hash)

