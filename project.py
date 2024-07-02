import re
import os
import pathlib


__all__ = ['Project', 'parse']


_REGEX_REFERENCE = re.compile(r'\s+<ProjectReference[\s=]+Include=\"(.*\\((.+).csproj))\"\s/>\s+')


class Project(object):

    def __init__(self, filename, build_references=True):

        project_path = pathlib.Path(filename)
        project_dir = project_path.parent

        self.filename = filename
        self.name = project_path.stem
        self.references = []

        if build_references:
            with open(self.filename, 'rb') as f:
                while True:
                    b_line = f.readline()

                    if not b_line:
                        break

                    line = b_line.decode('utf-8')

                    match = _REGEX_REFERENCE.match(line)
                    if match:
                        proj_path = os.path.join(project_dir, match.groups()[0])

                        self.references.append(Project(proj_path, build_references=False))

    # if the namespace in the 'using' statement is different from the assembly name
    # describe namespaces rules here
    def get_namespaces(self):
        namespaces = [self.name]

        if ".mvc" in self.name:
            namespaces.append(self.name.replace(".mvc", ""))

        return namespaces


def parse(filename):
    return Project(filename)
