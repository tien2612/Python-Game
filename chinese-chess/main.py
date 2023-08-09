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

WAIT_FOR_CLICK = 10
MAKE_DECISION = 11
MAKE_MOVE = 12

class Player:
    def __init__(self, initial_turn):
        self.current_turn = initial_turn
        self.king_alive = True
        self.king_checkmate = False

    def is_king_alive(self):
        return self.king_alive
    
    def is_checkmate(self):
        return self.king_checkmate
    
    def switch_turn(self):
        if self.current_turn == 'red':
            self.current_turn = 'black'
        else:
            self.current_turn = 'red'

    def get_current_turn(self):
        return self.current_turn
        
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
        self.piece_grid = [[ (None, None) for _ in range(COL_SIZE + 1)] for _ in range(ROW_SIZE + 1)]  # Create the grid
        self.dotMove_grid = [[ (None, None) for _ in range(COL_SIZE + 1)] for _ in range(ROW_SIZE + 1)]  # Create the grid

        self.selected_piece = None

        self.previous_select = []

        self.dotMove_coordinate = []

        self.status = MAKE_DECISION

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
        if (piece_type == 'dotMove'):
            self.dotMove_grid[row][col] = piece_type, image_id
        else: 
            self.piece_grid[row][col] = piece_type, image_id

    def handle_square_click(self, event):
        # Calculate the row and column of the clicked cell 
        cell_width = 64
        cell_height = 64

        # Calculate the row and column of the clicked cell
        row = round((event.y - 57) / cell_height)
        col = round((event.x - 41) / cell_width)

        while (True):

            self.selected_piece, _ = self.piece_grid[row][col]
            
            if (self.selected_piece != None):
                if (app.players.get_current_turn() == 'red' and self.selected_piece[0] != 'r' and self.status != MAKE_MOVE):
                    print('no its black turn')
                    return
                elif(app.players.get_current_turn() == 'black' and self.selected_piece[0] != 'b' and self.status != MAKE_MOVE):
                    print('no its red turn')
                    return
            
            # If the king is checkmate, then only king can move or piece can protect the king
            if (app.players.is_checkmate):
                pass
            
            if self.status == MAKE_DECISION:
                print(f'Piece at {row},{col} selected')

                self.remove_dotMove(self.dotMove_coordinate)            

                self.dotMove_coordinate = self.can_move_to(self.selected_piece, row, col)
                
                self.previous_select = [self.selected_piece, {(row, col)}]

                self.status = MAKE_MOVE

                break
            elif self.status == MAKE_MOVE:
                # check and move piece
                if (row, col) in self.dotMove_coordinate:
                    print(f'Piece move to {row},{col}')
                    self.move_piece(self.previous_select[0], row, col, self.previous_select[1])
                    break
                else:
                    self.status = MAKE_DECISION
                    continue
            else:
                print("Something is wrong!")
                break

    def can_move_to(self, piece_type, row, col):
        """Display and return the coordinates that piece can move to."""
        can_move_coordinate = []
        
        if piece_type in ['bRook', 'rRook']:
            # Rooks can move any number of squares along the row or column
            # Check each direction (up, down, left, right)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                for i in range(1, max(ROW_SIZE + 1, COL_SIZE + 1)):
                    new_row, new_col = row + dr * i, col + dc * i

                    # Stop if the rook moved off the board
                    if not (0 <= new_row < ROW_SIZE + 1 and 0 <= new_col < COL_SIZE + 1):
                        break
                    # Stop if the rook hits a piece
                    piece, _ = self.piece_grid[new_row][new_col]

                    if piece is not None:  # add this check
                        if piece[0] != piece_type[0]:  # Check if the piece is not the same color
                            can_move_coordinate.append((new_row, new_col))
                            self.place_piece('dotMove', new_row, new_col)
                        break
                    else:
                        can_move_coordinate.append((new_row, new_col))
                        self.place_piece('dotMove', new_row, new_col)

        elif piece_type in ['bHorse', 'rHorse']:
            # Horses can only move L direction, jump through 2 squares
            for dr, dc in [(1, -2), (2, -1), (2, 1), (-1, 2), (-2, 1), (1, 2), (-2, -1), (-1, -2)]:
                new_row, new_col = row + dr, col + dc

                # Stop if the horse moved off the board
                if not (0 <= new_row < ROW_SIZE + 1 and 0 <= new_col < COL_SIZE + 1):
                    continue
                
                # Stop if the horse jumps over a piece
                jump_row, jump_col = row + round(dr / 2), col + round(dc / 2)
                
                if self.piece_grid[jump_row][jump_col][0] is not None:
                    continue
                
                # # If the destination square is empty or contains an enemy piece, the horse can move/attack there
                piece, _ = self.piece_grid[new_row][new_col]

                if piece is None or piece[0] != piece_type[0]:
                    can_move_coordinate.append((new_row, new_col))
                    self.place_piece('dotMove', new_row, new_col)

        elif piece_type in ['bElephant', 'rElephant']:
            # Elephant can only move X direction, jump through 2 squares
            for dr, dc in [(-2, -2), (-2, 2), (2, 2), (2, -2)]:
                new_row, new_col = row + dr, col + dc

                river_boundary = 4

                # Stop if the elephant moved off the board and cannot across the river
                if not (0 <= new_row < ROW_SIZE + 1 and 0 <= new_col < COL_SIZE + 1):
                    continue
                     
                if (piece_type[0] == 'r' and new_row > river_boundary) or \
                    (piece_type[0] == 'b' and new_row <= river_boundary):
                    continue

                # Stop if the elephant move over a piece 
                jump_row, jump_col = row + round(dr / 2), col + round(dc / 2)
                
                if self.piece_grid[jump_row][jump_col][0] is not None:
                    continue
                
                # If the destination square is empty or contains an enemy piece, the horse can move/attack there
                piece, _ = self.piece_grid[new_row][new_col]

                if piece is None or piece[0] != piece_type[0]:
                    can_move_coordinate.append((new_row, new_col))
                    self.place_piece('dotMove', new_row, new_col)

        elif piece_type in ['bAdvisor', 'rAdvisor']:
            # Advisor can only move X direction, jump through 1 squares and in its boundry
            for dr, dc in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                new_row, new_col = row + dr, col + dc

                boundaries = {
                    "col": [3, 5],
                    "row": {('black', 'red'): [(7, 9), (0, 2)]}
                }

                # Stop if the advisor moved off the board and cannot beyond its boundary
                if not (0 <= new_row < ROW_SIZE + 1 and 0 <= new_col < COL_SIZE + 1):
                    continue
                     
                black_boundary, red_boundary = boundaries["row"][('black', 'red')]

                # Check boundaries for red advisor
                if piece_type[0] == 'r':
                    if not ( (red_boundary[0] <= new_row <= red_boundary[1]) and\
                        (boundaries['col'][0] <= new_col <= boundaries['col'][1]) ):
                        continue

                # Check boundaries for black advisor
                elif piece_type[0] == 'b':
                    if not ( (black_boundary[0] <= new_row <= black_boundary[1]) and\
                        (boundaries['col'][0] <= new_col <= boundaries['col'][1]) ):
                        continue
         
                # If the destination square is empty or contains an enemy piece, the horse can move/attack there
                piece, _ = self.piece_grid[new_row][new_col]

                if piece is None or piece[0] != piece_type[0]:
                    can_move_coordinate.append((new_row, new_col))
                    self.place_piece('dotMove', new_row, new_col)

        elif piece_type in ['bKing', 'rKing']:
            # King can only move 1 direction, through 1 squares and in its boundry
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc

                boundaries = {
                    "col": [3, 5],
                    "row": {('black', 'red'): [(7, 9), (0, 2)]}
                }

                # Stop if the advisor moved off the board and cannot beyond its boundary
                if not (0 <= new_row < ROW_SIZE + 1 and 0 <= new_col < COL_SIZE + 1):
                    continue
                     
                black_boundary, red_boundary = boundaries["row"][('black', 'red')]

                # Check boundaries for red advisor
                if piece_type[0] == 'r':
                    if not ( (red_boundary[0] <= new_row <= red_boundary[1]) and\
                        (boundaries['col'][0] <= new_col <= boundaries['col'][1]) ):
                        continue

                # Check boundaries for black advisor
                elif piece_type[0] == 'b':
                    if not ( (black_boundary[0] <= new_row <= black_boundary[1]) and\
                        (boundaries['col'][0] <= new_col <= boundaries['col'][1]) ):
                        continue
         
                # If the destination square is empty or contains an enemy piece, the horse can move/attack there
                piece, _ = self.piece_grid[new_row][new_col]

                if piece is None or piece[0] != piece_type[0]:
                    can_move_coordinate.append((new_row, new_col))
                    self.place_piece('dotMove', new_row, new_col)

        elif piece_type in ['bCannon', 'rCannon']:
            # Cannon can move any number of squares along the row or column but only attack through one piece (jump over)
            # Check each direction (up, down, left, right)
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ready_to_attack = False
                for i in range(1, max(ROW_SIZE + 1, COL_SIZE + 1)):
                    new_row, new_col = row + dr * i, col + dc * i
                        
                    # Stop if the cannon moved off the board
                    if not (0 <= new_row < ROW_SIZE + 1 and 0 <= new_col < COL_SIZE + 1):
                        break

                    # Stop if the rook hits a piece
                    piece, _ = self.piece_grid[new_row][new_col]

                    if piece is None:  # add this check
                        if not ready_to_attack:
                            can_move_coordinate.append((new_row, new_col))
                            self.place_piece('dotMove', new_row, new_col)
                    else: # find the next piece after it, check if cannon can attack
                        if (ready_to_attack):
                            if (piece[0] != piece_type[0]):
                                can_move_coordinate.append((new_row, new_col))
                                self.place_piece('dotMove', new_row, new_col)
                                break
                            else:
                                break
                        else:
                            ready_to_attack = True  

        elif piece_type in ['bKing', 'rKing']:
            # King can only move 1 direction, through 1 squares and in its boundry
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc

                boundaries = {
                    "col": [3, 5],
                    "row": {('black', 'red'): [(7, 9), (0, 2)]}
                }

                # Stop if the advisor moved off the board and cannot beyond its boundary
                if not (0 <= new_row < ROW_SIZE + 1 and 0 <= new_col < COL_SIZE + 1):
                    continue
                     
                black_boundary, red_boundary = boundaries["row"][('black', 'red')]

                # Check boundaries for red advisor
                if piece_type[0] == 'r':
                    if not ( (red_boundary[0] <= new_row <= red_boundary[1]) and\
                        (boundaries['col'][0] <= new_col <= boundaries['col'][1]) ):
                        continue

                # Check boundaries for black advisor
                elif piece_type[0] == 'b':
                    if not ( (black_boundary[0] <= new_row <= black_boundary[1]) and\
                        (boundaries['col'][0] <= new_col <= boundaries['col'][1]) ):
                        continue
         
                # If the destination square is empty or contains an enemy piece, the horse can move/attack there
                piece, _ = self.piece_grid[new_row][new_col]

                if piece is None or piece[0] != piece_type[0]:
                    can_move_coordinate.append((new_row, new_col))
                    self.place_piece('dotMove', new_row, new_col)

        elif piece_type in ['bPawn', 'rPawn']:
            # Pawn can only move 1 squares along the row if it hasnt been across the river yet
            # After that, Pawn can move up or right and left, cannot move downward
            has_across_theRiver = False
            river_boundary = 4

            direction = []

            #  Check if has across the river
            if (piece_type[0] == 'r' and row > river_boundary) or \
                (piece_type[0] == 'b' and row <= river_boundary):
                has_across_theRiver = True

            if (has_across_theRiver and piece_type[0] == 'r'):
                direction = [(1, 0), (0, -1), (0, 1)]
            elif has_across_theRiver:
                    direction = [(-1, 0), (0, -1), (0, 1)]
            elif (piece_type[0] == 'r'): 
                    direction = [(1, 0)]
            else: direction = [(-1, 0)]

            for dr, dc in direction:
                new_row, new_col = row + dr, col + dc
                # Stop if the pawn moved off the board
                if not (0 <= new_row < ROW_SIZE + 1 and 0 <= new_col < COL_SIZE + 1):
                    continue
                
                # If the destination square is empty or contains an enemy piece, the horse can move/attack there
                piece, _ = self.piece_grid[new_row][new_col]

                if piece is None or piece[0] != piece_type[0]:
                    can_move_coordinate.append((new_row, new_col))
                    self.place_piece('dotMove', new_row, new_col)

        else:
            raise ValueError(f"Unknown piece type: {piece_type}")

        return can_move_coordinate

    def move_piece(self, selected_piece, row, col, old_coordinate):
        # If the piece is exist piece, then terminate this peice before place new peice
        if (self.piece_grid[row][col] != (None, None)):
            self.remove_piece({(row, col)})
        # First, place the new piece
        self.place_piece(selected_piece, row, col)
        # Then, remove the old piece
        self.remove_piece(old_coordinate)

        self.remove_dotMove(self.dotMove_coordinate)
        
        # Need to checkmate
        coordinate = self.can_move_to(selected_piece, row, col)
        
        if (coordinate in self.get_king_position()):
            app.players.is_checkmate = True

        app.players.switch_turn()

    def remove_dotMove(self, coordinate):   

        if coordinate is not None:
            for row, col in coordinate:
                _, image_id = self.dotMove_grid[row][col]
                if image_id is not None:  # Make sure you don't try to delete a non-existing image
                    self.canvas.delete(image_id)
                    self.dotMove_grid[row][col] = (None, None)
                self.dotMove_coordinate = []

    def remove_piece(self, coordinate):        
        if coordinate is not None:
            for row, col in coordinate:
                _, image_id = self.piece_grid[row][col]
                if image_id is not None:  # Make sure you don't try to delete a non-existing image
                    self.canvas.delete(image_id)
                    self.piece_grid[row][col] = (None, None)
    
    def get_king_position(self, current_turn):
        if (current_turn == 'red'):
            range_row = (0, 2)
        else: range_row = (7, 9)

        for i in range_row:
            for j in range (3, 5):
                if (self.piece_grid[i][j][0] == 'rKing' or self.piece_grid[i][j][0] == 'bKing'):
                    return (i, j)
                
        return (0, 0)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Chinese Chess Board")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
                
        board = Piece(screen_width, screen_height)

        board.init_chess_man()
        board.init_piece()

        self.players = Player('red')  # red go first
        
root = tk.Tk()
app = App(root)
root.mainloop()