import re
import os
import pathlib
import project


__all__ = ['Solution', 'parse']


_REGEX_PROJECT_FILE = re.compile(r'^Project\(\"\{([^}]+)}\"\)[\s=]+\"([^\"]+)\",\s\"(.+csproj)\", \"(\{[^}]+})\"')


class Solution(object):

    def __init__(self, filename):

        sln_path = pathlib.Path(filename)
        sln_dir = sln_path.parent

        self.filename = filename
        self.projects = []

        with open(self.filename, 'rb') as f:
            while True:
                b_line = f.readline()

                if not b_line:
                    break

                line = b_line.decode('utf-8')

                match = _REGEX_PROJECT_FILE.match(line)
                if match:
                    proj_path = os.path.join(sln_dir, match.groups()[2])

                    self.projects.append(project.Project(proj_path))


def parse(filename):
    return Solution(filename)
