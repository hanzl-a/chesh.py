from piece import *
from move import Move
from typing import Union
from square import Square


class Board:
    def __init__(self) -> None:
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for x in range(8)]
        self.last_move = None

        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    def move(self, piece: Piece, move: Move) -> None:
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        piece.moved = True

        piece.clear_moves()

        self.last_move = move

    def valid_move(self, piece: Piece, move: Move) -> bool:
        return move in piece.moves

    def calc_moves(self, row: int, col: int, piece: Piece) -> None:

        if isinstance(piece, Pawn):
            self._pawn_moves(row, col, piece)

        if isinstance(piece, Knight):
            self._knight_moves(row, col, piece)

        if isinstance(piece, Bishop):
            incrs = [
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
            ]
            self._straightline_moves(row, col, piece, incrs)

        if isinstance(piece, Rook):
            incrs = [
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1),
            ]
            self._straightline_moves(row, col, piece, incrs)

        if isinstance(piece, Queen):
            incrs = [
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1),
            ]
            self._straightline_moves(row, col, piece, incrs)

        if isinstance(piece, King):
            self._king_moves(row, col, piece)

    def _pawn_moves(self, row: int, col: int, piece: Pawn) -> None:
        steps = 1 if piece.moved else 2

        # vertical moves
        start = row + piece.dir
        end = row + (piece.dir * (1 + steps))

        for pos_move_row in range(start, end, piece.dir):
            if Square.in_range(pos_move_row):
                if self.squares[pos_move_row][col].is_empty():
                    initial = Square(row, col)
                    final = Square(pos_move_row, col)
                    move = Move(initial, final)
                    piece.add_move(move)
                else:
                    break
            else:
                break

        # diagonal moves
        pos_move_row = row + piece.dir
        pos_move_cols = [col - 1, col + 1]

        for pos_move_col in pos_move_cols:
            if Square.in_range(pos_move_row, pos_move_col):
                if self.squares[pos_move_row][pos_move_col].has_enemy_piece(
                    piece.color
                ):
                    initial = Square(row, col)
                    final = Square(pos_move_row, pos_move_col)
                    move = Move(initial, final)
                    piece.add_move(move)

    def _knight_moves(self, row: int, col: int, piece: Knight) -> None:
        pos_moves = [
            (row + 2, col - 1),
            (row + 2, col + 1),
            (row - 2, col - 1),
            (row - 2, col + 1),
            (row - 1, col - 2),
            (row - 1, col + 2),
            (row + 1, col - 2),
            (row + 1, col + 2),
        ]

        for pos_move in pos_moves:
            pos_move_row, pos_move_col = pos_move

            if Square.in_range(pos_move_row, pos_move_col):
                if self.squares[pos_move_row][pos_move_col].is_empty_or_enemy(
                    piece.color
                ):
                    initial = Square(row, col)
                    final = Square(pos_move_row, pos_move_col)
                    move = Move(initial, final)
                    piece.add_move(move)

    def _straightline_moves(
        self, row: int, col: int, piece: Union[Bishop, Rook, Queen], incrs: list
    ) -> None:
        for incr in incrs:
            row_incr, col_incr = incr

            pos_move_row = row + row_incr
            pos_move_col = col + col_incr

            while True:
                if Square.in_range(pos_move_row, pos_move_col):
                    initial = Square(row, col)
                    final = Square(pos_move_row, pos_move_col)
                    move = Move(initial, final)

                    if self.squares[pos_move_row][pos_move_col].is_empty():
                        piece.add_move(move)

                    if self.squares[pos_move_row][pos_move_col].has_enemy_piece(
                        piece.color
                    ):
                        piece.add_move(move)
                        break

                    if self.squares[pos_move_row][pos_move_col].has_team_piece(
                        piece.color
                    ):
                        break

                else:
                    break

                pos_move_row += row_incr
                pos_move_col += col_incr

    def _king_moves(self, row: int, col: int, piece: King) -> None:
        adjs = [
            (row - 1, col),
            (row - 1, col + 1),
            (row, col + 1),
            (row + 1, col + 1),
            (row + 1, col),
            (row + 1, col - 1),
            (row, col - 1),
            (row - 1, col - 1),
        ]

        for pos_move in adjs:
            pos_move_row, pos_move_col = pos_move

            if Square.in_range(pos_move_row, pos_move_col):
                if self.squares[pos_move_row][pos_move_col].is_empty_or_enemy(
                    piece.color
                ):
                    initial = Square(row, col)
                    final = Square(pos_move_row, pos_move_col)
                    move = Move(initial, final)
                    piece.add_move(move)

    def _create(self) -> None:
        for row in range(8):
            for col in range(8):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color: str) -> None:
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # pawns
        for col in range(8):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 3, King(color))
