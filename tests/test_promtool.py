import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from promtool import main
from utils import check_command_exists

FIXTURES = Path(__file__).resolve().parent / "example-prometheus"


# ── utils ────────────────────────────────────────────────────────────────


class TestCheckCommandExists:
    def test_command_found(self):
        check_command_exists("promtool")

    def test_command_not_found(self):
        with pytest.raises(SystemExit):
            check_command_exists("nonexistent_tool_xyz")


# ── check rules ──────────────────────────────────────────────────────────


class TestCheckRules:
    def test_valid_rules_pass(self):
        main(check_type="rules", files=[str(FIXTURES / "valid-rules.yml")])

    def test_invalid_rules_fail(self):
        with pytest.raises(SystemExit):
            main(check_type="rules", files=[str(FIXTURES / "invalid-rules.yml")])

    def test_rules_is_default_type(self):
        main(files=[str(FIXTURES / "valid-rules.yml")])


# ── check config ─────────────────────────────────────────────────────────


class TestCheckConfig:
    def test_valid_config_pass(self):
        main(check_type="config", files=[str(FIXTURES / "valid-config.yml")])

    def test_invalid_config_fail(self):
        with pytest.raises(SystemExit):
            main(check_type="config", files=[str(FIXTURES / "invalid-config.yml")])


# ── edge cases ───────────────────────────────────────────────────────────


class TestEdgeCases:
    def test_no_files_provided(self):
        with pytest.raises(SystemExit):
            main(check_type="rules", files=[])

    def test_nonexistent_file(self):
        with pytest.raises(SystemExit):
            main(check_type="rules", files=["/tmp/does_not_exist_promtool_test.yml"])

    def test_invalid_check_type(self):
        with pytest.raises(SystemExit):
            main(check_type="bogus", files=[str(FIXTURES / "valid-rules.yml")])

    def test_multiple_files_with_one_bad(self):
        with pytest.raises(SystemExit):
            main(
                check_type="rules",
                files=[
                    str(FIXTURES / "valid-rules.yml"),
                    str(FIXTURES / "invalid-rules.yml"),
                ],
            )

    def test_fail_fast_stops_early(self):
        with pytest.raises(SystemExit):
            main(
                check_type="rules",
                fail_fast=True,
                files=[
                    str(FIXTURES / "invalid-rules.yml"),
                    str(FIXTURES / "valid-rules.yml"),
                ],
            )

    def test_subprocess_error(self):
        with patch("promtool.check_command_exists"):  # skip dependency check
            with patch(
                "promtool.subprocess.run",
                side_effect=subprocess.SubprocessError("fail"),
            ):
                with pytest.raises(SystemExit):
                    main(check_type="rules", files=[str(FIXTURES / "valid-rules.yml")])
