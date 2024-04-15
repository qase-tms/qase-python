import os
import platform
import threading
import sys
import pip
import string
import uuid

from pkg_resources import DistributionNotFound, get_distribution


class QaseUtils:

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
    def package_version(name):
        try:
            version = get_distribution(name).version
        except DistributionNotFound:
            version = "unknown"
        return version


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
