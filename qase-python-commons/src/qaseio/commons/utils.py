class QaseUtils:

    @staticmethod
    def build_tree(items):
        tree = {}
        for uuid in items:
            step = items[uuid]
            if (step.get('parent_id', None)):
                parent_id = step.get('parent_id')
                items[parent_id]['steps'][uuid] = items[uuid]
            else: 
                tree[uuid] = step
        return tree