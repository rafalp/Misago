import argparse
import logging
import sys

from zappa.cli import ZappaCLI

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    logger.root.addHandler(handler)

parser = argparse.ArgumentParser()
parser.add_argument('stage', type=str, help='stage for deployment')
parsed_args = parser.parse_args()

z = ZappaCLI()
z.stage_env = parsed_args.stage
z.api_stage = parsed_args.stage
z.load_settings()

run_deploy = False
try:
    logger.info("Checking zappa status")
    z.status()
except Exception:
    logger.exception("Zappa status check failed")
    run_deploy = True

if run_deploy:
    logger.info("Starting zappa deploy")
    try:
        z.deploy()
    except Exception as e:
        logger.exception("Zappa deploy exception")
        if str(e).find("already deployed") == -1:
            raise e
