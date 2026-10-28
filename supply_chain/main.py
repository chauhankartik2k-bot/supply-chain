from supplier_bst import SupplierBST
from order_heap import Order, OrderMinHeap, heap_sort
from supply_graph import SupplyGraph
from dp_planner import knapsack_container, lcs_checkpoints, allocate_trucks
from route_backtrack import tsp_branch_and_bound, min_dock_slots
from btree_index import BTree

SUPPLIERS = [
    (105, "Apex Steel Works", "India", 4.6),
    (102, "Orient Electronics", "Taiwan", 4.4),
    (110, "Rhein Machinery", "Germany", 4.7),
    (101, "Sagar Polymers", "India", 4.2),
    (104, "Hanil Batteries", "South Korea", 4.5),
    (108, "Nordic Shipping", "Denmark", 4.8),
    (112, "Alpen Auto Parts", "Germany", 4.3),
    (107, "Gulf Freight Co.", "UAE", 4.1),
]

ORDERS = [
    Order("O501", "Lithium cells", 2, 400),
    Order("O502", "Steel coils", 4, 120),
    Order("O503", "Life-saving medicines", 1, 50),
    Order("O504", "Cotton fabric", 5, 900),
    Order("O505", "Engine parts", 3, 260),
    Order("O506", "Vaccine boxes", 1, 75),
]

ROUTES = [
    ("Delhi", "Mumbai", 14), ("Delhi", "Kolkata", 15), ("Delhi", "Dubai", 22),
    ("Mumbai", "Chennai", 13), ("Mumbai", "Dubai", 18), ("Chennai", "Kolkata", 16),
    ("Chennai", "Singapore", 20), ("Kolkata", "Singapore", 21),
    ("Dubai", "Singapore", 30), ("Dubai", "Rotterdam", 35),
    ("Singapore", "Shanghai", 19), ("Singapore", "Rotterdam", 45),
    ("Shanghai", "Rotterdam", 48),
]

CARGO = [
    ("Steel coils", 8, 40),
    ("Electronics", 3, 50),
    ("Textiles", 5, 30),
    ("Auto parts", 6, 45),
    ("Medicines", 2, 35),
    ("Machinery", 9, 55),
]

CITIES = ["Mumbai", "Pune", "Nashik", "Surat", "Vadodara"]
CITY_COST = [
    [0, 150, 170, 280, 410],
    [150, 0, 210, 420, 540],
    [170, 210, 0, 250, 370],
    [280, 420, 250, 0, 150],
    [410, 540, 370, 150, 0],
]

SHIPMENTS = ["S1", "S2", "S3", "S4", "S5", "S6"]
CONFLICT = [
    [0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0],
]

TRACKING = [
    (4501, "Delivered"), (4510, "At Dubai Hub"), (4503, "Customs Check"),
    (4520, "Loaded on Ship"), (4507, "At Mumbai Port"), (4515, "In Transit"),
    (4502, "Delivered"), (4530, "Order Placed"), (4509, "At Singapore Hub"),
    (4512, "Out for Delivery"),
]


def build_network():
    graph = SupplyGraph()
    for u, v, cost in ROUTES:
        graph.add_route(u, v, cost)
    return graph


def supplier_module(ask=True):
    print("\n--- Supplier Directory (Binary Search Tree) ---")
    tree = SupplierBST()
    for sid, name, country, rating in SUPPLIERS:
        tree.insert(sid, name, country, rating)
    print("Inorder   (sorted IDs):", tree.inorder())
    print("Preorder  :", tree.preorder())
    print("Postorder :", tree.postorder())
    print("Height of tree:", tree.height())
    sid = 104
    if ask:
        sid = int(input("Enter supplier ID to search: "))
    node = tree.search(sid)
    if node:
        print("Found:", node.sid, node.name, "|", node.country, "| Rating", node.rating)
    else:
        print("Supplier", sid, "not found")
    tree.update_rating(107, 4.4)
    print("Rating of 107 updated to", tree.search(107).rating)
    tree.delete(105)
    print("After deleting 105, inorder:", tree.inorder())


def order_module():
    print("\n--- Urgent Order Queue (Min-Heap) ---")
    heap = OrderMinHeap()
    for order in ORDERS:
        heap.push(order)
    print("Most urgent order now:", heap.peek().order_id, heap.peek().item)
    print("Dispatch sequence (priority 1 = most urgent):")
    while heap.size() > 0:
        order = heap.pop()
        tag = "| P" + str(order.priority)
        print("  ", order.order_id, tag, "|", order.item, "| Qty", order.quantity)
    quantities = [order.quantity for order in ORDERS]
    print("Quantities before heap sort:", quantities)
    print("Quantities after heap sort :", heap_sort(quantities))


