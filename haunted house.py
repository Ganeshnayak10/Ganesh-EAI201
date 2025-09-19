import math
import heapq
from collections import defaultdict

def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def diagonal(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy)

grid = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0]
]

start = (0, 0)
goal = (5, 5)

def get_neighbors(pos):
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors
def greedy_best_first(grid, start, goal, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start, goal), start))
    came_from = {start: None}
    visited = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        visited += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current):
            if neighbor not in came_from:
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))
                came_from[neighbor] = current

    path = []
    node = goal
    while node:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path, visited


def astar(grid, start, goal, heuristic):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    visited = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        visited += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    path = []
    node = goal
    while node:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path, visited

def print_path_in_rows(path):
    rows = defaultdict(list)
    for step in path:
        rows[step[0]].append(step)
    for row in sorted(rows):
        print(' '.join(str(cell) for cell in rows[row]))

print("\n Pathfinding in Haunted House\n")
print(f"Start: {start}, Goal: {goal}\n")

print(" GREEDY BEST-FIRST SEARCH\n")
for h_name, h_func in [("Euclidean", euclidean), ("Diagonal", diagonal)]:
    path, visited = greedy_best_first(grid, start, goal, h_func)
    print(f"Heuristic: {h_name}")
    print(" Path:")
    print_path_in_rows(path)
    print(" Path length:", len(path))
    print(" Nodes explored:", visited)
    print("-" * 40)

print("\n A* SEARCH\n")
for h_name, h_func in [("Euclidean", euclidean), ("Diagonal", diagonal)]:
    path, visited = astar(grid, start, goal, h_func)
    print(f"Heuristic: {h_name}")
    print(" Path:")
    print_path_in_rows(path)
    print(" Path length:", len(path))
    print(" Nodes explored:", visited)
    print("-" * 40)
