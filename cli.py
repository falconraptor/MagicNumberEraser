# if __name__ == '__main__':
# 	source = input('code file: ')
# 	regex = input('regex file: ')
# 	with open(source, 'rt') as file:
# 		source_code = file.read()
# 	with open(regex, 'rt') as _in, open(f'fixed_{source}', 'wt') as _out:
# 		for match, replacement in _in.readline().split(',', 1):
# 			_out.write(re.sub(match, replacement, source_code))
import argparse
import re
from importlib import import_module
from os import walk
from shutil import move
from typing import List

from mappings.base import Mapping


def run(mapping_file: str, regex_file: str, replacement_dir: str):
    if not mapping_file:
        mapping_file = input('mapping file: ')
    if not regex_file:
        regex_file = input('regex file: ')
    if not replacement_dir:
        replacement_dir = input('replacement dir: ')
    mapping = read_mapping(mapping_file)
    regex = read_regex(regex_file)
    replace_dir(mapping, regex, replacement_dir)


def read_mapping(mapping_file: str) -> Mapping:
    ext = mapping_file.split('.')[-1]
    try:
        mod = getattr(import_module(f'mappings.{ext}'), ext.upper())()
    except ModuleNotFoundError:
        mod = Mapping()
    return mod.get_mapping(mapping_file)


def read_regex(regex_file: str) -> List[List[str]]:
    with open(regex_file, 'rt') as file:
        regex = [line.split(',', 1) for line in file]
    return regex


def replace_dir(mapping: Mapping, regex: List[List[str]], replacement_dir: str):
    for path, dirs, files in walk(replacement_dir):
        for file in files:
            with open(f'{path}/{file}', 'rt') as _in, open('tmp', 'wt') as _out:
                for line in _in:
                    for (match, replace) in regex:
                        _out.write(re.sub(match, f'{mapping.class_}.{replace}', line))
            move('tmp', f'{path}/{file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mapping_file', default='')
    parser.add_argument('regex_file', default='')
    parser.add_argument('replacement_dir', default='')
    run(**parser.parse_args().__dict__)
