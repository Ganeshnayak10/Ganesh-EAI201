
campus = {
    "Main Gate": {"Security Gate": 100},
    "Security Gate": {"Main Gate": 100, "Flag Pole": 120},
    "Flag Pole": {"Security Gate": 120, "Administration Block": 80},
    "Administration Block": {"Flag Pole": 80, "Block 2": 150, "Cafeteria": 30},
    "Cafeteria": {"Administration Block": 30},  
    "Block 2": {"Administration Block": 150, "Food Court": 130},
    "Food Court": {"Block 2": 130, "Hostel Block": 200},
    "Hostel Block": {"Food Court": 200, "Mini Mart": 60, "Sports Area": 250},
    "Mini Mart": {"Hostel Block": 60},
    "Sports Area": {"Hostel Block": 250, "Student Center": 200},
    "Student Center": {"Sports Area": 200}
}
walking_speed = 1.4

def find_path(graph, start, end, visited=None, distance=0, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path = path + [start]

    if start == end:
        return distance, path

    shortest = None
    for place, dist in graph[start].items():
        if place not in visited:
            result = find_path(graph, place, end, visited.copy(), distance + dist, path)
            if result is not None:
                total_dist, new_path = result
                if shortest is None or total_dist < shortest[0]:
                    shortest = (total_dist, new_path)

    return shortest

start_point = "Main Gate"
end_point = "Student Center"

result = find_path(campus, start_point, end_point)

if result is not None:
    total_distance, route = result
    time_minutes = round(total_distance / walking_speed / 60, 2)
    print("Start:", start_point)
    print("End:", end_point)
    print("Route:", " → ".join(route))
    print("Total Distance:", total_distance, "meters")
    print("Estimated Time:", time_minutes, "minutes")
else:
    print(f"No path found between {start_point} and {end_point}")
