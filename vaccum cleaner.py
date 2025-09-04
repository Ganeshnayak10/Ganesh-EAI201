shape_map = {
    "c": "Circle",
    "s": "Square",
    "r": "Rectangle",
    "t": "Triangle"
}
shape_input = input("Enter shape (c=Circle, s=Square, r=Rectangle, t=Triangle): ").lower()

if shape_input not in shape_map:
    print("Invalid shape. Use: c, s, r, t.")
    exit()
shape = shape_map[shape_input]
print(f"\nYou selected: {shape} Vacuum Cleaner")

running = False

def show_cmds():
    print("\nCommands: a=auto, s=stop, l=left, r=right, d=dock, e=exit")
show_cmds()
while True:
    cmd = input("Enter command: ").lower()
    if cmd == "a":
        running = True
        print(f"{shape} Cleaner started in auto mode...")
        for side in ["left", "right"]:
            print(f"Sliding {side}... Path is clear.")
        show_cmds()
    elif cmd == "s":
        running = False
        print(f"{shape} Cleaner stopped.")
    elif cmd in "lr":
        if running:
            print(f"{shape} Cleaner turned {cmd}.")
        else:
            print("Start the cleaner first!")
    elif cmd == "d":
        print(f"{shape} Cleaner returning to dock.")
    elif cmd == "e":
        print("Exiting program.")
        break
    else:
        print("Invalid command.")
