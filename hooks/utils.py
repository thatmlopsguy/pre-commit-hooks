import logging
import subprocess
import sys

logger = logging.getLogger(__name__)


def check_command_exists(command):
    try:
        subprocess.run([command, "--version"], capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Missing %s dependency.", command)
        sys.exit(1)
