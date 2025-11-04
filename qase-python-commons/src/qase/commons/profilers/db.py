import sys
import time
import uuid
import threading
from functools import wraps
from typing import Optional, Any, Dict

from ..models.runtime import Runtime
from ..models.step import Step, StepDbQueryData, StepType


class DatabaseProfiler:
    _instance = None
    _lock = threading.Lock()

    def __init__(self, runtime: Runtime, track_on_fail: bool = True):
        self._original_functions = {}
        self.runtime = runtime
        self.track_on_fail = track_on_fail
        self.step = None

    def enable(self):
        """Enable database profiling for all supported database libraries."""
        # SQLAlchemy - try to enable (will skip if not available)
        self._enable_sqlalchemy()
        
        # psycopg2 (PostgreSQL) - try to enable (will skip if not available)
        self._enable_psycopg2()
        
        # pymysql (MySQL) - try to enable (will skip if not available)
        self._enable_pymysql()
        
        # sqlite3 (built-in) - try to enable (will skip if not available)
        self._enable_sqlite3()
        
        # pymongo (MongoDB) - try to enable (will skip if not available)
        self._enable_pymongo()
        
        # redis-py - try to enable (will skip if not available)
        self._enable_redis()

    def disable(self):
        """Disable database profiling and restore original functions."""
        for module_name, original_func in self._original_functions.items():
            if module_name == 'sqlalchemy':
                # SQLAlchemy 2.0+ uses event listeners
                try:
                    from sqlalchemy import event
                    from sqlalchemy.engine import Engine
                    
                    if isinstance(original_func, dict):
                        # Remove event listeners
                        if 'before' in original_func:
                            event.remove(Engine, "before_cursor_execute", original_func['before'])
                        if 'after' in original_func:
                            event.remove(Engine, "after_cursor_execute", original_func['after'])
                except (ImportError, AttributeError):
                    pass
            elif module_name == 'psycopg2':
                import psycopg2
                psycopg2.connect = original_func
            elif module_name == 'pymysql':
                import pymysql.cursors
                pymysql.cursors.Cursor.execute = original_func
            elif module_name == 'sqlite3':
                import sqlite3
                sqlite3.connect = original_func
            elif module_name == 'pymongo':
                import pymongo.collection
                pymongo.collection.Collection.find = original_func.get('find')
                pymongo.collection.Collection.find_one = original_func.get('find_one')
                pymongo.collection.Collection.insert_one = original_func.get('insert_one')
                pymongo.collection.Collection.update_one = original_func.get('update_one')
                pymongo.collection.Collection.delete_one = original_func.get('delete_one')
            elif module_name == 'redis':
                import redis
                redis.Redis.execute_command = original_func
        
        self._original_functions.clear()

    def _enable_sqlalchemy(self):
        """Enable profiling for SQLAlchemy."""
        try:
            import sqlalchemy
            from sqlalchemy import event
            from sqlalchemy.engine import Engine
            
            if 'sqlalchemy' not in self._original_functions:
                # SQLAlchemy 2.0+ uses event listeners instead of monkey patching
                # We'll use the before_cursor_execute and after_cursor_execute events
                
                def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
                    conn.info.setdefault('query_start_time', []).append(time.time())
                    return statement, parameters
                
                def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
                    try:
                        if conn.info.get('query_start_time'):
                            start_time = conn.info['query_start_time'].pop()
                            execution_time = time.time() - start_time
                            
                            query = str(statement)
                            if parameters:
                                try:
                                    query += f" | params: {parameters}"
                                except:
                                    pass
                            
                            DatabaseProfilerSingleton.get_instance()._log_db_query(
                                query=query,
                                database_type="SQLAlchemy",
                                execution_time=execution_time,
                                rows_affected=getattr(cursor, 'rowcount', None),
                                connection_info=f"SQLAlchemy Engine: {conn.engine.url}"
                            )
                    except Exception:
                        pass  # Don't break SQLAlchemy execution
                
                # Register event listeners
                event.listen(Engine, "before_cursor_execute", receive_before_cursor_execute)
                event.listen(Engine, "after_cursor_execute", receive_after_cursor_execute)
                
                # Store listeners for later removal
                self._original_functions['sqlalchemy'] = {
                    'before': receive_before_cursor_execute,
                    'after': receive_after_cursor_execute
                }
                
        except (ImportError, AttributeError):
            pass

    def _enable_psycopg2(self):
        """Enable profiling for psycopg2 (PostgreSQL)."""
        try:
            import psycopg2
            if 'psycopg2' not in self._original_functions:
                # psycopg2.extensions.cursor is a C extension and cannot be monkey-patched directly
                # Use monkey patching through connect function instead
                self._original_functions['psycopg2'] = psycopg2.connect
                psycopg2.connect = self._psycopg2_connect_wrapper(psycopg2.connect)
        except ImportError:
            pass

    def _enable_pymysql(self):
        """Enable profiling for pymysql (MySQL)."""
        try:
            import pymysql.cursors
            if 'pymysql' not in self._original_functions:
                self._original_functions['pymysql'] = pymysql.cursors.Cursor.execute
                pymysql.cursors.Cursor.execute = self._pymysql_execute_wrapper(
                    pymysql.cursors.Cursor.execute
                )
        except ImportError:
            pass

    def _enable_sqlite3(self):
        """Enable profiling for sqlite3."""
        try:
            import sqlite3
            if 'sqlite3' not in self._original_functions:
                # SQLite3 методы нельзя переопределить напрямую
                # Используем monkey patching через connect функцию
                self._original_functions['sqlite3'] = sqlite3.connect
                sqlite3.connect = self._sqlite3_connect_wrapper(sqlite3.connect)
        except ImportError:
            pass

    def _enable_pymongo(self):
        """Enable profiling for pymongo (MongoDB)."""
        try:
            import pymongo.collection
            if 'pymongo' not in self._original_functions:
                self._original_functions['pymongo'] = {
                    'find': pymongo.collection.Collection.find,
                    'find_one': pymongo.collection.Collection.find_one,
                    'insert_one': pymongo.collection.Collection.insert_one,
                    'update_one': pymongo.collection.Collection.update_one,
                    'delete_one': pymongo.collection.Collection.delete_one,
                }
                pymongo.collection.Collection.find = self._pymongo_find_wrapper(
                    pymongo.collection.Collection.find
                )
                pymongo.collection.Collection.find_one = self._pymongo_find_one_wrapper(
                    pymongo.collection.Collection.find_one
                )
                pymongo.collection.Collection.insert_one = self._pymongo_insert_wrapper(
                    pymongo.collection.Collection.insert_one
                )
                pymongo.collection.Collection.update_one = self._pymongo_update_wrapper(
                    pymongo.collection.Collection.update_one
                )
                pymongo.collection.Collection.delete_one = self._pymongo_delete_wrapper(
                    pymongo.collection.Collection.delete_one
                )
        except ImportError:
            pass

    def _enable_redis(self):
        """Enable profiling for redis-py."""
        try:
            import redis
            if 'redis' not in self._original_functions:
                self._original_functions['redis'] = redis.Redis.execute_command
                redis.Redis.execute_command = self._redis_execute_wrapper(
                    redis.Redis.execute_command
                )
        except ImportError:
            pass

    def _sqlalchemy_execute_wrapper(self, func):
        @wraps(func)
        def wrapper(self, statement, *args, **kwargs):
            start_time = time.time()
            query = str(statement) if hasattr(statement, '__str__') else str(statement)
            
            try:
                result = func(self, statement, *args, **kwargs)
                execution_time = time.time() - start_time
                
                self._log_db_query(
                    query=query,
                    database_type="SQLAlchemy",
                    execution_time=execution_time,
                    rows_affected=getattr(result, 'rowcount', None),
                    connection_info=f"SQLAlchemy Engine: {self.url}"
                )
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                if self.track_on_fail:
                    self._log_db_query(
                        query=query,
                        database_type="SQLAlchemy",
                        execution_time=execution_time,
                        connection_info=f"SQLAlchemy Engine: {self.url}",
                        error=str(e)
                    )
                raise
        
        return wrapper

    def _psycopg2_connect_wrapper(self, func):
        track_on_fail = self.track_on_fail
        profiler_instance = self  # Capture profiler instance
        
        class CursorProxy:
            """Proxy class for psycopg2 cursor to intercept execute method."""
            def __init__(self, cursor, conn):
                self._cursor = cursor
                self._conn = conn
            
            def execute(self, query, *args, **kwargs):
                """Execute query and log it."""
                start_time = time.time()
                error_msg = None
                
                try:
                    result = self._cursor.execute(query, *args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    # Get connection info
                    try:
                        dsn_params = self._conn.get_dsn_parameters()
                        host = dsn_params.get('host', 'localhost')
                    except Exception:
                        host = 'localhost'
                    
                    # Get rowcount safely
                    try:
                        rows_affected = self._cursor.rowcount
                    except Exception:
                        rows_affected = None
                    
                    # Log query - don't let logging break the execution
                    try:
                        profiler = DatabaseProfilerSingleton.get_instance()
                        profiler._log_db_query(
                            query=query,
                            database_type="PostgreSQL (psycopg2)",
                            execution_time=execution_time,
                            rows_affected=rows_affected,
                            connection_info=f"PostgreSQL: {host}"
                        )
                    except Exception:
                        # Silently ignore logging errors
                        pass
                    
                    return result
                except Exception as e:
                    error_msg = str(e)
                    execution_time = time.time() - start_time
                    
                    if track_on_fail:
                        try:
                            dsn_params = self._conn.get_dsn_parameters()
                            host = dsn_params.get('host', 'localhost')
                        except Exception:
                            host = 'localhost'
                        
                        # Log error - don't let logging break the exception propagation
                        try:
                            profiler = DatabaseProfilerSingleton.get_instance()
                            profiler._log_db_query(
                                query=query,
                                database_type="PostgreSQL (psycopg2)",
                                execution_time=execution_time,
                                connection_info=f"PostgreSQL: {host}",
                                error=error_msg
                            )
                        except Exception:
                            # Silently ignore logging errors
                            pass
                    
                    # Re-raise the original exception
                    raise
            
            def __getattr__(self, name):
                """Delegate all other attributes to the original cursor."""
                return getattr(self._cursor, name)
        
        class ConnectionProxy:
            """Proxy class for psycopg2 connection to intercept cursor creation."""
            def __init__(self, conn):
                self._conn = conn
            
            def cursor(self, *args, **kwargs):
                """Create cursor and return proxy."""
                cursor = self._conn.cursor(*args, **kwargs)
                return CursorProxy(cursor, self._conn)
            
            def __getattr__(self, name):
                """Delegate all other attributes to the original connection."""
                return getattr(self._conn, name)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the original connection
            conn = func(*args, **kwargs)
            
            # Return proxy instead of original connection
            return ConnectionProxy(conn)
        
        return wrapper

    def _psycopg2_execute_wrapper(self, func):
        @wraps(func)
        def wrapper(self, query, *args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(self, query, *args, **kwargs)
                execution_time = time.time() - start_time
                
                self._log_db_query(
                    query=query,
                    database_type="PostgreSQL (psycopg2)",
                    execution_time=execution_time,
                    rows_affected=self.rowcount,
                    connection_info=f"PostgreSQL: {self.connection.get_dsn_parameters().get('host', 'localhost')}"
                )
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                if self.track_on_fail:
                    self._log_db_query(
                        query=query,
                        database_type="PostgreSQL (psycopg2)",
                        execution_time=execution_time,
                        connection_info=f"PostgreSQL: {self.connection.get_dsn_parameters().get('host', 'localhost')}",
                        error=str(e)
                    )
                raise
        
        return wrapper

    def _pymysql_execute_wrapper(self, func):
        track_on_fail = self.track_on_fail
        
        @wraps(func)
        def wrapper(self, query, *args, **kwargs):
            start_time = time.time()
            error_msg = None
            
            try:
                result = func(self, query, *args, **kwargs)
                execution_time = time.time() - start_time
                
                # Get connection info safely
                try:
                    connection_info = f"MySQL: {self.connection.get_host_info()}"
                except Exception:
                    connection_info = "MySQL"
                
                # Get rowcount safely
                try:
                    rows_affected = self.rowcount
                except Exception:
                    rows_affected = None
                
                # Log query - don't let logging break the execution
                try:
                    profiler = DatabaseProfilerSingleton.get_instance()
                    profiler._log_db_query(
                        query=query,
                        database_type="MySQL (pymysql)",
                        execution_time=execution_time,
                        rows_affected=rows_affected,
                        connection_info=connection_info
                    )
                except Exception:
                    # Silently ignore logging errors
                    pass
                
                return result
            except Exception as e:
                error_msg = str(e)
                execution_time = time.time() - start_time
                
                if track_on_fail:
                    try:
                        connection_info = f"MySQL: {self.connection.get_host_info()}"
                    except Exception:
                        connection_info = "MySQL"
                    
                    # Log error - don't let logging break the exception propagation
                    try:
                        profiler = DatabaseProfilerSingleton.get_instance()
                        profiler._log_db_query(
                            query=query,
                            database_type="MySQL (pymysql)",
                            execution_time=execution_time,
                            connection_info=connection_info,
                            error=error_msg
                        )
                    except Exception:
                        # Silently ignore logging errors
                        pass
                
                # Re-raise the original exception
                raise
        
        return wrapper

    def _sqlite3_connect_wrapper(self, func):
        track_on_fail = self.track_on_fail
        
        class CursorProxy:
            """Proxy class for sqlite3 cursor to intercept execute method."""
            def __init__(self, cursor, conn):
                self._cursor = cursor
                self._conn = conn
            
            def execute(self, sql, *args, **kwargs):
                """Execute query and log it."""
                start_time = time.time()
                error_msg = None
                
                try:
                    result = self._cursor.execute(sql, *args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    # Get rowcount safely
                    try:
                        rows_affected = self._cursor.rowcount
                    except Exception:
                        rows_affected = None
                    
                    # Log query - don't let logging break the execution
                    try:
                        profiler = DatabaseProfilerSingleton.get_instance()
                        profiler._log_db_query(
                            query=sql,
                            database_type="SQLite",
                            execution_time=execution_time,
                            rows_affected=rows_affected,
                            connection_info="SQLite"
                        )
                    except Exception:
                        # Silently ignore logging errors
                        pass
                    
                    return result
                except Exception as e:
                    error_msg = str(e)
                    execution_time = time.time() - start_time
                    
                    if track_on_fail:
                        # Log error - don't let logging break the exception propagation
                        try:
                            profiler = DatabaseProfilerSingleton.get_instance()
                            profiler._log_db_query(
                                query=sql,
                                database_type="SQLite",
                                execution_time=execution_time,
                                connection_info="SQLite",
                                error=error_msg
                            )
                        except Exception:
                            # Silently ignore logging errors
                            pass
                    
                    # Re-raise the original exception
                    raise
            
            def __getattr__(self, name):
                """Delegate all other attributes to the original cursor."""
                return getattr(self._cursor, name)
        
        class ConnectionProxy:
            """Proxy class for sqlite3 connection to intercept cursor creation."""
            def __init__(self, conn):
                self._conn = conn
            
            def cursor(self, *args, **kwargs):
                """Create cursor and return proxy."""
                cursor = self._conn.cursor(*args, **kwargs)
                return CursorProxy(cursor, self._conn)
            
            def __getattr__(self, name):
                """Delegate all other attributes to the original connection."""
                return getattr(self._conn, name)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the original connection
            conn = func(*args, **kwargs)
            
            # Return proxy instead of original connection
            return ConnectionProxy(conn)
        
        return wrapper

    def _sqlite3_execute_wrapper(self, func):
        @wraps(func)
        def wrapper(self, sql, *args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(self, sql, *args, **kwargs)
                execution_time = time.time() - start_time
                
                self._log_db_query(
                    query=sql,
                    database_type="SQLite",
                    execution_time=execution_time,
                    rows_affected=self.rowcount,
                    connection_info=f"SQLite: {self.connection.execute('PRAGMA database_list').fetchone()}"
                )
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                if self.track_on_fail:
                    self._log_db_query(
                        query=sql,
                        database_type="SQLite",
                        execution_time=execution_time,
                        connection_info="SQLite",
                        error=str(e)
                    )
                raise
        
        return wrapper

    def _pymongo_find_wrapper(self, func):
        track_on_fail = self.track_on_fail
        
        @wraps(func)
        def wrapper(self, filter=None, *args, **kwargs):
            start_time = time.time()
            query = f"find({filter})"
            
            try:
                result = func(self, filter, *args, **kwargs)
                execution_time = time.time() - start_time
                
                # Get connection info safely
                try:
                    connection_info = f"MongoDB: {self.database.name}.{self.name}"
                except Exception:
                    connection_info = "MongoDB"
                
                # Log query - don't let logging break the execution
                try:
                    profiler = DatabaseProfilerSingleton.get_instance()
                    profiler._log_db_query(
                        query=query,
                        database_type="MongoDB (pymongo)",
                        execution_time=execution_time,
                        connection_info=connection_info
                    )
                except Exception:
                    # Silently ignore logging errors
                    pass
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                if track_on_fail:
                    try:
                        connection_info = f"MongoDB: {self.database.name}.{self.name}"
                    except Exception:
                        connection_info = "MongoDB"
                    
                    # Log error - don't let logging break the exception propagation
                    try:
                        profiler = DatabaseProfilerSingleton.get_instance()
                        profiler._log_db_query(
                            query=query,
                            database_type="MongoDB (pymongo)",
                            execution_time=execution_time,
                            connection_info=connection_info,
                            error=str(e)
                        )
                    except Exception:
                        # Silently ignore logging errors
                        pass
                raise
        
        return wrapper

    def _pymongo_find_one_wrapper(self, func):
        track_on_fail = self.track_on_fail
        
        @wraps(func)
        def wrapper(self, filter=None, *args, **kwargs):
            start_time = time.time()
            query = f"find_one({filter})"
            
            try:
                result = func(self, filter, *args, **kwargs)
                execution_time = time.time() - start_time
                
                # Get connection info safely
                try:
                    connection_info = f"MongoDB: {self.database.name}.{self.name}"
                except Exception:
                    connection_info = "MongoDB"
                
                # Log query - don't let logging break the execution
                try:
                    profiler = DatabaseProfilerSingleton.get_instance()
                    profiler._log_db_query(
                        query=query,
                        database_type="MongoDB (pymongo)",
                        execution_time=execution_time,
                        rows_affected=1 if result is not None else 0,
                        connection_info=connection_info
                    )
                except Exception:
                    # Silently ignore logging errors
                    pass
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                if track_on_fail:
                    try:
                        connection_info = f"MongoDB: {self.database.name}.{self.name}"
                    except Exception:
                        connection_info = "MongoDB"
                    
                    # Log error - don't let logging break the exception propagation
                    try:
                        profiler = DatabaseProfilerSingleton.get_instance()
                        profiler._log_db_query(
                            query=query,
                            database_type="MongoDB (pymongo)",
                            execution_time=execution_time,
                            connection_info=connection_info,
                            error=str(e)
                        )
                    except Exception:
                        # Silently ignore logging errors
                        pass
                raise
        
        return wrapper

    def _pymongo_insert_wrapper(self, func):
        track_on_fail = self.track_on_fail
        
        @wraps(func)
        def wrapper(self, document, *args, **kwargs):
            start_time = time.time()
            query = f"insert_one({document})"
            
            try:
                result = func(self, document, *args, **kwargs)
                execution_time = time.time() - start_time
                
                # Get connection info safely
                try:
                    connection_info = f"MongoDB: {self.database.name}.{self.name}"
                except Exception:
                    connection_info = "MongoDB"
                
                # Log query - don't let logging break the execution
                try:
                    profiler = DatabaseProfilerSingleton.get_instance()
                    profiler._log_db_query(
                        query=query,
                        database_type="MongoDB (pymongo)",
                        execution_time=execution_time,
                        rows_affected=1,
                        connection_info=connection_info
                    )
                except Exception:
                    # Silently ignore logging errors
                    pass
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                if track_on_fail:
                    try:
                        connection_info = f"MongoDB: {self.database.name}.{self.name}"
                    except Exception:
                        connection_info = "MongoDB"
                    
                    # Log error - don't let logging break the exception propagation
                    try:
                        profiler = DatabaseProfilerSingleton.get_instance()
                        profiler._log_db_query(
                            query=query,
                            database_type="MongoDB (pymongo)",
                            execution_time=execution_time,
                            connection_info=connection_info,
                            error=str(e)
                        )
                    except Exception:
                        # Silently ignore logging errors
                        pass
                raise
        
        return wrapper

    def _pymongo_update_wrapper(self, func):
        track_on_fail = self.track_on_fail
        
        @wraps(func)
        def wrapper(self, filter, update, *args, **kwargs):
            start_time = time.time()
            query = f"update_one({filter}, {update})"
            
            try:
                result = func(self, filter, update, *args, **kwargs)
                execution_time = time.time() - start_time
                
                # Get connection info safely
                try:
                    connection_info = f"MongoDB: {self.database.name}.{self.name}"
                except Exception:
                    connection_info = "MongoDB"
                
                # Get modified count safely
                try:
                    rows_affected = result.modified_count
                except Exception:
                    rows_affected = None
                
                # Log query - don't let logging break the execution
                try:
                    profiler = DatabaseProfilerSingleton.get_instance()
                    profiler._log_db_query(
                        query=query,
                        database_type="MongoDB (pymongo)",
                        execution_time=execution_time,
                        rows_affected=rows_affected,
                        connection_info=connection_info
                    )
                except Exception:
                    # Silently ignore logging errors
                    pass
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                if track_on_fail:
                    try:
                        connection_info = f"MongoDB: {self.database.name}.{self.name}"
                    except Exception:
                        connection_info = "MongoDB"
                    
                    # Log error - don't let logging break the exception propagation
                    try:
                        profiler = DatabaseProfilerSingleton.get_instance()
                        profiler._log_db_query(
                            query=query,
                            database_type="MongoDB (pymongo)",
                            execution_time=execution_time,
                            connection_info=connection_info,
                            error=str(e)
                        )
                    except Exception:
                        # Silently ignore logging errors
                        pass
                raise
        
        return wrapper

    def _pymongo_delete_wrapper(self, func):
        track_on_fail = self.track_on_fail
        
        @wraps(func)
        def wrapper(self, filter, *args, **kwargs):
            start_time = time.time()
            query = f"delete_one({filter})"
            
            try:
                result = func(self, filter, *args, **kwargs)
                execution_time = time.time() - start_time
                
                # Get connection info safely
                try:
                    connection_info = f"MongoDB: {self.database.name}.{self.name}"
                except Exception:
                    connection_info = "MongoDB"
                
                # Get deleted count safely
                try:
                    rows_affected = result.deleted_count
                except Exception:
                    rows_affected = None
                
                # Log query - don't let logging break the execution
                try:
                    profiler = DatabaseProfilerSingleton.get_instance()
                    profiler._log_db_query(
                        query=query,
                        database_type="MongoDB (pymongo)",
                        execution_time=execution_time,
                        rows_affected=rows_affected,
                        connection_info=connection_info
                    )
                except Exception:
                    # Silently ignore logging errors
                    pass
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                if track_on_fail:
                    try:
                        connection_info = f"MongoDB: {self.database.name}.{self.name}"
                    except Exception:
                        connection_info = "MongoDB"
                    
                    # Log error - don't let logging break the exception propagation
                    try:
                        profiler = DatabaseProfilerSingleton.get_instance()
                        profiler._log_db_query(
                            query=query,
                            database_type="MongoDB (pymongo)",
                            execution_time=execution_time,
                            connection_info=connection_info,
                            error=str(e)
                        )
                    except Exception:
                        # Silently ignore logging errors
                        pass
                raise
        
        return wrapper

    def _redis_execute_wrapper(self, func):
        track_on_fail = self.track_on_fail
        
        @wraps(func)
        def wrapper(self, command, *args, **kwargs):
            start_time = time.time()
            query = f"{command} {' '.join(map(str, args))}"
            
            try:
                result = func(self, command, *args, **kwargs)
                execution_time = time.time() - start_time
                
                # Get connection info safely
                try:
                    host = self.connection_pool.connection_kwargs.get('host', 'localhost')
                    port = self.connection_pool.connection_kwargs.get('port', 6379)
                    connection_info = f"Redis: {host}:{port}"
                except Exception:
                    connection_info = "Redis"
                
                # Log query - don't let logging break the execution
                try:
                    profiler = DatabaseProfilerSingleton.get_instance()
                    profiler._log_db_query(
                        query=query,
                        database_type="Redis",
                        execution_time=execution_time,
                        connection_info=connection_info
                    )
                except Exception:
                    # Silently ignore logging errors
                    pass
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                if track_on_fail:
                    try:
                        host = self.connection_pool.connection_kwargs.get('host', 'localhost')
                        port = self.connection_pool.connection_kwargs.get('port', 6379)
                        connection_info = f"Redis: {host}:{port}"
                    except Exception:
                        connection_info = "Redis"
                    
                    # Log error - don't let logging break the exception propagation
                    try:
                        profiler = DatabaseProfilerSingleton.get_instance()
                        profiler._log_db_query(
                            query=query,
                            database_type="Redis",
                            execution_time=execution_time,
                            connection_info=connection_info,
                            error=str(e)
                        )
                    except Exception:
                        # Silently ignore logging errors
                        pass
                
                # Re-raise the original exception
                raise
        
        return wrapper

    def _log_db_query(self, query: str, database_type: str, execution_time: float,
                     rows_affected: Optional[int] = None, connection_info: Optional[str] = None,
                     error: Optional[str] = None):
        """Log database query as a step."""
        step_data = StepDbQueryData(
            query=query,
            database_type=database_type,
            execution_time=execution_time,
            rows_affected=rows_affected,
            connection_info=connection_info
        )
        
        step = Step(
            id=str(uuid.uuid4()),
            step_type=StepType.DB_QUERY,
            data=step_data
        )
        
        self.runtime.add_step(step)
        
        # Determine step status based on error
        status = 'failed' if error else 'passed'
        self.runtime.finish_step(
            id=step.id,
            status=status
        )


class DatabaseProfilerSingleton:
    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def init(**kwargs):
        if DatabaseProfilerSingleton._instance is None:
            with DatabaseProfilerSingleton._lock:
                if DatabaseProfilerSingleton._instance is None:
                    DatabaseProfilerSingleton._instance = DatabaseProfiler(**kwargs)

    @staticmethod
    def get_instance() -> DatabaseProfiler:
        """Static access method"""
        if DatabaseProfilerSingleton._instance is None:
            raise Exception("Init plugin first")
        return DatabaseProfilerSingleton._instance

    def __init__(self):
        """Virtually private constructor"""
        raise Exception("Use get_instance()")
