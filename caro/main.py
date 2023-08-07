import json
import random
from tkinter import *
from time import sleep
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import Toplevel, messagebox
import customtkinter as ctk
import tkinter

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

COL_SIZE = 15
ROW_SIZE = 15
CONDITION_WIN = 5
MAX_STEP_CHECK = 4

class Player():
    def __init__(self, marker):
        self.marker = marker

class Board():
    def __init__(self):
        pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Caro Game")
        
        # image
        self.menu_image = ImageTk.PhotoImage(Image.open("images/background.png"))  # Change to your image file path
        image_label = tkinter.Label(self, image=self.menu_image)
        image_label.pack()  # You can adjust the placement with pack or grid as needed

        # button for menu
        play_wbot_button = tkinter.Button(self, text="Play Offline", command=self.handle_offline_button)
        play_versus_button = tkinter.Button(self, text="Play vs Friend", command=self.handle_versus_button)

        play_wbot_button.pack(pady=10)  # Use pack for simplicity
        play_versus_button.pack(pady=10)

    def handle_versus_button(self):
        self.setup_game()  # Call the game setup function

    def handle_offline_button(self):
        self.setup_game()  # Call the game setup function

    def setup_game(self):
        # Remove menu buttons
        for widget in self.winfo_children():
            widget.destroy()

        # Here, place the rest of the game setup code
        self.buttons = [[None]*ROW_SIZE for _ in range(COL_SIZE)]
        self.players = [Player('X'), Player('O')]
        self.position_taken = [[None]*ROW_SIZE for _ in range(COL_SIZE)]
        self.number_of_turn = 0
        self.player_number_count = 1

        imgX = Image.open("images/x.png")
        imgX = imgX.resize((35, 35), Image.LANCZOS)

        imgO = Image.open("images/o.png")
        imgO = imgO.resize((35, 35), Image.LANCZOS)
        self.images = [ImageTk.PhotoImage(imgX), ImageTk.PhotoImage(imgO)]   # Load the image

        self.placeholderImage = ImageTk.PhotoImage(Image.open("images/placeholder.png").resize((35, 35), Image.LANCZOS))  # Load the placeholder image

        self.current_turn = random.randint(0, 1)
        for i in range(ROW_SIZE):
            for j in range(COL_SIZE):
                self.buttons[i][j] = tkinter.Button(self, image=self.placeholderImage, command=lambda i=i, j=j: self.handle_user_select(i, j))
                self.buttons[i][j].grid(row=i, column=j, sticky="snew")

    def handle_user_select(self, row, col):
        if (self.position_taken[row][col] != None): return
        
        self.number_of_turn += 1

        self.position_taken[row][col] = self.players[self.current_turn].marker
        self.buttons[row][col].config(image=self.images[self.current_turn])

        if self.current_turn == 0:
            self.win_check('X', row, col)
        
        else:
            self.win_check('O', row, col)
        
        if (self.number_of_turn >= COL_SIZE*ROW_SIZE):
            is_retry = messagebox.askretrycancel("Game Over", f"Draw!")
            if (is_retry): self.restart_game()

        self.switch_turn()

    def switch_turn(self):
        if (self.current_turn == 0):
            self.current_turn = 1
        else:
            self.current_turn = 0
    
    def restart_game(self):
        self.position_taken = [[None]*ROW_SIZE for _ in range(COL_SIZE)]
        self.number_of_turn = 0
        self.player_number_count = 1

        for i in range(ROW_SIZE):
            for j in range(COL_SIZE):
                self.buttons[i][j].config(image=self.placeholderImage, command=lambda i=i, j=j: self.handle_user_select(i, j))

        return
    
    def win_condition_check(self, player):
        if (self.player_number_count == CONDITION_WIN): 
                is_retry = messagebox.askretrycancel("Game Over", f"Player {player} wins!")
                if (is_retry): self.restart_game()     

        self.player_number_count = 1
        
    def win_check(self, player, row, col):
        # col ++, row (tail)
        for i in range(col, min(col + MAX_STEP_CHECK, COL_SIZE)):
            if (i != COL_SIZE - 1):
                if (self.position_taken[row][i] == self.position_taken[row][i + 1]):
                    self.player_number_count += 1
                else: break
            else: break

        # col --, row (tail) ===> merge
        for i in range(col, max(0, col - MAX_STEP_CHECK) - 1, -1):
            if (self.position_taken[row][i] == self.position_taken[row][i - 1]):
                self.player_number_count += 1
            else: break

        self.win_condition_check(player)

        # row ++, col (tail)
        for i in range(row, min(row + MAX_STEP_CHECK, ROW_SIZE)):
            if (i != COL_SIZE - 1):
                if (self.position_taken[i][col] == self.position_taken[i + 1][col]):
                    self.player_number_count += 1
                else: break
            else: break


        # row --, col (tail) ===> merge
        for i in range(row, max(0, row - MAX_STEP_CHECK) - 1, -1):
            if (self.position_taken[i][col] == self.position_taken[i - 1][col]):
                self.player_number_count += 1
            else: break

        self.win_condition_check(player)

        # col ++, row-- (tail)
        for i, j in zip(range(row, max(0, row - MAX_STEP_CHECK) - 1, -1),
                        range(col, min(col + MAX_STEP_CHECK, COL_SIZE))):
            if (j != COL_SIZE - 1):
                if (self.position_taken[i][j] == self.position_taken[i - 1][j + 1]):
                    self.player_number_count += 1
                else: break
            else: break

        # col --, row++ (tail) ===> merge
        for i, j in zip(range(row, min(row + MAX_STEP_CHECK, COL_SIZE)),
                        range(col, max(0, col - MAX_STEP_CHECK) - 1, -1)):

            if (i != COL_SIZE - 1):
                if (self.position_taken[i][j] == self.position_taken[i + 1][j - 1]):
                    self.player_number_count += 1
                else: break
            else: break

        self.win_condition_check(player)

        # row ++, col++ (tail)
        for i, j in zip(range(row, min(row + MAX_STEP_CHECK, COL_SIZE)),
                        range(col, min(col + MAX_STEP_CHECK, COL_SIZE))):

            if (i != COL_SIZE - 1 and j != ROW_SIZE - 1):
                if (self.position_taken[i][j] == self.position_taken[i + 1][j + 1]):
                    self.player_number_count += 1
                else: break
            else: break

        # row --, col-- (tail) ===> merge
        for i, j in zip(range(col, max(0, col - MAX_STEP_CHECK) - 1, -1),
                        range(row, max(0, row - MAX_STEP_CHECK) - 1, -1)):
            
            if (self.position_taken[j][i] == self.position_taken[j - 1][i - 1]):
                self.player_number_count += 1
            else: break

        self.win_condition_check(player)

        return False

if __name__ == "__main__":
    app = App()
    app.mainloop()