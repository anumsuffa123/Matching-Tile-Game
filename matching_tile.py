import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Matching Tiles")

emojis = ['🍇', '🍉', '🍒', '🍋', '🥭', '🍊', '🥝', '🍐']

rows = 4
columns = 4
cards = []
card_buttons = []
selected = []
moves = 0
matches = 0
time_left = 30
game_started = False
game_won= False
player_name = ""

# Create widgets
frame = tk.Frame(root)
frame.pack()

def setup_game():
    global cards, selected, moves, matches, time_left
    selected = []
    moves = 0
    matches = 0
    time_left = 30
    
    emojis = ['🍇', '🍉', '🍒', '🍋', '🥭', '🍊', '🥝', '🍐']
    cards = []
    for emoji in emojis:
        cards.append(emoji)
        cards.append(emoji)  # Add a pair for each emoji
    random.shuffle(cards)  # Shuffle cards
setup_game()  # Call setup_game before creating buttons

def update_score():
    score_label.config(text=f"Moves: {moves} | Matches: {matches} | Time: {time_left}")

def flip(row, col):
    global selected, moves, matches
    if time_left <= 0:
        return
    index = row * columns + col
    if index in selected or len(selected) >= 2:
        return

    card_buttons[index].config(text=cards[index], font=("Helvetica", 20))
    selected.append(index)

    if len(selected) == 2:
        idx1, idx2 = selected
        moves += 1
        update_score()
        root.update()  # Ensure GUI updates instantly

        if cards[idx1] == cards[idx2]:
            matches += 1
            card_buttons[idx1].config(state=tk.DISABLED)  # Disable matched cards
            card_buttons[idx2].config(state=tk.DISABLED)
            selected = []  # Reset selected cards
            if matches == 8:
                messagebox.showinfo("Matching Tiles", "Congratulations! You Win")
                game_won= True
        else:
            root.after(1000, lambda idx1=idx1, idx2=idx2: unflip(idx1, idx2))

def unflip(idx1, idx2):
    global selected
    if card_buttons[idx1]['state'] != tk.DISABLED and card_buttons[idx2]['state'] != tk.DISABLED:
        card_buttons[idx1].config(text="", font=("Helvetica", 20))
        card_buttons[idx2].config(text="", font=("Helvetica", 20))
    selected.clear()  # Reset selected cards

def start_game(event):
    global game_started, player_name
    player_name = name_entry.get()
    if player_name == "":
        messagebox.showinfo("Error", "Please enter your name!")
        return
    start_label.pack_forget()
    name_entry.pack_forget()
    countdown()
    game_started = True


def countdown():
    global time_left
    if time_left > 0:
        time_left -= 1
        update_score()
        root.after(1000, countdown)
    else:
        messagebox.showinfo("Game Over", f"Time's up! You made {moves} moves and found {matches} matches, {player_name}!")
        with open("high_score.txt", "r+") as f:
            try:
                high_score_data = f.read().splitlines()
                high_score_moves = int(high_score_data[0].split(": ")[1])
                high_score_matches = int(high_score_data[1].split(": ")[1])
                high_score_player = high_score_data[2].split(": ")[1]
            except (ValueError, IndexError):
                high_score_moves = 0
                high_score_matches = 0
                high_score_player = ""

            if matches > high_score_matches or high_score_matches == 0:
              if moves < high_score_moves or high_score_moves == 0:
                f.seek(0)
                f.write(f"Player: {player_name}\n")
                f.write(f"Moves: {moves}\n")
                f.write(f"Matches: {matches}\n")
                f.truncate()
def show_start_message():
    messagebox.showinfo("Wait!", "Please press Enter to start the game first!")

score_label = tk.Label(root, text="Moves: 0 | Matches: 0 | Time: 30", font=("times", 16))
score_label.pack(pady=10)

start_label = tk.Label(root, text="Enter your name and press Enter to start the game...", font=("times", 16))
start_label.pack(pady=10)

name_entry = tk.Entry(root, font=("times", 16))
name_entry.pack(pady=10)

for i in range(rows):
    for j in range(columns):
        button = tk.Button(frame, text="", width=5, height=3, font=("Helvetica", 20), command=lambda row=i, col=j: flip(row, col) if game_started else show_start_message())
        button.grid(row=i, column=j, padx=5, pady=5)
        card_buttons.append(button)

root.bind("<Return>", lambda event: start_game(event))
frame.configure(bg='#F49DA2')  # Change the background color of the frame to green
root.configure(bg='#F49DA2')# Change the background color to purple

root.mainloop()
