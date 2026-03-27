#!/usr/bin/env python3

import logging
import subprocess
import sys
import os
from pathlib import Path

from utils import check_command_exists

logger = logging.getLogger(__name__)


def main(charts: str = None, fail_fast: bool = False):

    # Check for required tools
    check_command_exists("kubectl")
    check_command_exists("helm")
    check_command_exists("kubectl-score")

    if charts is None:
        # Try to get the chart directory from an environment variable
        charts = os.environ.get("CHART_DIR")

    if not charts:
        logger.error("No chart directory provided.")
        logger.error(
            "Please set the CHART_DIR environment variable or provide a path as an argument."
        )
        sys.exit(1)

    if not Path(charts).is_dir():
        logger.error("Directory '%s' does not exist.", charts)
        sys.exit(1)

    fails = 0
    for dir in Path(charts).glob("*"):
        if dir.is_dir():
            dir_name = dir.name

            helm_template_cmd = ["helm", "template", f"{charts}/{dir_name}"]
            kube_score_cmd = ["kubectl-score", "score", "-"]

            try:
                helm_process = subprocess.Popen(
                    helm_template_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                output, error = helm_process.communicate()

                if helm_process.returncode != 0:
                    logger.error(
                        "Error running helm template for %s: %s", dir_name, error
                    )
                    continue

                kube_score = subprocess.Popen(
                    kube_score_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                output, error = kube_score.communicate(input=output)

                if kube_score.returncode != 0:
                    logger.error("helm chart %s needs attention!", dir_name)
                    logger.error("%s", output.strip())
                    if fail_fast:
                        sys.exit(1)
                    fails += 1
                    continue

            except subprocess.SubprocessError as e:
                logger.error("Error running command for %s: %s", dir_name, e)
                sys.exit(1)

        if fails > 0:
            sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Check Helm charts with kube-score")
    parser.add_argument("--charts", help="Path to the directory containing Helm charts")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main(args.charts)
