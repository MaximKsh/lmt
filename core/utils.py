import hashlib
import os
import re
from os import listdir
from os.path import join, isfile


def get_number_from_name(directory_name):
    values = list(map(int, re.findall('\d+', directory_name)))
    if len(values) == 0:
        return -1
    else:
        return values[0]


def get_sql_from_directory(directory):
    files = list([f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.sql')])
    files.sort(key=get_number_from_name)
    file_contents = []
    for filename in files:
        with open(join(directory, filename), 'r') as file:
            file_contents.append('-- ' + filename + '\n' + file.read() + '\n\n')
    return ''.join(file_contents)


def get_tagged_sql(sql, tag_prefix):
    reading = False
    sql_lines = []
    start_regex = re.compile(f'--\s*{tag_prefix}\s+begin\s*')
    end_regex = re.compile(f'--\s*{tag_prefix}\s+end\s*')
    for line in sql.splitlines():
        if start_regex.match(line):
            reading = True
        elif end_regex.match(line):
            reading = False
        elif reading:
            sql_lines.append(line)
            sql_lines.append(os.linesep)
    return ''.join(sql_lines)


def get_hash(script):
    return hashlib.md5(script.encode()).hexdigest()

