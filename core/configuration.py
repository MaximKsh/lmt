import argparse
import json
from os import getcwd, path

FORWARD = 'forward'
BACKWARD = 'backward'


class Configuration:

    def __init__(self,
                 adapter,
                 connection_string,
                 target,
                 migration_path,
                 direction,
                 ignore_validation,
                 verbose):
        if adapter is None:
            raise Exception('adapter isn\'t specified')
        if connection_string is None:
            raise Exception('connection_string isn\'t specified')

        self.adapter = adapter
        self.connection_string = connection_string
        self.target = target if target is not None else -1
        self.migration_path = migration_path or getcwd()
        self.direction = direction or FORWARD
        self.ignore_validation = ignore_validation or False
        self.verbose = verbose or False


def parse_file(filename):
    with open(path.join(getcwd(), filename)) as f:
        conf_file = json.loads(f.read())
    return Configuration(
        conf_file.get("adapter"),
        conf_file.get("connection_string"),
        conf_file.get("target"),
        conf_file.get("migration_path"),
        conf_file.get("direction"),
        conf_file.get("ignore_validation"),
        conf_file.get("verbose")
    )


def parse_cli(args):
    return Configuration(
        args.adapter,
        args.connection_string,
        args.target,
        args.migration_path,
        args.direction,
        args.ignore_validation,
        args.verbose
    )


def read_configuration():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-f", "--file", help="configuration file")
    parser.add_argument("-a", "--adapter", help="adapter name")
    parser.add_argument("-c", "--connection_string", help="connection string to database")
    parser.add_argument("-p", "--migration_path", help="migrations location")
    parser.add_argument("-t", "--target", type=int, help="target number of migration")
    parser.add_argument("-d", "--direction", choices=['forward', 'backward'], help="direction of migration")
    parser.add_argument("-i", "--ignore_validation", action='store_true', help="ignore migrations hash validation")
    parser.add_argument("-v", "--verbose", action='store_true', help="increase output verbosity")
    args = parser.parse_args()
    if args.file is not None:
        return parse_file(args.file)
    else:
        return parse_cli(args)
