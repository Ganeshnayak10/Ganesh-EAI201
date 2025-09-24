import tkinter as tk
from tkinter import scrolledtext
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

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Chatbot")

        
        self.root.state('zoomed')

       
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=80, height=20, font=("Arial", 12))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

       
        entry_frame = tk.Frame(root)
        entry_frame.pack(pady=(0,10), fill=tk.X)
        self.entry = tk.Entry(entry_frame, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, padx=(10,0), fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.handle_text_input)
        self.send_button = tk.Button(entry_frame, text="Send", command=self.handle_text_input)
        self.send_button.pack(side=tk.LEFT, padx=10)

       
        self.main_option_frame = tk.Frame(root)
        self.main_option_frame.pack(pady=20)

       
        self.scroll_frame = tk.Frame(root)
        self.scroll_frame.pack_forget() 

        self.button_canvas = tk.Canvas(self.scroll_frame, width=680, height=300)
        self.scrollbar = tk.Scrollbar(self.scroll_frame, orient="vertical", command=self.button_canvas.yview)
        self.button_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.button_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollable_button_frame = tk.Frame(self.button_canvas)
        self.scrollable_button_frame.bind(
            "<Configure>",
            lambda e: self.button_canvas.configure(scrollregion=self.button_canvas.bbox("all"))
        )
        self.button_canvas.create_window((0, 0), window=self.scrollable_button_frame, anchor="nw")

      
        def _on_mousewheel(event):
            self.button_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.button_canvas.bind_all("<MouseWheel>", _on_mousewheel)      # Windows
        self.button_canvas.bind_all("<Button-4>", lambda e: self.button_canvas.yview_scroll(-1, "units"))  # Linux scroll up
        self.button_canvas.bind_all("<Button-5>", lambda e: self.button_canvas.yview_scroll(1, "units"))   # Linux scroll down

        
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, anchor='w', padx=10, pady=10)

        exit_btn = tk.Button(self.bottom_frame, text="Exit Bot", command=self.root.quit, fg="white", bg="red", font=("Arial", 10, "bold"))
        exit_btn.pack()

     
        self.mode = None        
        self.travel_start = None

        
        self.insert_message("Bot", "🤖 Welcome to the University Campus Chatbot!")
        self.insert_message("Bot", "Please choose an option:")
        self.show_main_options()

    def insert_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def clear_buttons(self):
        for widget in self.main_option_frame.winfo_children():
            widget.destroy()
        for widget in self.scrollable_button_frame.winfo_children():
            widget.destroy()

    def show_main_options(self):
        self.mode = None
        self.travel_start = None
        self.entry.config(state='normal')
        self.send_button.config(state='normal')
        self.clear_buttons()

        
        self.scroll_frame.pack_forget()

        self.main_option_frame.pack(pady=20)

       
        faq_btn = tk.Button(self.main_option_frame, text="FAQ", width=20, height=3, font=("Arial", 18, "bold"), command=self.start_faq)
        faq_btn.pack(side=tk.LEFT, padx=30)

        travel_btn = tk.Button(self.main_option_frame, text="Plan Travel", width=20, height=3, font=("Arial", 18, "bold"), command=self.start_travel)
        travel_btn.pack(side=tk.LEFT, padx=30)

    def start_faq(self):
        self.mode = 'faq'
        self.insert_message("Bot", "Please select a location for FAQ:")
        self.entry.config(state='disabled')
        self.send_button.config(state='disabled')

        self.main_option_frame.pack_forget()
        
        self.scroll_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.show_location_buttons()

    def start_travel(self):
        self.mode = 'travel'
        self.travel_start = None
        self.insert_message("Bot", "Please select the **start point** for your travel:")
        self.entry.config(state='disabled')
        self.send_button.config(state='disabled')

        self.main_option_frame.pack_forget()
        self.scroll_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.show_location_buttons()

    def show_location_buttons(self):
        
        for widget in self.scrollable_button_frame.winfo_children():
            widget.destroy()

    
        for loc in sorted(campus.keys()):
            btn = tk.Button(self.scrollable_button_frame, text=loc, width=30, font=("Arial", 12))
            if self.mode == 'faq':
                btn.config(command=lambda l=loc: self.faq_selected(l))
            elif self.mode == 'travel':
                btn.config(command=lambda l=loc: self.travel_point_selected(l))
            btn.pack(pady=3, anchor='w')

     
        back_btn = tk.Button(self.scrollable_button_frame, text="Back to Main Menu", width=30, height=2,
                             font=("Arial", 14, "bold"), bg="#007acc", fg="white", command=self.back_to_main)
        back_btn.pack(pady=15)

    def faq_selected(self, location):
        answer = faq_data.get(location, "Sorry, no FAQ info available.")
        self.insert_message("You", location)
        self.insert_message("Bot", answer)
        self.insert_message("Bot", "Select another FAQ location or click 'Back to Main Menu'.")

    def travel_point_selected(self, location):
        if not self.travel_start:
            self.travel_start = location
            self.insert_message("You", f"Start point: {location}")
            self.insert_message("Bot", "Now please select the **end point**:")
        else:
            travel_end = location
            if travel_end == self.travel_start:
                self.insert_message("Bot", "Start and end points cannot be the same. Please select a different end point.")
                return

            self.insert_message("You", f"End point: {travel_end}")
            path, cost, visited = bfs(campus, self.travel_start, travel_end)
            if path:
                response = (f"🧭 Best path from {self.travel_start} to {travel_end}:\n"
                            f"Path: {' → '.join(path)}\nDistance: {cost} meters\nVisited nodes: {visited}")
            else:
                response = "Sorry, no path found between these locations."

            self.insert_message("Bot", response)
            self.insert_message("Bot", "Plan another travel by selecting a new start point or click 'Back to Main Menu'.")
            self.travel_start = None

    def back_to_main(self):
        self.scroll_frame.pack_forget()
        self.main_option_frame.pack(pady=20)
        self.entry.config(state='normal')
        self.send_button.config(state='normal')
        self.insert_message("Bot", "Back to main menu. Please choose an option:")
        self.show_main_options()

    def handle_text_input(self, event=None):
        user_msg = self.entry.get().strip()
        if not user_msg:
            return
        self.insert_message("You", user_msg)
        self.entry.delete(0, tk.END)

       
        if self.mode is None:
            lower = user_msg.lower()
            if any(g in lower for g in ["hi", "hello", "hey"]):
                self.insert_message("Bot", "Hello! 😊 How can I help you today?")
            elif "faq" in lower:
                self.start_faq()
            elif "travel" in lower or "plan" in lower:
                self.start_travel()
            elif "exit" in lower or "bye" in lower or "quit" in lower:
                self.insert_message("Bot", "Goodbye! 👋 Have a great day!")
                self.root.quit()
            else:
                self.insert_message("Bot", "Please use the buttons to interact or type 'FAQ' or 'Plan Travel'.")
        else:
            self.insert_message("Bot", "Please use the buttons to interact. Click 'Back to Main Menu' to switch modes.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()


