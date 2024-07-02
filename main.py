import os
import sys
import pathlib
import solution


def find_string_in_dir(search_items, directory, file_extensions_for_search):
    files_contains_string = []

    for folder, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extensions_for_search):
                fullpath = os.path.join(folder, file)
                with open(fullpath, 'rb') as f:
                    content = f.read().decode('utf-8')
                    if any(si in content for si in search_items):
                        files_contains_string.append(fullpath)

    return files_contains_string


def find_namespace_usages(project_filename, namespaces):
    path = pathlib.Path(project_filename)
    project_dir = path.parent

    return find_string_in_dir(namespaces, project_dir, file_extensions_for_search=".cs")


if __name__ == '__main__':
    sln_path = pathlib.Path(sys.argv[1])

    sln = solution.parse(sln_path)

    for project in sln.projects:
        print("Project: " + project.name)

        for reference in project.references:
            files_using_namespaces = find_namespace_usages(project.filename, reference.get_namespaces())

            if len(files_using_namespaces) == 0:
                print("\tReferences: " + reference.name)
