import importlib
from os import listdir
from os.path import isdir, join

from core.configuration import read_configuration, FORWARD, BACKWARD
from core.logging import get_suitable_logger
from core.models import DirectoryMigration
from core.utils import get_tagged_sql
from core.validation import validate


def prepare_data(config, adapter):
    path = config.migration_path
    directories = [f for f in listdir(path) if isdir(join(path, f)) and f.startswith('migration_')]
    directory_migrations = [DirectoryMigration.from_directory(config.migration_path, d) for d in directories]
    directory_migrations.sort(key=lambda x: x.number)
    history_migrations = adapter.get_migration_history()

    return directory_migrations, history_migrations


def get_target_migrations_directories(config, history_migrations, directory_migrations):
    def filter_directories(predicate):
        return list(filter(predicate, directory_migrations))

    migrations_size = len(history_migrations)

    if config.direction == FORWARD:
        max_directory = max(directory_migrations, key=lambda x: x.number)
        if config.target != -1:
            target = config.target
        else:
            target = max_directory.number
        if migrations_size != 0:
            max_migration = max(history_migrations, key=lambda x: x.number)
            target_directories = filter_directories(lambda x: max_migration.number < x.number <= target)
        else:
            target_directories = filter_directories(lambda x: x.number <= target)
    elif config.direction == BACKWARD:
        max_migration = max(history_migrations, key=lambda x: x.number)
        target = config.target
        target_directories = filter_directories(lambda x: target <= x.number <= max_migration.number)
    else:
        raise Exception(f'Unknown direction {config.direction}.')

    target_directories.sort(key=lambda x: x.number, reverse=config.direction == BACKWARD)
    return target_directories


def get_migration_history_action(config, adapter):
    def insert(descriptor):
        adapter.insert_migration(descriptor)

    def delete(descriptor):
        adapter.delete_migration(descriptor)

    if config.direction == FORWARD:
        return insert
    elif config.direction == BACKWARD:
        return delete
    return None


def migrate(config, adapter):
    adapter.open(config.connection_string)
    logger = get_suitable_logger(config)
    try:
        adapter.begin_transaction()
        directory_migrations, history_migrations = prepare_data(config, adapter)

        if not validate(config, history_migrations, directory_migrations, logger):
            return

        target_directories = get_target_migrations_directories(config, history_migrations, directory_migrations)
        migration_history_action = get_migration_history_action(config, adapter)
        for target_directory in target_directories:
            sql = get_tagged_sql(target_directory.sql, config.direction)
            adapter.execute_non_query(sql)
            migration_history_action(target_directory)

        adapter.commit_transaction()
    except:
        adapter.rollback_transaction()
        raise
    finally:
        adapter.close()


def main():
    conf = read_configuration()
    adapter_module = importlib.import_module('adapters.' + conf.adapter)
    adapter = adapter_module.Adapter()
    migrate(conf, adapter)
