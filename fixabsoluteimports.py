import os


def walk_directory(root, dirs, files):
    for file_path in files:
        if 'project_template' not in root and file_path.lower().endswith('.py'):
            clean_file(os.path.join(root, file_path))


def clean_file(file_path):
    py_source = file(file_path).read()
    if 'misago.' in py_source:
        package = file_path.rstrip('.py').split('/')[:-1]

        parse_file = True
        save_file = False
        cursor = 0

        while parse_file:
            try:
                import_start = py_source.index('from ', cursor)
                import_end = py_source.index(' import', import_start)
                cursor = import_end

                import_len = import_end - import_start
                import_path = py_source[import_start:import_end].lstrip('from').strip()

                if import_path.startswith('misago.'):
                    cleaned_import = clean_import(package, import_path.split('.'))
                    if cleaned_import:
                        save_file = True

                        cleaned_import_string = 'from {}'.format('.'.join(cleaned_import))
                        py_source = ''.join((py_source[:import_start], cleaned_import_string, py_source[import_end:]))
                        cursor -= import_end - import_start - len(cleaned_import_string)
            except ValueError:
                parse_file = False

        if save_file:
            with open(file_path, 'w') as package:
                print file_path
                package.write(py_source)


def clean_import(package, import_path):
    if len(package) < 2 or len(import_path) < 2:
        return

    if package[:2] != import_path[:2]:
        return

    if package == import_path:
        # import from sibling module
        return ['', '']

    if len(package) < len(import_path) and package == import_path[:len(package)]:
        # import from child module
        return [''] + import_path[len(package):]

    # find upwards path
    overlap_len = 2
    while True:
        if package[:overlap_len + 1] != import_path[:overlap_len + 1]:
            break
        overlap_len += 1

    upward_path = (['', ''] * (len(package) - overlap_len))[:-1]

    # append eventual downwards path
    return upward_path + import_path[overlap_len:]


if __name__ == '__main__':
    for args in os.walk('misago'):
        walk_directory(*args)

    print "\nDone! Don't forget to run isort to fix imports ordering!"
