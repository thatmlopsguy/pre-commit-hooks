#!/usr/bin/env python3

import logging
import subprocess
import sys
from pathlib import Path

from utils import check_command_exists

logger = logging.getLogger(__name__)


def main(check_type: str = "rules", files: list = None, fail_fast: bool = False):

    # Check for required tools
    check_command_exists("promtool")

    if not files:
        logger.error("No files provided.")
        sys.exit(1)

    valid_types = ("rules", "config")
    if check_type not in valid_types:
        logger.error(
            "Invalid check type '%s'. Must be one of: %s",
            check_type,
            ", ".join(valid_types),
        )
        sys.exit(1)

    fails = 0
    for filepath in files:
        path = Path(filepath)

        if not path.is_file():
            logger.error("File '%s' does not exist.", filepath)
            fails += 1
            continue

        cmd = ["promtool", "check", check_type, str(path)]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                logger.error("promtool check %s failed for %s!", check_type, filepath)
                if result.stdout.strip():
                    logger.error("%s", result.stdout.strip())
                if result.stderr.strip():
                    logger.error("%s", result.stderr.strip())
                if fail_fast:
                    sys.exit(1)
                fails += 1

        except subprocess.SubprocessError as e:
            logger.error("Error running promtool for %s: %s", filepath, e)
            sys.exit(1)

    if fails > 0:
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate Prometheus rules and configuration with promtool"
    )
    parser.add_argument(
        "--type",
        dest="check_type",
        default="rules",
        choices=["rules", "config"],
        help="Type of check to run: 'rules' or 'config' (default: rules)",
    )
    parser.add_argument(
        "--fail-fast", action="store_true", help="Exit on first failure"
    )
    parser.add_argument("files", nargs="*", help="Files to check")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main(check_type=args.check_type, files=args.files, fail_fast=args.fail_fast)
