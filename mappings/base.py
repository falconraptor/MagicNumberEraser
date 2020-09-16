import re


class Mapping:
    SPACES = re.compile(r'\s')

    def __init__(self):
        self.namespace = ''
        self.class_ = ''
        self.constants = {}
        self.mapping = {}

    def get_mapping(self, mapping_file):
        with open(mapping_file, 'rt') as file:
            self.constants = dict(self.SPACES.sub('', file.readline()).replace(';', '').split('=', 1))
        self.mapping = {value: key for key, value in self.constants.items()}
        return self
