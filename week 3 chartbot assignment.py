import tkinter as tk
from tkinter import simpledialog, messagebox
import heapq

# -------------------- Backend Data --------------------
faq_data = {
    "Main Gate": "Main entrance of the university.",
    "Security Gate": "Security checkpoint near the entrance.",
    "Flag Pole": "Central flag area near the Security Gate.",
    "Administration Block": "Main university office. Connects to Cafeteria, Library, and Block 2.",
    "Cafeteria": "Dining area inside the Administration Block.",
    "Library": "Study and research space inside the Administration Block.",
    "Block 2": "Academic block adjacent to the Administration Block.",
    "Food Court": "Popular eating spot near Block 2.",
    "Hostel Block": "Student accommodation area.",
    "Mini Mart": "Campus convenience store near the Hostel Block.",
    "Sports Area": "Outdoor ground and sports facilities near Hostel Block."
}

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

# -------------------- Backend Logic --------------------
def shortest_path(graph, start, end):
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

# -------------------- Frontend GUI --------------------
def show_faq():
    place_input = simpledialog.askstring("FAQ", "Enter place name:")
    if not place_input:
        messagebox.showwarning("Invalid Input", "No place entered.")
        return

    # Normalize input to match graph keys
    place_input = place_input.strip().title()

    if place_input in faq_data:
        messagebox.showinfo("FAQ Result", f"{place_input}: {faq_data[place_input]}")
    else:
        messagebox.showwarning("Not Found", "Place not found in campus map.")

def show_locations():
    text = " University Locations:\n"
    for i, place in enumerate(faq_data.keys(), start=1):
        text += f"{i}. {place}\n"
    text += "----------------------------------------"
    messagebox.showinfo("All Locations", text)

def show_route():
    start = simpledialog.askstring("Route", "Enter starting place:")
    end = simpledialog.askstring("Route", "Enter destination place:")

    if not start or not end:
        messagebox.showwarning("Invalid", "Start and End places are required.")
        return

    start = start.strip().title()
    end = end.strip().title()

    if start not in campus or end not in campus:
        messagebox.showwarning("Invalid", "Invalid Start or End location.")
        return

    result = shortest_path(campus, start, end)
    if result:
        dist, route = result
        output = f" Route from {start} to {end}\nTotal Distance: {dist} meters\n"
        for i in range(len(route) - 1):
            curr, nxt = route[i], route[i+1]
            d = campus[curr][nxt]
            output += f"➡️ {curr} → {nxt} ({d} m)\n"
        messagebox.showinfo("Route Results", output)
    else:
        messagebox.showerror("Error", "No path found between selected locations.")

# -------------------- Launch GUI --------------------
root = tk.Tk()
root.title(" University Chatbot")
root.geometry("420x340")

label = tk.Label(root, text=" Welcome to University Chatbot", font=("Arial", 14))
label.pack(pady=10)

btn1 = tk.Button(root, text=" FAQ (Location Info)", width=35, command=show_faq)
btn1.pack(pady=5)

btn2 = tk.Button(root, text=" Show All Locations", width=35, command=show_locations)
btn2.pack(pady=5)

btn3 = tk.Button(root, text=" Best Route (Start → End)", width=35, command=show_route)
btn3.pack(pady=5)

btn_exit = tk.Button(root, text=" Exit", width=35, command=root.quit)
btn_exit.pack(pady=20)

root.mainloop()
