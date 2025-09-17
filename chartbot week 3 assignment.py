import tkinter as tk
from tkinter import simpledialog, messagebox

faq_data = {
    "main gate": "Main entrance of the university.",
    "security gate": "Security check near the entrance.",
    "flag pole": "Central flag area near Security Gate.",
    "administration block": "Main university office.",
    "cafeteria": "Inside the Administration Block.",
    "library": "Located inside the Administration Block (20 meters from it).",
    "block 2": "Academic block next to Admin Block.",
    "food court": "Located near Block 2.",
    "hostel block": "Accommodation for students.",
    "mini mart": "Campus shop near Hostel Block.",
    "sports area": "Outdoor ground and sports facilities."
}
\
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

def shortest_path(graph, start, end):
    import heapq
    q = [(0, start, [])]
    visited = set()
    while q:
        dist, node, path = heapq.heappop(q)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == end:
            return dist, path
        for neigh, d in graph.get(node, {}).items():
            if neigh not in visited:
                heapq.heappush(q, (dist + d, neigh, path))
    return None

def show_faq():
    place = simpledialog.askstring("FAQ", "Enter place name:").strip().lower()
    if place in faq_data:
        messagebox.showinfo("FAQ Result", f"{place.title()}: {faq_data[place]}")
    else:
        messagebox.showwarning("Not Found", "Place not in FAQ.")

def show_locations():
    text = " University Locations:\n"
    for i, place in enumerate(faq_data.keys(), start=1):
        text += f"{i}. {place.title()}\n"
    text += "----------------------------------------"
    messagebox.showinfo("All Locations", text)

def show_route():
    start = simpledialog.askstring("Route", "Enter starting place:").strip().title()
    end = simpledialog.askstring("Route", "Enter destination place:").strip().title()
    if start in campus and end in campus:
        result = shortest_path(campus, start, end)
        if result:
            dist, route = result
            route_text = f" Best Route from {start} to {end}\n Total Distance: {dist} meters\n\n"
            for i in range(len(route) - 1):
                curr, nxt = route[i], route[i+1]
                d = campus[curr][nxt]
                route_text += f" {curr} → {nxt} ({d} m)\n"
            messagebox.showinfo("Route Result", route_text)
        else:
            messagebox.showerror("Error", "No path found.")
    else:
        messagebox.showwarning("Invalid", "Invalid place names.")

root = tk.Tk()
root.title("🏫 University Chatbot")
root.geometry("400x250")

label = tk.Label(root, text="👋 Welcome to University Chatbot", font=("Arial", 14))
label.pack(pady=10)

btn1 = tk.Button(root, text="FAQ (Location Info)", width=25, command=show_faq)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Show All Locations", width=25, command=show_locations)
btn2.pack(pady=5)

btn3 = tk.Button(root, text="Best Route (Path Finding)", width=25, command=show_route)
btn3.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", width=25, command=root.quit)
btn_exit.pack(pady=20)

root.mainloop()
