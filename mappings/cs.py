import re

from mappings.base import Mapping


class CS(Mapping):
    def get_mapping(self, mapping_file):  # TODO add comment ignoring
        struct = re.compile(r'class|struct')
        types = re.compile(r'public\s+const\s+\w+\s+(\w+)\s*=\s*(.*)\s*;')
        with open(mapping_file, 'rt') as file:
            for line in file:
                if self.class_:
                    if 'const' in line:
                        match = types.match(line)
                        self.constants[match[1]] = match[2]
                        self.mapping[match[2]] = match[1]
                elif 'namespace' in line:
                    self.namespace = line.split()[-1].replace('{', '')
                elif struct.search(line):
                    self.class_ = line.split()[-1].replace('{', '')
        return self
