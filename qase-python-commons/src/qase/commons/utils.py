import os
import platform
import threading
import sys
from typing import Union, List
import pip
import string
import uuid
import time


class QaseUtils:

    @staticmethod
    def get_real_time() -> float:
        """
        Get real system time, bypassing time mocking libraries like freezegun.
        
        This is necessary when reporting test results to external systems that validate
        timestamps against current time, even when tests are using time mocking.
        
        Returns:
            float: Current Unix timestamp in seconds with microsecond precision
        """
        # Try to get the original time function if it was wrapped by freezegun
        # freezegun stores the original function in __wrapped__ attribute
        if hasattr(time.time, '__wrapped__'):
            return time.time.__wrapped__()
        
        # Fallback: use direct system call via ctypes
        # This works on Unix-like systems and Windows
        try:
            import ctypes
            import ctypes.util
            
            if sys.platform == 'win32':
                # Windows: use GetSystemTimeAsFileTime
                class FILETIME(ctypes.Structure):
                    _fields_ = [("dwLowDateTime", ctypes.c_uint32),
                                ("dwHighDateTime", ctypes.c_uint32)]
                
                kernel32 = ctypes.windll.kernel32
                ft = FILETIME()
                kernel32.GetSystemTimeAsFileTime(ctypes.byref(ft))
                
                # Convert FILETIME to Unix timestamp
                # FILETIME is 100-nanosecond intervals since January 1, 1601
                timestamp = (ft.dwHighDateTime << 32) + ft.dwLowDateTime
                # Convert to seconds and adjust epoch (1601 -> 1970)
                return (timestamp / 10000000.0) - 11644473600.0
            else:
                # Unix-like systems: use gettimeofday for microsecond precision
                # Try multiple approaches to find libc
                libc = None
                
                # Method 1: Use find_library (works on most systems)
                libc_path = ctypes.util.find_library('c')
                if libc_path:
                    try:
                        libc = ctypes.CDLL(libc_path)
                    except OSError:
                        pass
                
                # Method 2: Try common library names directly (for Alpine Linux, musl libc, etc.)
                if libc is None:
                    for lib_name in ['libc.so.6', 'libc.so', 'libc.dylib']:
                        try:
                            libc = ctypes.CDLL(lib_name)
                            break
                        except OSError:
                            continue
                
                if libc is None:
                    raise OSError("Could not load C library")
                
                class timeval(ctypes.Structure):
                    _fields_ = [("tv_sec", ctypes.c_long),
                                ("tv_usec", ctypes.c_long)]
                
                tv = timeval()
                libc.gettimeofday(ctypes.byref(tv), None)
                
                return float(tv.tv_sec) + (float(tv.tv_usec) / 1000000.0)
        except Exception:
            # Last resort: return the potentially mocked time
            # This will still work in normal cases without freezegun
            # If freezegun is active, the user might see timestamp validation errors
            # but the core functionality will continue to work
            return time.time()

    @staticmethod
    def build_tree(items):
        nodes = {item.id: item for item in items}

        roots = []
        for item in items:
            try:
                parent_id = item.parent_id
            except Exception as e:
                print(f'Failed to get parent id: {e}')

            if parent_id is None:
                # If the item has no parent, it's a root node
                roots.append(item)
            else:
                # If the item has a parent, add it to the parent's children list
                try:
                    parent = nodes[parent_id]
                    parent.steps.append(item)
                except Exception as e:
                    print(f'Failed to append child to parent: {e}')

        return roots

    @staticmethod
    def get_thread_name() -> str:
        return f"{os.getpid()}-{threading.current_thread().name}"

    @staticmethod
    def parse_bool(value) -> bool:
        return value in ("y", "yes", "true", "True", "TRUE", "1", 1, True)

    @staticmethod
    def uuid() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def get_host_data() -> dict:
        try:
            return {
                "system": platform.uname().system,
                "node": platform.uname().node,
                "release": platform.uname().release,
                "version": platform.uname().version,
                "machine": platform.uname().machine,
                'python': '.'.join(map(str, sys.version_info)),
                'pip': pip.__version__
            }
        except Exception as e:
            return {}

    @staticmethod
    def get_filename(path) -> str:
        return os.path.basename(path)

    @staticmethod
    def get_signature(testops_ids: Union[List[int], None], suites: List[str], params: dict) -> str:
        signature_parts = []

        if testops_ids:
            signature_parts.append(
                f"{'-'.join(map(str, testops_ids))}")

        for suite in suites:
            signature_parts.append(suite.lower().replace(" ", "_"))

        for key, val in params.items():
            signature_parts.append(f"{{{key}:{val}}}")

        return "::".join(signature_parts)


class StringFormatter(string.Formatter):
    """
        is designed to enhance string formatting by allowing it to gracefully handle and skip any keys in the format string 
        that are not provided in the arguments, rather than raising exceptions for missing keys or indexes. 
        This makes it particularly useful for formatting strings in contexts where not all variables may be known 
        or provided ahead of time, enhancing robustness and reducing the need for extensive error handling in code 
        that generates dynamic text output.
    """

    class SafeError(Exception):
        pass

    def get_value(self, key, args, kwargs):
        try:
            return super().get_value(key, args, kwargs)
        except (IndexError, KeyError):
            raise self.SafeError()

    def get_field(self, field, args, kwargs):
        try:
            return super().get_field(field, args, kwargs)
        except self.SafeError:
            return "{" + field + "}", field
