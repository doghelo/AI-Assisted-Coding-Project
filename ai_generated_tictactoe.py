import tkinter as tk

# Initialize the Tkinter window
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("500x600")

# Game variables
current_player = "X"
player_x_wins = 0
player_o_wins = 0
board_state = [[None for _ in range(3)] for _ in range(3)]  # 3x3 matrix to track moves
buttons = [[None for _ in range(3)] for _ in range(3)]      # 3x3 grid for buttons
move_count = 0  # Track the number of moves to identify a draw

# Function to update the display for the current player
def update_turn_indicator():
    if current_player == "X":
        player_x_icon.config(bg="lightgreen")
        player_o_icon.config(bg="white")
    else:
        player_x_icon.config(bg="white")
        player_o_icon.config(bg="lightgreen")

# Function to check if there is a winner or a draw
def check_winner():
    global player_x_wins, player_o_wins, move_count
    # Check for horizontal, vertical, and diagonal wins
    for row in range(3):
        if board_state[row][0] == board_state[row][1] == board_state[row][2] and board_state[row][0] is not None:
            highlight_winning_buttons([(row, 0), (row, 1), (row, 2)])
            return board_state[row][0]

    for col in range(3):
        if board_state[0][col] == board_state[1][col] == board_state[2][col] and board_state[0][col] is not None:
            highlight_winning_buttons([(0, col), (1, col), (2, col)])
            return board_state[0][col]

    if board_state[0][0] == board_state[1][1] == board_state[2][2] and board_state[0][0] is not None:
        highlight_winning_buttons([(0, 0), (1, 1), (2, 2)])
        return board_state[0][0]

    if board_state[0][2] == board_state[1][1] == board_state[2][0] and board_state[0][2] is not None:
        highlight_winning_buttons([(0, 2), (1, 1), (2, 0)])
        return board_state[0][2]

    # Check for a draw
    if move_count == 9:
        return "Draw"

    return None

# Highlight the winning buttons
def highlight_winning_buttons(winning_buttons):
    for row, col in winning_buttons:
        buttons[row][col].config(fg="green")  # Make winning buttons non-interactive
    disable_non_winning_buttons(winning_buttons)

# Disable all non-winning buttons
def disable_non_winning_buttons(winning_buttons):
    for row in range(3):
        for col in range(3):
            if (row, col) not in winning_buttons:
                buttons[row][col].config(state="disabled")  # Disable non-winning buttons
            else:
                buttons[row][col].config(state="normal")  # Keep winning buttons active but highlighted

# Function to handle button clicks
def button_click(row, col):
    global current_player, move_count, player_x_wins, player_o_wins  # Declare global variables
    
    if board_state[row][col] is None:
        buttons[row][col].config(text=current_player, disabledforeground="white", state="disabled")
        board_state[row][col] = current_player
        move_count += 1
        
        # Check for a winner or draw after the move
        result = check_winner()
        if result == "X" or result == "O":
            game_status_label.config(text=f"Player {result} wins!")
            if result == "X":
                player_x_wins += 1
                player_x_wins_label.config(text=f"Wins: {player_x_wins}")
            else:
                player_o_wins += 1
                player_o_wins_label.config(text=f"Wins: {player_o_wins}")
        elif result == "Draw":
            game_status_label.config(text="It's a draw!")
            disable_buttons()  # Disable buttons on draw
        else:
            # Alternate player turn if no winner or draw
            current_player = "O" if current_player == "X" else "X"
            update_turn_indicator()

# Function to disable the board after the game ends
def disable_buttons():
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(state="disabled")

# Function to reset the game board while keeping the win counts
def reset_board():
    global board_state, current_player, move_count
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="", state="normal", bg="white")
    board_state = [[None for _ in range(3)] for _ in range(3)]
    current_player = "X"
    move_count = 0
    game_status_label.config(text="")
    update_turn_indicator()

# Function to reset both the game board and the win counters
def reset_scores():
    global player_x_wins, player_o_wins
    reset_board()
    player_x_wins = 0
    player_o_wins = 0
    player_x_wins_label.config(text=f"Wins: {player_x_wins}")
    player_o_wins_label.config(text=f"Wins: {player_o_wins}")

# Left section: Player X turn indicator and win count
left_frame = tk.Frame(root, width=100, height=300)
left_frame.grid(row=0, column=0, padx=10, pady=10)

player_x_icon = tk.Label(left_frame, text="X", font=("Arial", 40), width=2, height=1, bg="lightgreen")
player_x_icon.pack(pady=10)

player_x_wins_label = tk.Label(left_frame, text=f"Wins: {player_x_wins}", font=("Arial", 14))
player_x_wins_label.pack()

# Right section: Player O turn indicator and win count
right_frame = tk.Frame(root, width=100, height=300)
right_frame.grid(row=0, column=2, padx=10, pady=10)

player_o_icon = tk.Label(right_frame, text="O", font=("Arial", 40), width=2, height=1, bg="white")
player_o_icon.pack(pady=10)

player_o_wins_label = tk.Label(right_frame, text=f"Wins: {player_o_wins}", font=("Arial", 14))
player_o_wins_label.pack()

# Middle section: 3x3 game board
board_frame = tk.Frame(root, width=300, height=300)
board_frame.grid(row=0, column=1, padx=10, pady=10)

# Create a 3x3 grid of buttons for the Tic-Tac-Toe board
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(board_frame, text="", font=("Arial", 40), width=5, height=2,
                                      command=lambda r=row, c=col: button_click(r, c))
        buttons[row][col].grid(row=row, column=col)

# Bottom section: Game status label, "Next Round" button, and "Reset Scores" button
bottom_frame = tk.Frame(root)
bottom_frame.grid(row=1, column=0, columnspan=3, pady=20)

game_status_label = tk.Label(bottom_frame, text="", font=("Arial", 20))
game_status_label.pack(pady=10)

next_round_button = tk.Button(bottom_frame, text="Next Round", font=("Arial", 14), command=reset_board)
next_round_button.pack()

reset_scores_button = tk.Button(bottom_frame, text="Reset Scores", font=("Arial", 14), command=reset_scores)
reset_scores_button.pack()

# Initialize the turn indicator to show Player X's turn
update_turn_indicator()

# Start the Tkinter event loop
root.mainloop()
