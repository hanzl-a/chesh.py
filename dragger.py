from const import *
from piece import Piece


class Dragger:
    def __init__(self) -> None:
        self.mouseX = 0
        self.mouseY = 0
        self.piece: Piece = None
        self.dragging = False
        self.initial_row = None
        self.initial_col = None

    def update_mouse(self, pos) -> None:
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos) -> None:
        self.initial_row = pos[1] // SQUARE_SIZE
        self.initial_col = pos[0] // SQUARE_SIZE

    def drag_piece(self, piece: Piece) -> None:
        self.piece = piece
        self.dragging = True

    def undrag_piece(self) -> None:
        self.piece = None
        self.dragging = False
