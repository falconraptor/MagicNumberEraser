import re

from .base import Mapping


class CS(Mapping):
    def get_mapping(self, mapping_file):  # TODO add comment ignoring
        self.ext.add(mapping_file.split('.')[-1])
        struct = re.compile(r'class|struct')
        types = re.compile(r'\s*public\s+const\s+\w+\s+(\w+)\s*=\s*(.*)\s*;\s*')
        with open(mapping_file, 'rt') as file:
            for line in file:
                if struct.search(line):
                    if self.class_:
                        self.class_ += '.'
                    self.class_ += line.split()[-1].replace('{', '')
                if self.class_:
                    if 'const' in line:
                        match = types.match(line)
                        if match:
                            self.constants[match[1]] = match[2]  # Name -> Value
                            self.mapping[match[2]] = match[1]  # Value -> Name
                elif 'namespace' in line:
                    self.namespace = line.split()[-1].replace('{', '')
        return self
