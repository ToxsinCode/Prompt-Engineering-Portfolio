import tkinter as tk
from tkinter import messagebox, ttk
import heapq

#Action Definitions
class Action:
    def __init__(self, name, damage, action_type, effect=None):
        self.name = name
        self.damage = damage
        self.action_type = action_type  # 'Attack', 'Heal', or 'Effect'
        self.effect = effect  # Optional special effect

action_catalogue = {
    "Slash": Action("Slash", 10, "Attack"),
    "Fireball": Action("Fireball", 15, "Attack", effect="Burn"),
    "Heal": Action("Heal", -10, "Heal"),  # Negative damage means healing
    "Defend": Action("Defend", 0, "Effect", effect="Increase defense")
}

#Character Class
class Character:
    def __init__(self, name, speed, health=100):
        self.name = name
        self.speed = speed
        self.health = health
        self.action_time = 0
        self.current_action = action_catalogue["Slash"]  # Default action
        self.learned_actions = list(action_catalogue.keys())  # Learned actions

    def __lt__(self, other):
        if self.action_time == other.action_time:
            return self.speed > other.speed
        return self.action_time < other.action_time

    def perform_action(self, target):
        action = self.current_action
        print(f"{self.name} uses {action.name} on {target.name}!")
        if action.effect:
            print(f"{target.name} is affected by {action.effect}!")
        target.health -= action.damage
        print(f"{target.name}'s health is now {target.health}.")
        self.action_time += 100 / self.speed

#Character Management

characters = []

def add_character():
    name = entry_name.get()
    speed = entry_speed.get()
    health = entry_health.get()

    if not name or not speed or not health:
        messagebox.showerror("Error", "Please enter name, speed, and health.")
        return

    try:
        speed = int(speed)
        health = int(health)
    except ValueError:
        messagebox.showerror("Error", "Speed and health must be integers.")
        return

    characters.append(Character(name, speed, health))
    listbox_characters.insert(tk.END, f"{name} (Speed: {speed}, Health: {health})")
    entry_name.delete(0, tk.END)
    entry_speed.delete(0, tk.END)
    entry_health.delete(0, tk.END)

def delete_character():
    selected_indices = listbox_characters.curselection()
    for index in selected_indices[::-1]:
        listbox_characters.delete(index)
        del characters[index]

def update_character():
    selected_index = listbox_characters.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Please select a character to update.")
        return

    selected_index = selected_index[0]
    name = entry_name.get()
    speed = entry_speed.get()
    health = entry_health.get()

    if not name or not speed or not health:
        messagebox.showerror("Error", "Please enter name, speed, and health.")
        return

    try:
        speed = int(speed)
        health = int(health)
    except ValueError:
        messagebox.showerror("Error", "Speed and health must be integers.")
        return

    characters[selected_index].name = name
    characters[selected_index].speed = speed
    characters[selected_index].health = health
    listbox_characters.delete(selected_index)
    listbox_characters.insert(selected_index, f"{name} (Speed: {speed}, Health: {health})")
    entry_name.delete(0, tk.END)
    entry_speed.delete(0, tk.END)
    entry_health.delete(0, tk.END)

#Simulation Functions

turn_queue = []

def start_simulation():
    global turn_queue
    turn_queue = []
    if not characters:
        messagebox.showerror("Error", "No characters to simulate.")
        return

    for character in characters:
        heapq.heappush(turn_queue, (character.action_time, character))

    result_text.delete(1.0, tk.END)
    simulate_turn()

def simulate_turn():
    global turn_queue
    if turn_queue:
        current_time, current_character = heapq.heappop(turn_queue)
        result_text.insert(tk.END, f"{current_character.name} takes action '{current_character.current_action.name}' at time {current_time:.2f}\n")
        # Allow user to select target for action
        select_target(current_character)
    else:
        messagebox.showinfo("Info", "Simulation complete.")

def perform_action_with_target(character, target):
    character.perform_action(target)
    heapq.heappush(turn_queue, (character.action_time, character))
    result_text.insert(tk.END, f"{character.name} performs '{character.current_action.name}' on {target.name}\n")

def exit_simulation():
    confirm_exit = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?")
    if confirm_exit:
        window.destroy()

def delete_character():
    selected_indices = listbox_characters.curselection()
    for index in selected_indices[::-1]:
        listbox_characters.delete(index)
        del characters[index]

