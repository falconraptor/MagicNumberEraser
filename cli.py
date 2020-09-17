import argparse
import re
from importlib import import_module
from os import walk
from shutil import move
from typing import List

from .mappings.base import Mapping


def run(mapping_file: str, regex_file: str, replacement_dir: str, ignore_paths: Iterable[str] = None):
    if not mapping_file:
        mapping_file = input('mapping file: ')
    if not regex_file:
        regex_file = input('regex file: ')
    if not replacement_dir:
        replacement_dir = input('replacement dir: ')
    if not ignore_paths:
        ignore_paths = []
    mapping = read_mapping(mapping_file)
    regex = read_regex(regex_file)
    replace_dir(mapping, regex, replacement_dir, ignore_paths)


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


def replace_dir(mapping: Mapping, regex: List[List[str]], replacement_dir: str, ignore_paths: Iterable[str] = None):
    for path, dirs, files in walk(replacement_dir):
        if path in ignore_paths:
            continue
        for file in files:
            if file.split('.')[-1] not in mapping.ext:
                continue
            file_path = f'{path}/{file}'
            try:
                with open(file_path, 'rt') as _in, open('tmp', 'wt') as _out:
                    for line_number, line in enumerate(_in):
                        for (match, replace) in regex:
                            groups = re.search(match, line)
                            if groups:
                                line = re.sub(match, f'{replace}{mapping.mapping[groups[2]]}', line)
                            _out.write(line)
                move('tmp', file_path)
                print(f'Patched "{file_path}"')
            except UnicodeDecodeError:
                print(f'Unicode Decode Error "{file_path}"')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mapping_file', default='')
    parser.add_argument('regex_file', default='')
    parser.add_argument('replacement_dir', default='')
    parser.add_argument('-i', '--ignore_path', dest='ignore_paths', action='append')
    run(**parser.parse_args().__dict__)
