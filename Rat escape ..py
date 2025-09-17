from collections import deque
graph = {
    0: [(1, 2), (3, 5)],
    1: [(0, 2), (2, 4)],
    2: [(1, 4), (4, 1)],
    3: [(0, 5), (4, 1)],
    4: [(3, 1), (2, 1)]
}
def dfs(start, goal, visited=None, path=None, cost=0):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    visited.add(start)
    path = path + [start]
    if start == goal:
        return path, cost, len(visited)
    for neigh, c in graph[start]:
        if neigh not in visited:
            res = dfs(neigh, goal, visited, path, cost + c)
            if res:
                return res
    return None

def bfs(start, goal):
    q = deque([(start, [start], 0, set([start]))])
    while q:
        node, path, cost, visited = q.popleft()
        if node == goal:
            return path, cost, len(visited)
        for neigh, c in graph[node]:
            if neigh not in visited:
                q.append((neigh, path + [neigh], cost + c, visited | {neigh}))
    return None

start, goal = 1 ,4


dfs_path, dfs_cost, dfs_vis = dfs(start, goal)
bfs_path, bfs_cost, bfs_vis = bfs(start, goal)

print("DFS Path:", dfs_path, "Cost:", dfs_cost, "Visited:", dfs_vis)
print("BFS Path:", bfs_path, "Cost:", bfs_cost, "Visited:", bfs_vis)
