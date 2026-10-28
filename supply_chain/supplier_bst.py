class SupplierNode:
    def __init__(self, sid, name, country, rating):
        self.sid = sid
        self.name = name
        self.country = country
        self.rating = rating
        self.left = None
        self.right = None


class SupplierBST:
    def __init__(self):
        self.root = None

    def insert(self, sid, name, country, rating):
        new_node = SupplierNode(sid, name, country, rating)
        if self.root is None:
            self.root = new_node
            return
        current = self.root
        while True:
            if sid < current.sid:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            elif sid > current.sid:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right
            else:
                current.name = name
                current.country = country
                current.rating = rating
                return

    def search(self, sid):
        current = self.root
        while current is not None:
            if sid == current.sid:
                return current
            elif sid < current.sid:
                current = current.left
            else:
                current = current.right
        return None

    def update_rating(self, sid, new_rating):
        node = self.search(sid)
        if node is None:
            return False
        node.rating = new_rating
        return True

    def delete(self, sid):
        self.root = self._delete(self.root, sid)

    def _delete(self, node, sid):
        if node is None:
            return None
        if sid < node.sid:
            node.left = self._delete(node.left, sid)
        elif sid > node.sid:
            node.right = self._delete(node.right, sid)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.sid = successor.sid
            node.name = successor.name
            node.country = successor.country
            node.rating = successor.rating
            node.right = self._delete(node.right, successor.sid)
        return node

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.sid)
            self._inorder(node.right, result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node is not None:
            result.append(node.sid)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.sid)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))
