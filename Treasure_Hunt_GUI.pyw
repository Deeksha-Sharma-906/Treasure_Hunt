import tkinter as tk
import random

# -----------------------------
# Main Window Setup
# -----------------------------
root = tk.Tk()
root.title("Treasure Hunt Game")

# Global variables
size_choice = tk.StringVar(value="7")
cells = []
player_x = player_y = 0
treasure_x = treasure_y = 0
moves_left = 0
status_label = None
frame_buttons = None
frame_grid = None

# -----------------------------
# Map Size Selection UI
# -----------------------------
def show_map_selector():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Choose map size:", font=("Arial", 14)).pack(pady=10)
    for val in ["3", "5", "7", "10"]:
        tk.Radiobutton(root, text=f"{val}x{val}", variable=size_choice, value=val).pack(anchor="w")
    tk.Button(root, text="Start Game", command=start_game).pack(pady=10)

# -----------------------------
# Game Setup
# -----------------------------
def start_game():
    global player_x, player_y, treasure_x, treasure_y, moves_left, cells, status_label, frame_buttons, frame_grid

    size = int(size_choice.get())
    player_x, player_y = 0, 0
    treasure_x = random.randint(0, size - 1)
    treasure_y = random.randint(0, size - 1)
    moves_left = 10 if size in [3, 5] else 15
    cells = []

    for widget in root.winfo_children():
        widget.destroy()

    frame_buttons = tk.Frame(root)
    frame_buttons.pack(side=tk.LEFT, padx=10, pady=10)
    frame_grid = tk.Frame(root)
    frame_grid.pack(side=tk.RIGHT, padx=10, pady=10)

    status_label = tk.Label(frame_buttons, text=f"Moves left: {moves_left}", font=("Arial", 12))
    status_label.pack(pady=10)

    for y in range(size):
        row = []
        for x in range(size):
            lbl = tk.Label(frame_grid, text=".", width=4, height=2, bg="lightblue", font=("Arial", 14), relief="ridge")
            lbl.grid(row=y, column=x)
            row.append(lbl)
        cells.append(row)

    tk.Label(frame_buttons, text="Controls", font=("Arial", 14)).pack(pady=5)
    tk.Button(frame_buttons, text="Up", width=10, command=lambda: move_player(0, -1)).pack(pady=5)
    tk.Button(frame_buttons, text="Down", width=10, command=lambda: move_player(0, 1)).pack(pady=5)
    tk.Button(frame_buttons, text="Left", width=10, command=lambda: move_player(-1, 0)).pack(pady=5)
    tk.Button(frame_buttons, text="Right", width=10, command=lambda: move_player(1, 0)).pack(pady=5)

    update_grid()

# -----------------------------
# Game Logic
# -----------------------------
def update_grid():
    size = int(size_choice.get())
    for y in range(size):
        for x in range(size):
            if x == player_x and y == player_y:
                cells[y][x].config(text="P", bg="yellow")
            else:
                cells[y][x].config(text=".", bg="lightblue")

def reveal_treasure():
    cells[treasure_y][treasure_x].config(text="T", bg="gold")

def move_player(dx, dy):
    global player_x, player_y, moves_left
    size = int(size_choice.get())

    if moves_left <= 0:
        return

    new_x = player_x + dx
    new_y = player_y + dy

    if 0 <= new_x < size and 0 <= new_y < size:
        player_x, player_y = new_x, new_y
        moves_left -= 1
        update_grid()
        check_treasure()
    else:
        status_label.config(text="🚧 Can't move there!")

def check_treasure():
    if player_x == treasure_x and player_y == treasure_y:
        status_label.config(text="🎉 You found the treasure! 🎉")
        reveal_treasure()
        show_restart_button()
    elif moves_left == 0:
        dx = abs(player_x - treasure_x)
        dy = abs(player_y - treasure_y)
        total_distance = dx + dy
        if total_distance == 1:
            msg = "😮 Ohh you missed by just 1 step!"
        else:
            msg = f"💀 Game Over! You missed by ({dx},{dy}) → total {total_distance} steps away."
        status_label.config(text=msg)
        reveal_treasure()
        show_restart_button()
    else:
        status_label.config(text=f"Moves left: {moves_left}")

# -----------------------------
# Restart Option
# -----------------------------
def show_restart_button():
    tk.Button(frame_buttons, text="🔁 Restart Game", width=15, command=show_map_selector).pack(pady=10)

# -----------------------------
# Launch
# -----------------------------
show_map_selector()
root.mainloop()
