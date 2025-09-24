from flask import Flask, render_template, request, jsonify
from queue import PriorityQueue
import math

app = Flask(__name__)

# Coordinates of locations
locations = {
    'main_gate': (13.2200, 77.7539),
    'id_gate': (13.2214, 77.7549),
    'flag_pole': (13.2218, 77.7550),
    'admin_block': (13.2222, 77.7552),
    'library': (13.221971, 77.75558),
    'vending': (13.222264, 77.755126),
    'cafeteria': (13.22242, 77.755158),
    'lawn_area': (13.222775, 77.755576),
    'block_2': (13.22336, 77.755963),
    'food_court': (13.224758, 77.75725),
    'hostel': (13.224195, 77.758613),
    'sports_area': (13.22887, 77.7572)
}

# Graph representation with distances (in meters)
graph = {
    'main_gate': {'id_gate': 156},
    'id_gate': {'main_gate': 156, 'flag_pole': 45},
    'flag_pole': {'id_gate': 45, 'admin_block': 45, 'library': 30},
    'admin_block': {'flag_pole': 45, 'vending': 20, 'cafeteria': 25},
    'library': {'flag_pole': 30, 'vending': 35},
    'vending': {'admin_block': 20, 'library': 35, 'cafeteria': 15},
    'cafeteria': {'admin_block': 25, 'vending': 15, 'lawn_area': 50},
    'lawn_area': {'cafeteria': 50, 'block_2': 65},
    'block_2': {'lawn_area': 65, 'food_court': 85, 'hostel': 70},
    'food_court': {'block_2': 85, 'sports_area': 200},
    'hostel': {'block_2': 70, 'sports_area': 150},
    'sports_area': {'food_court': 200, 'hostel': 150}
}

def haversine_distance(coord1, coord2):
    """Calculate distance between two coordinates using Haversine formula"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def bfs(start, goal):
    """Breadth-First Search"""
    if start == goal:
        return [start], 0
    
    queue = [[start]]
    visited = set([start])
    
    while queue:
        path = queue.pop(0)
        node = path[-1]
        
        if node == goal:
            distance = calculate_path_distance(path)
            return path, distance
            
        for neighbor in graph.get(node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    
    return None, 0

def dfs(start, goal):
    """Depth-First Search"""
    if start == goal:
        return [start], 0
    
    stack = [[start]]
    visited = set([start])
    
    while stack:
        path = stack.pop()
        node = path[-1]
        
        if node == goal:
            distance = calculate_path_distance(path)
            return path, distance
            
        for neighbor in graph.get(node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)
    
    return None, 0

def ucs(start, goal):
    """Uniform Cost Search"""
    if start == goal:
        return [start], 0
    
    pq = PriorityQueue()
    pq.put((0, [start]))
    visited = set()
    
    while not pq.empty():
        cost, path = pq.get()
        node = path[-1]
        
        if node == goal:
            return path, cost
            
        if node not in visited:
            visited.add(node)
            
            for neighbor, edge_cost in graph.get(node, {}).items():
                if neighbor not in visited:
                    total_cost = cost + edge_cost
                    new_path = list(path)
                    new_path.append(neighbor)
                    pq.put((total_cost, new_path))
    
    return None, 0

def calculate_path_distance(path):
    """Calculate total distance of a path"""
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += graph[path[i]][path[i+1]]
    return total_distance

@app.route('/')
def index():
    return render_template('index.html', locations=locations.keys())

@app.route('/find-path', methods=['POST'])
def find_path():
    data = request.json
    start = data['start']
    goal = data['goal']
    algorithm = data['algorithm']
    
    if start not in locations or goal not in locations:
        return jsonify({'error': 'Invalid locations'}), 400
    
    if start == goal:
        return jsonify({'error': 'Start and goal cannot be the same'}), 400
    
    # Find path based on algorithm
    if algorithm == 'bfs':
        path, distance = bfs(start, goal)
    elif algorithm == 'dfs':
        path, distance = dfs(start, goal)
    elif algorithm == 'ucs':
        path, distance = ucs(start, goal)
    else:
        return jsonify({'error': 'Invalid algorithm'}), 400
    
    if not path:
        return jsonify({'error': 'No path found'}), 400
    
    # Convert path to coordinates
    path_coordinates = [{'lat': locations[node][0], 'lng': locations[node][1], 'name': node.replace('_', ' ').title()} for node in path]
    
    return jsonify({
        'path': path_coordinates,
        'distance': distance,
        'algorithm': algorithm.upper()
    })

if __name__ == '__main__':
    app.run(debug=True)
