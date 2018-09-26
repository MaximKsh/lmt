from core.configuration import FORWARD, BACKWARD


def validate_config(config, history_migrations, directory_migrations, logger):
    min_migration_number = min(history_migrations, key=lambda x: x.number)
    max_migration_number = max(history_migrations, key=lambda x: x.number)
    max_directory_number = max(directory_migrations, key=lambda x: x.number)

    if config.direction == FORWARD \
            and config.target != -1 \
            and not max_migration_number < config.target <= max_directory_number:
        logger.err(f'target must be a migration number between ({max_migration_number}, {max_directory_number}].')
        return False

    if config.direction == BACKWARD:
        if len(history_migrations) != 0:
            logger.err(f'migrations history is empty.')
            return False
        if config.target == -1:
            logger.err(f'target must be specified for {BACKWARD} direction.')
            return False
        if min_migration_number <= config.target < max_migration_number:
            logger.err(f'target must be a migration number between [{min_migration_number}, {max_migration_number}).')
            return False
    return True


def validate(config, history_migrations, directory_migrations, logger):
    if not validate_config(config, history_migrations, directory_migrations, logger):
        return False

    if config.ignore_validation:
        logger.trace('hash validation ignored.')
        return True

    dir_index = 0
    for migration in history_migrations:
        logger.trace(f'Checking migration {migration.directory_name}')
        directory = directory_migrations[dir_index]
        if directory.directory_name != migration.directory_name:
            logger.err(f'Migration {migration.directory_name} is '
                       f'differ from migration on disk {directory.directory_name}')
            return False
        if directory.script_hash != migration.script_hash:
            logger.err(f'Хэш миграции не соответствует миграции на диске')
            return False
        dir_index += 1
    return True
