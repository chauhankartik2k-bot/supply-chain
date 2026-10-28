class BTreeNode:
    def __init__(self, leaf):
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []


class BTree:
    def __init__(self, t=2):
        self.t = t
        self.root = BTreeNode(True)

    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        if node.leaf:
            return None
        return self.search(key, node.children[i])

    def insert(self, key, value):
        if self.search(key) is not None:
            return False
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)
        return True

    def _split_child(self, parent, i):
        t = self.t
        full = parent.children[i]
        new_node = BTreeNode(full.leaf)
        parent.keys.insert(i, full.keys[t - 1])
        parent.values.insert(i, full.values[t - 1])
        parent.children.insert(i + 1, new_node)
        new_node.keys = full.keys[t:]
        new_node.values = full.values[t:]
        full.keys = full.keys[:t - 1]
        full.values = full.values[:t - 1]
        if not full.leaf:
            new_node.children = full.children[t:]
            full.children = full.children[:t]

    def _insert_non_full(self, node, key, value):
        i = len(node.keys) - 1
        if node.leaf:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            node.keys.insert(i + 1, key)
            node.values.insert(i + 1, value)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def traverse(self):
        result = []
        self._traverse(self.root, result)
        return result

    def _traverse(self, node, result):
        for i in range(len(node.keys)):
            if not node.leaf:
                self._traverse(node.children[i], result)
            result.append(node.keys[i])
        if not node.leaf:
            self._traverse(node.children[len(node.keys)], result)

    def levels(self):
        result = []
        current = [self.root]
        while current:
            result.append([node.keys for node in current])
            next_level = []
            for node in current:
                next_level.extend(node.children)
            current = next_level
        return result
