import os
import re


RELATIVE_IMPORT = re.compile(r'(from|import) \.\.+([a-z]+)?')


def walk_directory(root, dirs, files):
    for file_path in files:
        if 'project_template' not in root and file_path.lower().endswith('.py'):
            clean_file(os.path.join(root, file_path))


def clean_file(file_path):
    py_source = file(file_path).read()
    if 'from ..' in py_source or 'import ..' in py_source:
        print '====' * 8
        print file_path
        print '====' * 8

        package = file_path.rstrip('.py').split('/')

        def replace_import(matchobj):
            prefix, suffix = matchobj.group(0).split()
            return '{} {}'.format(prefix, clean_import(package, suffix))

        py_source = RELATIVE_IMPORT.sub(replace_import, py_source)

        #print py_source
        with open(file_path, 'w') as package:
            print file_path
            package.write(py_source)


def clean_import(package, match):
    path = match[1:]

    import_path = package[:]
    while match and match[0] == '.':
        import_path = import_path[:-1]
        match = match[1:]

    if match:
        import_path.append(match)

    return '.'.join(import_path)


if __name__ == '__main__':
    for args in os.walk('../misago'):
        walk_directory(*args)

    print "\nDone! Don't forget to run isort to fix imports ordering!"
