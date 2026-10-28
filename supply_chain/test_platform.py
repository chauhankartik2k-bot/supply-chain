from itertools import permutations
from supplier_bst import SupplierBST
from order_heap import heap_sort
from dp_planner import knapsack_container, lcs_checkpoints
from route_backtrack import tsp_branch_and_bound, min_dock_slots
from btree_index import BTree
from main import SUPPLIERS, build_network, CARGO, CITY_COST, CITIES, CONFLICT, TRACKING


def check(name, condition):
    print("PASS" if condition else "FAIL", "-", name)
    return condition


def run_tests():
    results = []

    tree = SupplierBST()
    for sid, name, country, rating in SUPPLIERS:
        tree.insert(sid, name, country, rating)
    ok = tree.inorder() == sorted(s[0] for s in SUPPLIERS)
    results.append(check("BST inorder is sorted", ok))
    ok = tree.search(999) is None
    results.append(check("BST search missing ID returns None", ok))
    tree.delete(105)
    ok = tree.inorder() == [101, 102, 104, 107, 108, 110, 112]
    results.append(check("BST delete root keeps order", ok))

    data = [50, 400, 120, 900, 260, 75]
    results.append(check("Heap sort matches sorted()", heap_sort(data) == sorted(data)))

    graph = build_network()
    path, cost = graph.shortest_route("Delhi", "Rotterdam")
    names, dist = graph.floyd_warshall()
    fw = dist[names.index("Delhi")][names.index("Rotterdam")]
    results.append(check("Dijkstra cost equals Floyd-Warshall", cost == fw))
    ok = graph.prim_mst()[1] == graph.kruskal_mst()[1]
    results.append(check("Prim and Kruskal give same MST cost", ok))

    best = 0
    n = len(CARGO)
    for mask in range(1 << n):
        weight = sum(CARGO[i][1] for i in range(n) if mask & (1 << i))
        value = sum(CARGO[i][2] for i in range(n) if mask & (1 << i))
        if weight <= 20:
            best = max(best, value)
    ok = knapsack_container(CARGO, 20)[0] == best
    results.append(check("Knapsack equals brute force", ok))
    ok = lcs_checkpoints(list("ABCBDAB"), list("BDCABA"))[0] == 4
    results.append(check("LCS of ABCBDAB and BDCABA is 4", ok))

    brute = min(
        sum(CITY_COST[a][b] for a, b in zip((0,) + p, p + (0,)))
        for p in permutations(range(1, len(CITIES)))
    )
    ok = tsp_branch_and_bound(CITY_COST, CITIES)[0] == brute
    results.append(check("TSP B&B equals brute force", ok))

    slots, colours = min_dock_slots(CONFLICT)
    ok = True
    for i in range(6):
        for j in range(6):
            if CONFLICT[i][j] == 1 and colours[i] == colours[j]:
                ok = False
    results.append(check("Dock colouring has no clash", ok))

    index = BTree(2)
    for key, status in TRACKING:
        index.insert(key, status)
    ok = index.traverse() == sorted(k for k, s in TRACKING)
    results.append(check("B-Tree traversal is sorted", ok))
    ok = all(index.search(k) == s for k, s in TRACKING)
    results.append(check("B-Tree finds every key", ok))

    print(sum(results), "of", len(results), "tests passed")


if __name__ == "__main__":
    run_tests()
