#!/usr/bin/env python3

import subprocess
import sys
import os
from pathlib import Path


def check_command_exists(command):
    try:
        subprocess.run([command])
    except subprocess.CalledProcessError:
        print(f"ERROR: Missing {command} dependency.", file=sys.stderr)
        sys.exit(1)

def main(charts: str = None, fail_fast: bool = False):

    # Check for required tools
    check_command_exists('kubectl')
    check_command_exists('helm')
    check_command_exists('kubectl-score')

    if charts is None:
        # Try to get the chart directory from an environment variable
        charts = os.environ.get('CHART_DIR')

    if not charts:
        print("Error: No chart directory provided.")
        print("Please set the CHART_DIR environment variable or provide a path as an argument.")
        sys.exit(1)

    if not Path(charts).is_dir():
        print(f"Error: Directory '{charts}' does not exist.")
        sys.exit(1)

    for dir in Path(charts).glob('*'):
        fails = 0
        if dir.is_dir():
            dir_name = dir.name
            
            helm_template_cmd = ["helm", "template", f"{charts}/{dir_name}"]
            kube_score_cmd = ["kubectl-score", "score", "-"]

            try:
                helm_process = subprocess.Popen(helm_template_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = helm_process.communicate()

                if helm_process.returncode != 0:
                    print(f"Error running helm template for {dir_name}: {error}", file=sys.stderr)
                    continue

                kube_score = subprocess.Popen(kube_score_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = kube_score.communicate(input=output)

                if kube_score.returncode != 0:
                    print(f"helm chart {dir_name}")
                    print(output.strip())
                    if fail_fast:
                        sys.exit(1)
                    fails += 1

            except subprocess.SubprocessError as e:
                print(f"Error running command for {dir_name}: {e}", file=sys.stderr)
                sys.exit(1)

        if fails > 0:
            sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Check Helm charts with kube-score")
    parser.add_argument("--charts", help="Path to the directory containing Helm charts")
    args = parser.parse_args()

    main(args.charts)