def set_current_action(character, action_name):
    character.current_action = action_catalogue[action_name]

def update_action_dropdown(event):
    selected_index = listbox_characters.curselection()
    if selected_index:
        selected_index = selected_index[0]
        character = characters[selected_index]
        selected_attack.set(character.current_action.name)
        action_menu["menu"].delete(0, "end")
        for action_name in character.learned_actions:
            if action_catalogue[action_name].action_type == "Attack":
                action_menu["menu"].add_command(label=action_name, command=tk._setit(selected_attack, action_name, lambda name=action_name: set_current_action(character, name)))
        selected_heal.set(character.current_action.name)
        heal_menu["menu"].delete(0, "end")
        for action_name in character.learned_actions:
            if action_catalogue[action_name].action_type == "Heal":
                heal_menu["menu"].add_command(label=action_name, command=tk._setit(selected_heal, action_name, lambda name=action_name: set_current_action(character, name)))

def select_target(current_character):
    def on_target_select():
        selected_target_index = listbox_targets.curselection()
        if selected_target_index:
            selected_target_index = selected_target_index[0]
            target = characters[selected_target_index]
            perform_action_with_target(current_character, target)
        target_window.destroy()

    target_window = tk.Toplevel(window)
    target_window.title("Select Target")

    listbox_targets = tk.Listbox(target_window)
    listbox_targets.pack(pady=10)

    for i, character in enumerate(characters):
        listbox_targets.insert(tk.END, f"{character.name} (HP: {character.health})")

    button_select_target = tk.Button(target_window, text="Select", command=on_target_select)
    button_select_target.pack(pady=5)


# UI setup
window = tk.Tk()
window.title("Character Manager")

frame = tk.Frame(window)
frame.pack(pady=10)

label_name = tk.Label(frame, text="Name:")
label_name.grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

label_speed = tk.Label(frame, text="Speed:")
label_speed.grid(row=1, column=0, padx=5, pady=5)
entry_speed = tk.Entry(frame)
entry_speed.grid(row=1, column=1, padx=5, pady=5)

label_health = tk.Label(frame, text="Health:")
label_health.grid(row=2, column=0, padx=5, pady=5)
entry_health = tk.Entry(frame)
entry_health.grid(row=2, column=1, padx=5, pady=5)

button_add = tk.Button(frame, text="Add Character", command=add_character)
button_add.grid(row=3, column=0, columnspan=2, pady=5)

button_delete = tk.Button(frame, text="Delete Character", command=delete_character)
button_delete.grid(row=4, column=0, columnspan=2, pady=5)

button_update = tk.Button(frame, text="Update Character", command=update_character)
button_update.grid(row=5, column=0, columnspan=2, pady=5)

listbox_characters = tk.Listbox(window)
listbox_characters.pack(pady=10)

# Dropdown menu for selecting attacks
def update_action_dropdown(event):
    selected_index = listbox_characters.curselection()
    if selected_index:
        selected_index = selected_index[0]
        character = characters[selected_index]
        selected_attack.set(character.current_action.name)
        action_menu["menu"].delete(0, "end")
        for attack_name in character.learned_actions:
            action_menu["menu"].add_command(label=attack_name, command=tk._setit(selected_attack, attack_name, lambda name=attack_name: set_current_action(character, name)))

label_attack = tk.Label(frame, text="Action:")
label_attack.grid(row=6, column=0, padx=5, pady=5)

selected_attack = tk.StringVar()
selected_attack.set("Select Action")
action_menu = tk.OptionMenu(frame, selected_attack, *action_catalogue.keys())
action_menu.grid(row=6, column=1, padx=5, pady=5)

listbox_characters.bind("<<ListboxSelect>>", update_action_dropdown)

button_simulate = tk.Button(frame, text="Start Simulation", command=start_simulation)
button_simulate.grid(row=7, column=0, columnspan=2, pady=5)

button_next = tk.Button(frame, text="Next", command=simulate_turn)
button_next.grid(row=8, column=0, columnspan=2, pady=5)

button_exit = tk.Button(frame, text="Exit", command=exit_simulation)
button_exit.grid(row=9, column=0, columnspan=2, pady=5)

result_text = tk.Text(window, height=10)
result_text.pack(pady=10)

window.mainloop()


