import os
import json
import tempfile
from unittest.mock import patch, MagicMock

from qase.commons.models.config.qaseconfig import QaseConfig, NetworkProfilerConfig
from qase.commons.models.runtime import Runtime
from qase.commons.profilers.network import NetworkProfiler, NetworkProfilerSingleton


class TestNetworkProfilerConfig:
    def test_default_initialization(self):
        config = NetworkProfilerConfig()
        assert config.exclude_hosts == []

    def test_set_exclude_hosts(self):
        config = NetworkProfilerConfig()
        config.set_exclude_hosts(["telemetry.local", "monitoring.internal"])
        assert config.exclude_hosts == ["telemetry.local", "monitoring.internal"]

    def test_qase_config_has_network_profiler(self):
        config = QaseConfig()
        assert isinstance(config.network_profiler, NetworkProfilerConfig)
        assert config.network_profiler.exclude_hosts == []


class TestSetProfilersMixedFormat:
    def test_string_only(self):
        config = QaseConfig()
        config.set_profilers(["network", "db"])
        assert config.profilers == ["network", "db"]
        assert config.network_profiler.exclude_hosts == []

    def test_dict_format_with_exclude_hosts(self):
        config = QaseConfig()
        config.set_profilers([
            {"name": "network", "excludeHosts": ["telemetry.local", "monitoring.internal"]},
            "db"
        ])
        assert config.profilers == ["network", "db"]
        assert config.network_profiler.exclude_hosts == ["telemetry.local", "monitoring.internal"]

    def test_dict_format_without_exclude_hosts(self):
        config = QaseConfig()
        config.set_profilers([{"name": "network"}])
        assert config.profilers == ["network"]
        assert config.network_profiler.exclude_hosts == []

    def test_dict_format_non_network(self):
        config = QaseConfig()
        config.set_profilers([{"name": "db", "excludeHosts": ["some.host"]}])
        assert config.profilers == ["db"]
        assert config.network_profiler.exclude_hosts == []

    def test_empty_profilers(self):
        config = QaseConfig()
        config.set_profilers([])
        assert config.profilers == []


class TestNetworkProfilerShouldSkip:
    def test_should_skip_matching_domain(self):
        runtime = MagicMock(spec=Runtime)
        profiler = NetworkProfiler(runtime=runtime, skip_domains=["api.qase.io", "telemetry.local"])
        assert profiler._should_skip("https://api.qase.io/v1/runs") is True
        assert profiler._should_skip("https://telemetry.local/track") is True

    def test_should_not_skip_non_matching_domain(self):
        runtime = MagicMock(spec=Runtime)
        profiler = NetworkProfiler(runtime=runtime, skip_domains=["api.qase.io"])
        assert profiler._should_skip("https://example.com/api") is False

    def test_should_skip_empty_domains(self):
        runtime = MagicMock(spec=Runtime)
        profiler = NetworkProfiler(runtime=runtime, skip_domains=[])
        assert profiler._should_skip("https://example.com") is False

    def test_should_skip_substring_match(self):
        runtime = MagicMock(spec=Runtime)
        profiler = NetworkProfiler(runtime=runtime, skip_domains=["telemetry"])
        assert profiler._should_skip("https://telemetry.example.com/track") is True
        assert profiler._should_skip("https://app.telemetry.io/data") is True


class TestNetworkProfilerEnvVar:
    def test_env_var_parsing(self):
        from qase.commons.config import ConfigManager

        with patch.dict(os.environ, {
            'QASE_PROFILER_NETWORK_EXCLUDE_HOSTS': 'telemetry.local,monitoring.internal'
        }):
            config_manager = ConfigManager()
            assert config_manager.config.network_profiler.exclude_hosts == [
                "telemetry.local", "monitoring.internal"
            ]

    def test_env_var_single_host(self):
        from qase.commons.config import ConfigManager

        with patch.dict(os.environ, {
            'QASE_PROFILER_NETWORK_EXCLUDE_HOSTS': 'telemetry.local'
        }):
            config_manager = ConfigManager()
            assert config_manager.config.network_profiler.exclude_hosts == ["telemetry.local"]


class TestNetworkProfilerFileConfig:
    def test_mixed_format_from_file(self):
        from qase.commons.config import ConfigManager

        config_data = {
            "profilers": [
                {"name": "network", "excludeHosts": ["telemetry.local"]},
                "db"
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name

        try:
            config_manager = ConfigManager(config_file)
            assert config_manager.config.profilers == ["network", "db"]
            assert config_manager.config.network_profiler.exclude_hosts == ["telemetry.local"]
        finally:
            os.unlink(config_file)

    def test_string_format_backward_compatible(self):
        from qase.commons.config import ConfigManager

        config_data = {
            "profilers": ["network", "db"]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name

        try:
            config_manager = ConfigManager(config_file)
            assert config_manager.config.profilers == ["network", "db"]
            assert config_manager.config.network_profiler.exclude_hosts == []
        finally:
            os.unlink(config_file)
