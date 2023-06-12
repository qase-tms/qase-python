import os
import platform
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