def network_module(ask=True):
    print("\n--- Supply Network (Graph) ---")
    graph = build_network()
    print("Locations:", len(graph.adj), "| Routes:", len(ROUTES))
    print("BFS from Delhi:", graph.bfs("Delhi"))
    print("DFS from Delhi:", graph.dfs("Delhi"))
    print("Network connected:", graph.is_connected())
    source, target = "Delhi", "Rotterdam"
    if ask:
        source = input("Enter source location: ").strip()
        target = input("Enter destination location: ").strip()
    if source not in graph.adj or target not in graph.adj:
        print("Unknown location")
    else:
        path, cost = graph.shortest_route(source, target)
        print("Cheapest route (Dijkstra):", " -> ".join(path), "| Cost:", cost)
    mst, total = graph.prim_mst()
    print("Prim MST cost:", total)
    mst, total = graph.kruskal_mst()
    print("Kruskal MST cost:", total)
    for u, v, cost in mst:
        print("  ", u, "-", v, ":", cost)
    names, dist = graph.floyd_warshall()
    i, j = names.index("Delhi"), names.index("Shanghai")
    print("Floyd-Warshall Delhi to Shanghai:", dist[i][j])


def planning_module():
    print("\n--- Container and Truck Planning (Dynamic Programming) ---")
    value, chosen = knapsack_container(CARGO, 20)
    print("0/1 Knapsack, capacity 20 tonnes")
    print("  Selected cargo:", chosen)
    print("  Total value (Rs. lakh):", value)
    planned = ["Factory", "Mumbai Port", "Dubai Hub", "Suez",
               "Rotterdam Port", "Warehouse"]
    actual = ["Factory", "Mumbai Port", "Colombo", "Dubai Hub",
              "Rotterdam Port", "Warehouse"]
    length, common = lcs_checkpoints(planned, actual)
    print("LCS of planned and actual checkpoints:", length)
    print("  Matched checkpoints:", common)
    print("  Route match:", round(length * 100 / len(planned), 1), "%")
    profit = [[0, 5, 9, 12, 14], [0, 6, 10, 13, 15], [0, 4, 8, 12, 15]]
    best, plan = allocate_trucks(profit, 4)
    print("Truck allocation (4 trucks, 3 regions)")
    print("  North:", plan[0], "South:", plan[1], "West:", plan[2], "| Profit:", best)


def routing_module():
    print("\n--- Delivery Tour and Dock Scheduling (Backtracking / B&B) ---")
    cost, route, explored = tsp_branch_and_bound(CITY_COST, CITIES)
    print("Best delivery tour (TSP):", " -> ".join(route))
    print("  Total distance:", cost, "km | Nodes explored:", explored)
    slots, colours = min_dock_slots(CONFLICT)
    print("Minimum dock time-slots needed (graph colouring):", slots)
    for i in range(len(SHIPMENTS)):
        print("  ", SHIPMENTS[i], "-> Slot", colours[i])


def tracking_module(ask=True):
    print("\n--- Shipment Tracking Index (B-Tree, t = 2) ---")
    index = BTree(2)
    for key, status in TRACKING:
        index.insert(key, status)
    print("Sorted tracking IDs:", index.traverse())
    for level, nodes in enumerate(index.levels()):
        print("  Level", level, ":", nodes)
    key = 4509
    if ask:
        key = int(input("Enter tracking ID: "))
    status = index.search(key)
    if status:
        print("Shipment", key, "status:", status)
    else:
        print("Shipment", key, "not found")


def full_demo():
    supplier_module(False)
    order_module()
    network_module(False)
    planning_module()
    routing_module()
    tracking_module(False)


def main():
    while True:
        print("\n===== Intelligent Global Supply Chain Collaboration Platform =====")
        print("1. Supplier Directory (BST)")
        print("2. Urgent Order Queue (Heap)")
        print("3. Supply Network Routes (Graph)")
        print("4. Container and Truck Planning (DP)")
        print("5. Delivery Tour and Dock Slots (Backtracking)")
        print("6. Shipment Tracking (B-Tree)")
        print("7. Run Full Demo")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            supplier_module()
        elif choice == "2":
            order_module()
        elif choice == "3":
            network_module()
        elif choice == "4":
            planning_module()
        elif choice == "5":
            routing_module()
        elif choice == "6":
            tracking_module()
        elif choice == "7":
            full_demo()
        elif choice == "0":
            print("Thank you!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
