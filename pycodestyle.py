"""
Code style cleanups done after yapf
"""
import argparse
import os

from extras import fixdictsformatting


CLEANUPS = [
    fixdictsformatting,
]


def walk_directory(root, dirs, files):
    for filename in files:
        if filename.lower().endswith('.py'):
            with open(os.path.join(root, filename), 'r') as f:
                filesource = f.read()

            org_source = filesource
            if 'migrate_settings_group' not in filesource:
                continue

            for cleanup in CLEANUPS:
                filesource = cleanup.fix_formatting(filesource)

            if org_source != filesource:
                print '====' * 8
                print os.path.join(root, filename)
                print ''
                print filesource


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='./')

    for args in os.walk(parser.parse_args().path):
        walk_directory(*args)
