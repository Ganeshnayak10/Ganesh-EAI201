shape = input("Shape (Circle/Square/Rectangle/Triangle): ")
print(f"{shape} Vacuum Cleaner selected.")

def show_commands():
    print("\nCommands:")
    print("a = Auto Clean")
    print("s = Stop")
    print("l = Turn Left")
    print("r = Turn Right")
    print("d = Dock")
    print("e = Exit")

show_commands()

while True:
    cmd = input("Enter command: ").lower()
    if cmd == "a":
        run = True
        print("Auto Clean started...")
        for side in ["left", "right"]:
            print(f"Sliding {side}... Path is clear.")
        show_commands()
    elif cmd == "s":
        run = False
        print("Stopped.")
    elif cmd in "lr":
        print(f"Turned {cmd}.") if run else print("Start first!")
    elif cmd == "d":
        print("Docking.")
    elif cmd == "e":
        print("Exiting.")
        break
    else:
        print("Invalid.")
