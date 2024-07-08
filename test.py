from tkinter import *
import random

player_names = {'X': '', 'O': ''}

players = ['X', 'O']
player = random.choice(players)
game_mode = None 

points = {'X': 0, 'O': 0}

game_btns = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]

def next_turn(row, col):
    global player
    if game_btns[row][col]['text'] == "" and check_winner() == False:
        game_btns[row][col]['text'] = player

        if check_winner() == False:
            player = players[1] if player == players[0] else players[0]
            label.config(text=(player_names[player] + " turn"))
            if game_mode == 'robot' and player == 'O':
                window.after(500, robot_move) 
        elif check_winner() == True:
            label.config(text=(player_names[player] + " wins!"))
            points[player] += 1
            update_points()
        elif check_winner() == 'tie':
            label.config(text=("Tie, No Winner!"))

def check_winner():
    for row in range(3):
        if game_btns[row][0]['text'] == game_btns[row][1]['text'] == game_btns[row][2]['text'] != "":
            game_btns[row][0].config(bg='green', fg='red')
            game_btns[row][1].config(bg='green', fg='red')
            game_btns[row][2].config(bg='green', fg='red')
            return True

    for col in range(3):
        if game_btns[0][col]['text'] == game_btns[1][col]['text'] == game_btns[2][col]['text'] != "":
            game_btns[0][col].config(bg='green', fg='red')
            game_btns[1][col].config(bg='green', fg='red')
            game_btns[2][col].config(bg='green', fg='red')
            return True

    if game_btns[0][0]['text'] == game_btns[1][1]['text'] == game_btns[2][2]['text'] != '':
        game_btns[0][0].config(bg='green', fg='red')
        game_btns[1][1].config(bg='green', fg='red')
        game_btns[2][2].config(bg='green', fg='red')
        return True

    if game_btns[0][2]['text'] == game_btns[1][1]['text'] == game_btns[2][0]['text'] != '':
        game_btns[0][2].config(bg='green', fg='red')
        game_btns[1][1].config(bg='green', fg='red')
        game_btns[2][0].config(bg='green', fg='red')
        return True

    if check_empty_spaces() == False:
        for row in range(3):
            for col in range(3):
                game_btns[row][col].config(bg='yellow')
        return 'tie'
    else:
        return False

def check_empty_spaces():
    for row in range(3):
        for col in range(3):
            if game_btns[row][col]['text'] == "":
                return True
    return False

def start_new_game():
    global player
    player = random.choice(players)
    label.config(text=(player_names[player] + " turn"))

    for row in range(3):
        for col in range(3):
            game_btns[row][col].config(text='', bg='white',
                                        fg='black', state='normal')
    if game_mode == 'robot' and player == 'O':
        window.after(500, robot_move)  

def update_points():
    points_label.config(text=f"| {player_names['X']}: {points['X']} | {player_names['O']}: {points['O']} |")

def robot_move():
    empty_spaces = [(row, col) for row in range(3) for col in range(3) if game_btns[row][col]['text'] == ""]
    if empty_spaces:
        row, col = random.choice(empty_spaces)
        next_turn(row, col)

def get_player_names():
    def submit_names():
        player_names['X'] = entry_x.get()
        player_names['O'] = entry_o.get() if game_mode == 'friend' else 'Robot'
        label.config(text=(player_names[player] + " turn"))
        name_frame.pack_forget()
        game_frame.pack()
        start_new_game()

    name_frame.pack_forget()
    name_frame.pack(side='top', fill='both', expand=True)
    Label(name_frame, text="Enter name for Player X:", font=('consolas', 15), bg='lightgrey').grid(row=0, column=0, padx=10, pady=10)
    entry_x = Entry(name_frame, font=('consolas', 15))
    entry_x.grid(row=0, column=1, padx=10, pady=10)

    Label(name_frame, text="Enter name for Player O:" if game_mode == 'friend' else "Player O is Robot", font=('consolas', 15), bg='lightgrey').grid(row=1, column=0, padx=10, pady=10)
    entry_o = Entry(name_frame, font=('consolas', 15), state=NORMAL if game_mode == 'friend' else DISABLED)
    entry_o.grid(row=1, column=1, padx=10, pady=10)

    submit_btn = Button(name_frame, text="Submit", font=('consolas', 15), command=submit_names, bg='blue', fg='white', activebackground='lightblue', activeforeground='black')
    submit_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

def choose_game_mode():
    def set_mode(mode):
        global game_mode
        game_mode = mode
        mode_frame.pack_forget()
        get_player_names()

    mode_frame.pack(side='top', fill='both', expand=True)
    Label(mode_frame, text="Choose Game Mode:", font=('consolas', 20), bg='lightgrey').pack(pady=20)

    friend_btn = Button(mode_frame, text="Play with Friend", font=('consolas', 20), command=lambda: set_mode('friend'), bg='green', fg='white', activebackground='lightgreen', activeforeground='black')
    friend_btn.pack(pady=10)

    robot_btn = Button(mode_frame, text="Play with  Robot", font=('consolas', 20), command=lambda: set_mode('robot'), bg='orange', fg='white', activebackground='yellow', activeforeground='black')
    robot_btn.pack(pady=10)

    exit_btn = Button(mode_frame, text='Exit', font=('consolas', 20), command=window.quit,
                    bg='red', fg='white', activebackground='lightcoral', activeforeground='black')
    exit_btn.pack(pady=10)

window = Tk()
window.title('Tic Tac Toe')

mode_frame = Frame(window, bg='lightgrey')
name_frame = Frame(window, bg='lightgrey')
game_frame = Frame(window)

label = Label(game_frame, text='', font=('consolas', 40))
label.pack(side='top')

points_label = Label(game_frame, text=f"| {player_names['X']}: 0 | {player_names['O']}: 0 |", font=('consolas', 20))
points_label.pack(side='top')

btn_frame = Frame(game_frame)
btn_frame.pack()

for row in range(3):
    for col in range(3):
        game_btns[row][col] = Button(btn_frame, text='', bg="white", font=('consolas', 50), width=4, height=1,
                                    command=lambda row=row, col=col: next_turn(row, col))
        game_btns[row][col].grid(row=row, column=col)

bottom_frame = Frame(game_frame)
bottom_frame.pack(side='bottom', pady=10)

restart_btn = Button(bottom_frame, text='Restart', font=('consolas', 20), command=lambda: [start_new_game(), update_points()],
                    bg='blue', fg='white', activebackground='lightblue', activeforeground='black')
restart_btn.grid(row=0, column=0, padx=10)

exit_btn = Button(bottom_frame, text='Exit', font=('consolas', 20), command=window.quit,
                bg='red', fg='white', activebackground='lightcoral', activeforeground='black')
exit_btn.grid(row=0, column=1, padx=10)

window.after(500, choose_game_mode)  

window.mainloop()
