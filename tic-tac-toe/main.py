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


class Player():
    def __init__(self, marker):
        self.marker = marker
        pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tic Tac Toe Game")

        self.buttons = [[None]*3 for _ in range(3)]
        self.players = [Player('X'), Player('O')]
        self.position_taken = [[None]*3 for _ in range(3)]
        self.number_of_turn = 0

        imgX = Image.open("images/x.png")
        imgX = imgX.resize((90, 90), Image.LANCZOS)

        imgO = Image.open("images/o.png")
        imgO = imgO.resize((90, 90), Image.LANCZOS)
        self.images = [ImageTk.PhotoImage(imgX), ImageTk.PhotoImage(imgO)]   # Load the image
        
        self.placeholderImage = ImageTk.PhotoImage(Image.open("images/placeholder.png").resize((90, 90), Image.LANCZOS))  # Load the placeholder image

        self.current_turn = random.randint(0, 1)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tkinter.Button(self, image=self.placeholderImage, command=lambda i=i, j=j: self.handle_user_select(i, j))
                self.buttons[i][j].grid(row=i, column=j, sticky="snew")

    def handle_user_select(self, col, row):
        self.number_of_turn += 1

        self.position_taken[col][row] = self.players[self.current_turn].marker
        self.buttons[col][row].config(image=self.images[self.current_turn])

        if self.win_check('X'):
            return
        
        if self.win_check('O'):
            return
        
        if (self.number_of_turn >=9):
            is_retry = messagebox.askretrycancel("Game Over", f"Draw!")
            if (is_retry): self.restart_game()

        self.switch_turn()

    def switch_turn(self):
        if (self.current_turn == 0):
            self.current_turn = 1
        else:
            self.current_turn = 0
    
    def restart_game(self):
        self.position_taken = [[None]*3 for _ in range(3)]
        self.number_of_turn = 0

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(image=self.placeholderImage, command=lambda i=i, j=j: self.handle_user_select(i, j))

        return
    
    def win_check(self, player):
        # Check rows
        for i in range(3):
            if self.position_taken[i][0] == self.position_taken[i][1] == self.position_taken[i][2] == player:
                is_retry = messagebox.askretrycancel("Game Over", f"Player {player} wins!")

                if (is_retry): self.restart_game()

        # Check columns
        for i in range(3):
            if self.position_taken[0][i] == self.position_taken[1][i] == self.position_taken[2][i] == player:
                is_retry = messagebox.askretrycancel("Game Over", f"Player {player} wins!")

                if (is_retry): self.restart_game()

        # Check diagonals
        if self.position_taken[0][0] == self.position_taken[1][1] == self.position_taken[2][2] == player or self.position_taken[0][2] == self.position_taken[1][1] == self.position_taken[2][0] == player:
                is_retry = messagebox.askretrycancel("Game Over", f"Player {player} wins!")

                if (is_retry): self.restart_game()

        return False

if __name__ == "__main__":
    app = App()
    app.mainloop()