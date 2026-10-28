INF = float("inf")


def tsp_branch_and_bound(cost, names):
    n = len(cost)
    min_edge = INF
    for i in range(n):
        for j in range(n):
            if i != j and cost[i][j] < min_edge:
                min_edge = cost[i][j]
    best = {"cost": INF, "path": [], "explored": 0}
    visited = [False] * n
    visited[0] = True

    def solve(city, count, current_cost, path):
        best["explored"] += 1
        if count == n:
            total = current_cost + cost[city][0]
            if total < best["cost"]:
                best["cost"] = total
                best["path"] = path + [0]
            return
        for nxt in range(n):
            if not visited[nxt]:
                new_cost = current_cost + cost[city][nxt]
                lower_bound = new_cost + (n - count) * min_edge
                if lower_bound < best["cost"]:
                    visited[nxt] = True
                    solve(nxt, count + 1, new_cost, path + [nxt])
                    visited[nxt] = False

    solve(0, 1, 0, [0])
    route = [names[i] for i in best["path"]]
    return best["cost"], route, best["explored"]


def is_safe(v, conflict, colour, c):
    for u in range(len(conflict)):
        if conflict[v][u] == 1 and colour[u] == c:
            return False
    return True


def colour_graph(conflict, m):
    n = len(conflict)
    colour = [0] * n

    def solve(v):
        if v == n:
            return True
        for c in range(1, m + 1):
            if is_safe(v, conflict, colour, c):
                colour[v] = c
                if solve(v + 1):
                    return True
                colour[v] = 0
        return False

    if solve(0):
        return colour
    return None


def min_dock_slots(conflict):
    for m in range(1, len(conflict) + 1):
        result = colour_graph(conflict, m)
        if result is not None:
            return m, result
    return 0, []
