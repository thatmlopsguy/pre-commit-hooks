#!/usr/bin/env python3

import subprocess
import sys
import os
from pathlib import Path


def check_command_exists(command):
    try:
        subprocess.run([command], capture_output=True)
    except subprocess.CalledProcessError:
        print(f"{command} not installed or available in the PATH", file=sys.stderr)
        sys.exit(1)

def main(charts: str = None, fail_fast: bool = False):

    # Check for required tools
    check_command_exists('pluto')
    check_command_exists('helm')

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

    fails = 0
    for dir in Path(charts).glob('*'):
        if dir.is_dir():
            dir_name = dir.name

            helm_template_cmd = ["helm", "template", f"{charts}/{dir_name}"]
            pluto_detect_cmd = ["pluto", "detect", "--no-footer", "-"]

            try:
                helm_process = subprocess.Popen(helm_template_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = helm_process.communicate()

                if helm_process.returncode != 0:
                    print(f"Error running helm template for {dir_name}: {error}", file=sys.stderr)
                    continue

                pluto_process = subprocess.Popen(pluto_detect_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = pluto_process.communicate(input=output)

                if pluto_process.returncode != 0:
                    print(f"helm chart {dir_name} needs attention!")
                    print(output.strip())
                    if fail_fast:
                        sys.exit(1)
                    fails += 1
                    continue

            except subprocess.SubprocessError as e:
                print(f"Error running command for {dir_name}: {e}", file=sys.stderr)
                sys.exit(1)

        if fails > 0:
            sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Check Helm charts with Pluto")
    parser.add_argument("--charts", help="Path to the directory containing Helm charts")
    args = parser.parse_args()

    main(args.charts)
