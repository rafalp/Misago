"""
Code style cleanups done after yapf
"""
import argparse
import codecs
import os

from extras import fixdictsformatting


CLEANUPS = [
    fixdictsformatting,
]


def walk_directory(root, dirs, files):
    for filename in files:
        if filename.lower().endswith('.py'):
            with codecs.open(os.path.join(root, filename), 'r', 'utf-8') as f:
                filesource = f.read()

            org_source = filesource

            for cleanup in CLEANUPS:
                filesource = cleanup.fix_formatting(filesource)

            if org_source != filesource:
                print 'afterclean: %s' % os.path.join(root, filename)
                with codecs.open(os.path.join(root, filename), 'w', 'utf-8') as f:
                    f.write(filesource)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='./')

    for args in os.walk(parser.parse_args().path):
        walk_directory(*args)
