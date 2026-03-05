import sqlite3
import sys
from unittest.mock import MagicMock, patch

import pytest

from qase.commons.models.runtime import Runtime
from qase.commons.profilers.db import DatabaseProfiler, DatabaseProfilerSingleton


class TestDatabaseProfilerBasic:
    """TEST-04: DB profiler enable/disable, singleton lifecycle."""

    def setup_method(self):
        DatabaseProfilerSingleton._instance = None

    def teardown_method(self):
        DatabaseProfilerSingleton._instance = None

    def test_enable_registers_sqlite3(self):
        runtime = MagicMock(spec=Runtime)
        profiler = DatabaseProfiler(runtime=runtime)
        original_connect = sqlite3.connect
        try:
            profiler.enable()
            assert "sqlite3" in profiler._original_functions
            assert profiler._original_functions["sqlite3"] is original_connect
            assert sqlite3.connect is not original_connect
        finally:
            profiler.disable()

    def test_disable_restores_sqlite3(self):
        runtime = MagicMock(spec=Runtime)
        profiler = DatabaseProfiler(runtime=runtime)
        original_connect = sqlite3.connect
        try:
            profiler.enable()
            profiler.disable()
            assert sqlite3.connect is original_connect
            assert len(profiler._original_functions) == 0
        finally:
            # Safety net in case disable didn't work
            if sqlite3.connect is not original_connect:
                sqlite3.connect = original_connect

    def test_enable_disable_idempotent(self):
        runtime = MagicMock(spec=Runtime)
        profiler = DatabaseProfiler(runtime=runtime)
        original_connect = sqlite3.connect
        try:
            profiler.enable()
            profiler.enable()  # Second call should not crash or double-register
            assert "sqlite3" in profiler._original_functions
            assert profiler._original_functions["sqlite3"] is original_connect
            profiler.disable()
            assert sqlite3.connect is original_connect
        finally:
            if sqlite3.connect is not original_connect:
                sqlite3.connect = original_connect

    def test_singleton_init_and_get_instance(self):
        mock_runtime = MagicMock(spec=Runtime)
        DatabaseProfilerSingleton.init(runtime=mock_runtime)
        instance = DatabaseProfilerSingleton.get_instance()
        assert instance is not None
        assert instance.runtime is mock_runtime

    def test_singleton_raises_without_init(self):
        with pytest.raises(Exception, match="Init plugin first"):
            DatabaseProfilerSingleton.get_instance()

    def test_singleton_double_init_preserves_first(self):
        runtime_1 = MagicMock(spec=Runtime)
        runtime_2 = MagicMock(spec=Runtime)
        DatabaseProfilerSingleton.init(runtime=runtime_1)
        DatabaseProfilerSingleton.init(runtime=runtime_2)
        assert DatabaseProfilerSingleton.get_instance().runtime is runtime_1


class TestDatabaseProfilerErrors:
    """TEST-05: Error scenarios -- missing libs, forced ImportError, step recording."""

    def setup_method(self):
        DatabaseProfilerSingleton._instance = None

    def teardown_method(self):
        DatabaseProfilerSingleton._instance = None

    def test_enable_skips_unavailable_libraries(self):
        runtime = MagicMock(spec=Runtime)
        profiler = DatabaseProfiler(runtime=runtime)
        try:
            profiler.enable()  # Should not raise
            assert "sqlite3" in profiler._original_functions
        finally:
            profiler.disable()

    def test_enable_with_all_libs_missing_except_sqlite(self):
        runtime = MagicMock(spec=Runtime)
        profiler = DatabaseProfiler(runtime=runtime)
        with patch.dict(
            sys.modules,
            {
                "psycopg2": None,
                "pymysql": None,
                "pymysql.cursors": None,
                "pymongo": None,
                "pymongo.collection": None,
                "redis": None,
                "sqlalchemy": None,
                "sqlalchemy.engine": None,
            },
        ):
            try:
                profiler.enable()
                assert "sqlite3" in profiler._original_functions
                # Only sqlite3 should be registered (optional libs forced-missing)
                for key in profiler._original_functions:
                    assert key == "sqlite3", (
                        f"Unexpected library registered: {key}"
                    )
            finally:
                profiler.disable()

    def test_runtime_receives_steps_on_query(self):
        runtime = MagicMock(spec=Runtime)
        profiler = DatabaseProfiler(runtime=runtime)
        DatabaseProfilerSingleton.init(runtime=runtime)
        # Overwrite the singleton instance to use our profiler
        DatabaseProfilerSingleton._instance = profiler
        try:
            profiler.enable()
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            assert runtime.add_step.called
        finally:
            profiler.disable()
