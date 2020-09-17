import re


class Mapping:
    SPACES = re.compile(r'\s')

    def __init__(self):
        self.namespace = ''
        self.class_ = ''
        self.constants = {}
        self.mapping = {}
        self.ext = set()

    def get_mapping(self, mapping_file):
        raise NotImplementedError

    def add_ext(self, *ext):
        self.ext.update(ext)
        return self
