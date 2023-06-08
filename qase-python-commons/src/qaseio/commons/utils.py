import os
import threading
import sys
import pip

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
    def get_host_data() -> dict:
        return {
            "system": os.uname().sysname,
            "node": os.uname().nodename,
            "release": os.uname().release,
            "version": os.uname().version,
            "machine": os.uname().machine,
            'python': '.'.join(map(str, sys.version_info)),
            'pip': pip.__version__
        }
    
    @staticmethod
    def get_filename(path) -> str:
        return os.path.basename(path)