#!/usr/bin/python
import os, sys
import urllib2
from time import gmtime, strftime, time
try:
    from argparse import OptionParser
except ImportError:
    from optparse import OptionParser


def log_entry(logfile, response=None):
    if response and response.getcode() == 200:
        if response.time > 1:
            stopwatch = '%ss' % round(response.time, 3)
        else:
            stopwatch = '%sms' % int(response.time * 1000)
        msg = 'OK! HTTP 200 after %s' % stopwatch
    else:
        msg = 'FAIL!'

    print msg

    if logfile:
        lf = open(logfile, 'a+')
        lf.write('%s: ' % strftime("%a, %d %b %Y %X GMT", gmtime()))
        lf.write('%s\n' % msg)
        lf.close()


def heartbeat():
    # Change chdir to current file loation, then add it to pythonpath
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Parse options
    parser = OptionParser()
    parser.add_option("--timeout", dest="timeout", default=60, type="int",
                      help="Number of seconds after which heartbeat timeouts.")
    parser.add_option("--path", dest="pypath",
                      help="Add extra entry to python-path.")
    parser.add_option("--log", dest="logfile",
                      help="Log responses to file.", metavar="FILE")

    (options, argv) = parser.parse_args(sys.argv)

    # Set extra pythonpath?
    if options.pypath:
        sys.path.insert(0, options.pypath)

    # Validate timeout
    if options.timeout < 5 or options.timeout > 300:
        raise ValueError("Timeout cannot be lower than 5 seconds and greater than 5 minutes (300 seconds).")

    try:
        # Read Misago settings
        settings = __import__(argv[1]).settings
        BOARD_ADDRESS = settings.BOARD_ADDRESS
        HEARTBEAT_PATH = settings.HEARTBEAT_PATH

        # Validate
        if not BOARD_ADDRESS:
            raise ValueError('"BOARD_ADDRESS" setting is not set.')
        if not HEARTBEAT_PATH:
            raise ValueError('"HEARTBEAT_PATH" setting is not set.')

        request_url = '%s/%s' % (BOARD_ADDRESS, HEARTBEAT_PATH)

        # Send and handle request
        try:
            stopwatch = time()
            response = urllib2.urlopen(request_url, timeout=options.timeout)
            body = response.read()
            response.close()
            response.time = time() - stopwatch
            log_entry(options.logfile, response)
        except urllib2.URLError:
            log_entry(options.logfile)
    except IndexError:
        raise ValueError("You have to specify name of Misago's settings module used by your forum.")
    except ImportError:
        raise ValueError('"%s" could not be imported.' % argv[1])
    except AttributeError as e:
        raise ValueError('"%s" is not correct settings module.' % argv[1])


if __name__ == '__main__':
    heartbeat()
