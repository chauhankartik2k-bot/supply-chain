from collections import deque

INF = float("inf")


class SupplyGraph:
    def __init__(self):
        self.adj = {}

    def add_location(self, name):
        if name not in self.adj:
            self.adj[name] = []

    def add_route(self, u, v, cost):
        self.add_location(u)
        self.add_location(v)
        self.adj[u].append((v, cost))
        self.adj[v].append((u, cost))

    def bfs(self, start):
        visited = [start]
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v, cost in self.adj[u]:
                if v not in visited:
                    visited.append(v)
                    queue.append(v)
        return visited

    def dfs(self, start):
        visited = []
        self._dfs(start, visited)
        return visited

    def _dfs(self, u, visited):
        visited.append(u)
        for v, cost in self.adj[u]:
            if v not in visited:
                self._dfs(v, visited)

    def is_connected(self):
        if len(self.adj) == 0:
            return True
        first = list(self.adj.keys())[0]
        return len(self.bfs(first)) == len(self.adj)

    def dijkstra(self, source):
        dist = {node: INF for node in self.adj}
        prev = {node: None for node in self.adj}
        dist[source] = 0
        done = set()
        while len(done) < len(self.adj):
            u = None
            for node in self.adj:
                if node not in done and (u is None or dist[node] < dist[u]):
                    u = node
            if dist[u] == INF:
                break
            done.add(u)
            for v, cost in self.adj[u]:
                if dist[u] + cost < dist[v]:
                    dist[v] = dist[u] + cost
                    prev[v] = u
        return dist, prev

    def shortest_route(self, source, target):
        dist, prev = self.dijkstra(source)
        if dist[target] == INF:
            return None, INF
        path = []
        node = target
        while node is not None:
            path.insert(0, node)
            node = prev[node]
        return path, dist[target]

    def prim_mst(self):
        start = list(self.adj.keys())[0]
        in_tree = {start}
        mst = []
        total = 0
        while len(in_tree) < len(self.adj):
            best = None
            for u in in_tree:
                for v, cost in self.adj[u]:
                    if v not in in_tree and (best is None or cost < best[2]):
                        best = (u, v, cost)
            if best is None:
                break
            mst.append(best)
            total += best[2]
            in_tree.add(best[1])
        return mst, total

    def kruskal_mst(self):
        edges = []
        for u in self.adj:
            for v, cost in self.adj[u]:
                if u < v:
                    edges.append((cost, u, v))
        edges.sort()
        parent = {node: node for node in self.adj}

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        mst = []
        total = 0
        for cost, u, v in edges:
            root_u = find(u)
            root_v = find(v)
            if root_u != root_v:
                parent[root_u] = root_v
                mst.append((u, v, cost))
                total += cost
        return mst, total

    def floyd_warshall(self):
        names = list(self.adj.keys())
        n = len(names)
        index = {names[i]: i for i in range(n)}
        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u in self.adj:
            for v, cost in self.adj[u]:
                dist[index[u]][index[v]] = cost
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return names, dist
