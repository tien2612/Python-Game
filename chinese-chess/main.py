import tkinter as tk
import random
from tkinter import *
from time import sleep
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import Toplevel, messagebox
import customtkinter as ctk

ROW_SIZE = 9  # Replace with the number of rows in your board image
COL_SIZE = 8  # Replace with the number of columns in your board image

class Piece:
    def __init__(self, screen_width, screen_height):
        # Load the board image
        board = Image.open("images/ziga/board.png")
        # Get image original size
        img_width, img_height = board.size

        # Compare the aspect ratio of screen and image
        screen_ratio = screen_width / screen_height
        img_ratio = img_width / img_height

        if img_ratio > screen_ratio:
            # Image aspect ratio is wider than screen's. Match image width to screen width.
            width = int(screen_width * 0.9) # 90% of screen width
            height = int(width / img_ratio)
        else:
            # Image aspect ratio is taller than screen's. Match image height to screen height.
            height = int(screen_height * 0.9) # 90% of screen height
            width = int(height * img_ratio)

        # Resize the board image
        board = board.resize((width, height), Image.LANCZOS)
        self.board_image = ImageTk.PhotoImage(board)

        # Create a Canvas to hold the image
        self.canvas = tk.Canvas(root, width=self.board_image.width(), height=self.board_image.height())
        self.canvas.pack()

        # Place the board image on the canvas
        self.canvas.create_image(0, 0, image=self.board_image, anchor='nw')

        # Bind the <Button-1> event to the canvas
        self.piece_grid = [[None for _ in range(COL_SIZE + 1)] for _ in range(ROW_SIZE + 1)]  # Create the grid

        self.selected_piece = None

        self.previous_select = []
        self.canvas.bind("<Button-1>", self.handle_square_click)

    def init_chess_man(self):
        # rook image
        img_rRook = Image.open("images/red/Rook-Red.png")
        img_rRook = img_rRook.resize((50, 50), Image.LANCZOS)
        img_bRook = Image.open("images/black/Rook-Black.png")
        img_bRook = img_bRook.resize((50, 50), Image.LANCZOS)

        # horse image
        img_rHorse = Image.open("images/red/Horse-Red.png")
        img_rHorse = img_rHorse.resize((50, 50), Image.LANCZOS)
        img_bHorse = Image.open("images/black/Horse-Black.png")
        img_bHorse = img_bHorse.resize((50, 50), Image.LANCZOS)

        img_rElephant = Image.open("images/red/Elephant-Red.png")
        img_rElephant = img_rElephant.resize((50, 50), Image.LANCZOS)
        img_bElephant = Image.open("images/black/Elephant-Black.png")
        img_bElephant = img_bElephant.resize((50, 50), Image.LANCZOS)

        img_rAdvisor = Image.open("images/red/Advisor-Red.png")
        img_rAdvisor = img_rAdvisor.resize((50, 50), Image.LANCZOS)
        img_bAdvisor = Image.open("images/black/Advisor-Black.png")
        img_bAdvisor = img_bAdvisor.resize((50, 50), Image.LANCZOS)

        img_rKing = Image.open("images/red/King-Red.png")
        img_rKing = img_rKing.resize((50, 50), Image.LANCZOS)
        img_bKing = Image.open("images/black/King-Black.png")
        img_bKing = img_bKing.resize((50, 50), Image.LANCZOS)

        img_rCannon = Image.open("images/red/Cannon-Red.png")
        img_rCannon = img_rCannon.resize((50, 50), Image.LANCZOS)
        img_bCannon = Image.open("images/black/Cannon-Black.png")
        img_bCannon = img_bCannon.resize((50, 50), Image.LANCZOS)
        
        img_rPawn = Image.open("images/red/Pawn-Red.png")
        img_rPawn = img_rPawn.resize((50, 50), Image.LANCZOS)
        img_bPawn = Image.open("images/black/Pawn-Black.png")
        img_bPawn = img_bPawn.resize((50, 50), Image.LANCZOS)

        img_oos = Image.open("images/ziga/oos.png")
        img_oos = img_oos.resize((50, 50), Image.LANCZOS)
        img_dotMove = Image.open("images/ziga/dotmove.png")
        img_dotMove = img_dotMove.resize((25, 25), Image.LANCZOS)

        self.image_map = {
            'rRook': ImageTk.PhotoImage(img_rRook),
            'rHorse': ImageTk.PhotoImage(img_rHorse),
            'rElephant': ImageTk.PhotoImage(img_rElephant),
            'rAdvisor': ImageTk.PhotoImage(img_rAdvisor),
            'rKing': ImageTk.PhotoImage(img_rKing),
            'bRook': ImageTk.PhotoImage(img_bRook),
            'bHorse': ImageTk.PhotoImage(img_bHorse),
            'bElephant': ImageTk.PhotoImage(img_bElephant),
            'bAdvisor': ImageTk.PhotoImage(img_bAdvisor),
            'bKing': ImageTk.PhotoImage(img_bKing),
            'rCannon': ImageTk.PhotoImage(img_rCannon),
            'bCannon': ImageTk.PhotoImage(img_bCannon),
            'rPawn': ImageTk.PhotoImage(img_rPawn),
            'bPawn': ImageTk.PhotoImage(img_bPawn),
            'dotMove': ImageTk.PhotoImage(img_dotMove),
            'oos': ImageTk.PhotoImage(img_oos)
        }

    def init_piece(self):
        # Rook
        self.place_piece('rRook', 0, 0)
        self.place_piece('rRook', 0, 8)
        self.place_piece('bRook', 9, 8)
        self.place_piece('bRook', 9, 0)

        # Horse
        self.place_piece('rHorse', 0, 1)
        self.place_piece('rHorse', 0, 7)
        self.place_piece('bHorse', 9, 7)
        self.place_piece('bHorse', 9, 1)

        # Elephant
        self.place_piece('rElephant', 0, 2)
        self.place_piece('rElephant', 0, 6)
        self.place_piece('bElephant', 9, 6)
        self.place_piece('bElephant', 9, 2)

        # Advisor
        self.place_piece('rAdvisor', 0, 3)
        self.place_piece('rAdvisor', 0, 5)
        self.place_piece('bAdvisor', 9, 5)
        self.place_piece('bAdvisor', 9, 3)

        # king
        self.place_piece('rKing', 0, 4)
        self.place_piece('bKing', 9, 4)

        # Cannon
        self.place_piece('rCannon', 2, 1)
        self.place_piece('rCannon', 2, 7)
        self.place_piece('bCannon', 7, 1)
        self.place_piece('bCannon', 7, 7)

        # # Pawn
        self.place_piece('bPawn', 6, 0)
        self.place_piece('bPawn', 6, 2)
        self.place_piece('bPawn', 6, 4)
        self.place_piece('bPawn', 6, 6)
        self.place_piece('bPawn', 6, 8)

        self.place_piece('rPawn', 3, 0)
        self.place_piece('rPawn', 3, 2)
        self.place_piece('rPawn', 3, 4)
        self.place_piece('rPawn', 3, 6)
        self.place_piece('rPawn', 3, 8)

    def place_piece(self, piece_type, row, col):
        cell_width = 64
        cell_height = 64

        x = col * cell_width + 41
        y = row * cell_height + 57
        image_id = self.canvas.create_image(x, y, image=self.image_map[piece_type], anchor='center')

        # Store the type of piece in the grid
        self.piece_grid[row][col] = piece_type, image_id

    def make_move(self, piece_type, col, row):
        move = None
        return move
    
    def handle_square_click(self, event):
        # Calculate the row and column of the clicked cell 
        cell_width = 64
        cell_height = 64

        # Calculate the row and column of the clicked cell
        row = round((event.y - 57) / cell_height)
        col = round((event.x - 41) / cell_width)

        self.selected_piece, imageId = self.piece_grid[row][col]
        self.dotMove_coordinate = []
        if self.selected_piece is None:
            # If no piece is selected, try to select the piece at this square

            if self.selected_piece is None:
                print("No piece at this position")
            else:
                print(f'Piece at {row},{col} is {self.selected_piece}')
                self.dotMove_coordinate = self.can_move_to(self.selected_piece, row, col)
                self.selected_piece = None  # Reset selected piece

        elif(self.selected_piece != None):
            self.dotMove_coordinate = self.can_move_to(self.selected_piece, row, col)
        else:
            # If a piece is selected, try to move it to this square
            if self.move_piece(self.selected_piece, row, col):
                print(f'Piece moved to {row},{col}')
            # self.remove_piece(coordinate)
            self.selected_piece = None  # Reset selected piece

    def can_move_to(self, piece_type, row, col):
        """Display and return the coordinates that piece can move to."""
        can_move_coordinate = []
        
        if piece_type == 'bRook' or piece_type == 'rRook':
            # Rooks can move any number of squares along the row or column
            # Check each direction (up, down, left, right)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                for i in range(1, max(ROW_SIZE + 1, COL_SIZE + 1)):
                    new_row, new_col = row + dr * i, col + dc * i
                    # Stop if the rook moved off the board
                    if not (0 <= new_row < ROW_SIZE + 1 and 0 <= new_col < COL_SIZE + 1):
                        break
                    # Stop if the rook hits a piece
                    if self.piece_grid[new_row][new_col] is not None:
                        break
                    can_move_coordinate.append((new_row, new_col))
                    self.place_piece('dotMove', new_row, new_col)
        # Handle other piece types here
        else:
            raise ValueError(f"Unknown piece type: {piece_type}")

        return can_move_coordinate

    def move_piece(self, selected_piece, row, col, old_coordinate):
        self.place_piece(selected_piece, row, col)

        self.remove_piece(selected_piece, old_coordinate)
        self.remove_piece(selected_piece, self.dotMove_coordinate)
    
    def remove_piece(self, coordinate):
        for row, col in coordinate:
            piece_type, image_id = self.piece_grid[row][col]

            self.canvas.delete(image_id)
            self.piece_grid[row][col] = None, None
            self.dotMove_coordinate = None
            pass

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Chinese Chess Board")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
                
        board = Piece(screen_width, screen_height)

        board.init_chess_man()
        board.init_piece()
        
root = tk.Tk()
app = App(root)
root.mainloop()