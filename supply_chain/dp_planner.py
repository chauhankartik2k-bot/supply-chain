def knapsack_container(items, capacity):
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        name, weight, value = items[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weight <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weight] + value)
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(items[i - 1][0])
            w -= items[i - 1][1]
    selected.reverse()
    return dp[n][capacity], selected


def lcs_checkpoints(planned, actual):
    m = len(planned)
    n = len(actual)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if planned[i - 1] == actual[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    common = []
    i, j = m, n
    while i > 0 and j > 0:
        if planned[i - 1] == actual[j - 1]:
            common.insert(0, planned[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[m][n], common


def allocate_trucks(profit, trucks):
    regions = len(profit)
    dp = [[0] * (trucks + 1) for _ in range(regions + 1)]
    choice = [[0] * (trucks + 1) for _ in range(regions + 1)]
    for r in range(1, regions + 1):
        for t in range(trucks + 1):
            best = -1
            for k in range(t + 1):
                value = profit[r - 1][k] + dp[r - 1][t - k]
                if value > best:
                    best = value
                    choice[r][t] = k
            dp[r][t] = best
    plan = [0] * regions
    t = trucks
    for r in range(regions, 0, -1):
        plan[r - 1] = choice[r][t]
        t -= choice[r][t]
    return dp[regions][trucks], plan
