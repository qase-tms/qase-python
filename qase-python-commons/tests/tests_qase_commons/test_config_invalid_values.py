"""
One invalid setting must not discard the settings that come after it.
"""
import json
import os
from unittest.mock import patch

import pytest

from qase.commons.config import ConfigManager
from qase.commons.models.config.batch import BatchConfig
from qase.commons.models.config.qaseconfig import Mode


def _env_config(env):
    with patch.dict(os.environ, env, clear=True):
        return ConfigManager("/nonexistent/path.json").config


def _file_config(tmp_path, data):
    path = tmp_path / "qase.config.json"
    path.write_text(json.dumps(data))
    with patch.dict(os.environ, {}, clear=True):
        return ConfigManager(str(path)).config


class TestEnvConfig:

    @pytest.mark.parametrize("key", ["QASE_TESTOPS_RUN_ID", "QASE_TESTOPS_PLAN_ID",
                                     "QASE_TESTOPS_BATCH_SIZE"])
    def test_empty_numeric_value_is_treated_as_unset(self, key):
        config = _env_config({key: "", "QASE_MODE": "testops", "QASE_TESTOPS_PROJECT": "PRJ"})

        assert config.mode == Mode.testops
        assert config.testops.project == "PRJ"
        assert config.testops.run.id is None
        assert config.testops.plan.id is None
        assert config.testops.batch.size == 200

    def test_invalid_value_does_not_discard_other_variables(self):
        config = _env_config({
            "QASE_TESTOPS_RUN_ID": "abc",
            "QASE_MODE": "testops",
            "QASE_TESTOPS_PROJECT": "PRJ",
            "QASE_TESTOPS_BATCH_SIZE": "500",
            "QASE_REPORT_CONNECTION_PATH": "out",
        })

        assert config.mode == Mode.testops
        assert config.testops.project == "PRJ"
        assert config.testops.run.id is None
        assert config.testops.batch.size == 200
        assert config.report.connection.path == "out"


class TestFileConfig:

    def test_invalid_value_does_not_discard_rest_of_file(self, tmp_path):
        config = _file_config(tmp_path, {
            "mode": "unknown",
            "fallback": "report",
            "testops": {
                "project": "PRJ",
                "batch": {"size": -5},
                "statusFilter": ["skipped"],
            },
            "report": {"connection": {"path": "out"}},
            "framework": {"pytest": {"captureLogs": True}},
        })

        assert config.fallback == Mode.report
        assert config.testops.project == "PRJ"
        assert config.testops.batch.size == 200
        assert config.testops.status_filter == ["skipped"]
        assert config.report.connection.path == "out"
        assert config.framework.pytest.capture_logs is True

    def test_numeric_string_batch_size_is_accepted(self, tmp_path):
        config = _file_config(tmp_path, {"testops": {"batch": {"size": "50"}}})

        assert config.testops.batch.size == 50


class TestBatchSize:

    @pytest.mark.parametrize("size", [0, -1, 201])
    def test_out_of_range_size_is_rejected(self, size):
        with pytest.raises(ValueError):
            BatchConfig().set_size(size)
