from collections import deque

campus = {
    "Main Gate": {"Security Gate": 100},
    "Security Gate": {"Main Gate": 100, "Flag Pole": 120},
    "Flag Pole": {"Security Gate": 120, "Administration Block": 80},
    "Administration Block": {"Flag Pole": 80, "Block 2": 150, "Cafeteria": 30, "Library": 20},
    "Cafeteria": {"Administration Block": 30},
    "Library": {"Administration Block": 20},
    "Block 2": {"Administration Block": 150, "Food Court": 130},
    "Food Court": {"Block 2": 130, "Hostel Block": 200},
    "Hostel Block": {"Food Court": 200, "Mini Mart": 60, "Sports Area": 250},
    "Mini Mart": {"Hostel Block": 60},
    "Sports Area": {"Hostel Block": 250}
}
faq_data = {
    "Main Gate": "The main entrance of the university.",
    "Security Gate": "Security check near the entrance.",
    "Flag Pole": "Central flag area near Security Gate.",
    "Administration Block": "Main university office for administration.",
    "Cafeteria": "Located inside the Administration Block.",
    "Library": "Attached to the Administration Block.",
    "Block 2": "Academic block next to the Administration Block.",
    "Food Court": "Located near Block 2 for student dining.",
    "Hostel Block": "Accommodation area for students.",
    "Mini Mart": "Campus shop near Hostel Block.",
    "Sports Area": "Ground and outdoor sports facilities."
}

def bfs(graph, start, goal):
    visited = set()
    queue = deque([(start, [start], 0)])

    while queue:
        node, path, cost = queue.popleft()

        if node == goal:
            return path, cost, len(visited)

        if node not in visited:
            visited.add(node)
            for neighbor, dist in graph[node].items():
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor], cost + dist))

    return None, 0, len(visited)


def dfs(graph, start, goal):
    visited = set()
    stack = [(start, [start], 0)]

    while stack:
        node, path, cost = stack.pop()

        if node == goal:
            return path, cost, len(visited)

        if node not in visited:
            visited.add(node)
            for neighbor, dist in graph[node].items():
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], cost + dist))

    return None, 0, len(visited)

def print_result(path, cost, visited, method):
    if path:
        print(f"\n {method} Result:")
        print(" Path:", " → ".join(path))
        print(" Path length:", len(path))
        print(" Total cost:", cost, "meters")
        print(" Nodes visited:", visited, "\n")
    else:
        print(f"\n No path found using {method}.\n")


print(" Welcome to University Navigation System \n")

while True:
    print("Options:")
    print("1. Run BFS")
    print("2. Run DFS")
    print("3. Show All Locations")
    print("4. FAQ (Location Info)")
    print("5. Exit")

    choice = input("Choose option: ").strip()

    if choice == "5":
        print("Goodbye ")
        break

    elif choice == "3":
        print("\n University Locations:")
        for i, loc in enumerate(campus.keys(), start=1):
            print(f"{i}. {loc}")
        print("-" * 40)

    elif choice == "4":
        place = input("Enter place name: ").strip().title()
        if place in faq_data:
            print(f" {place}: {faq_data[place]}\n")
        else:
            print(" Sorry, location not found in FAQ.\n")

    elif choice in ["1", "2"]:
        start = input("Enter starting location: ").strip().title()
        end = input("Enter destination location: ").strip().title()

        if start not in campus or end not in campus:
            print(" Invalid location. Try again.\n")
            continue

        if choice == "1":
            path, cost, visited = bfs(campus, start, end)
            print_result(path, cost, visited, "BFS")
        elif choice == "2":
            path, cost, visited = dfs(campus, start, end)
            print_result(path, cost, visited, "DFS")

    else:
        print(" Invalid option. Please choose again.\n")

