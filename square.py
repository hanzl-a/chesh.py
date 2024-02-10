from typing import Union


class Square:
    def __init__(self, row: int, col: int, piece=None) -> None:
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, __value: object) -> bool:
        return self.row == __value.row and self.col == __value.col

    def has_piece(self) -> bool:
        return self.piece != None

    def is_empty(self) -> bool:
        return not self.has_piece()

    def has_enemy_piece(self, color: str) -> bool:
        return self.has_piece() and self.piece.color != color

    def has_team_piece(self, color: str) -> bool:
        return self.has_piece() and self.piece.color == color

    def is_empty_or_enemy(self, color: str) -> bool:
        return self.is_empty() or self.has_enemy_piece(color)

    def get_notation(self) -> Union[str, None]:
        if self.has_piece():
            return self.piece.notation + self.get_coordinates(self.row, self.col)

    @staticmethod
    def in_range(*args: int):
        for arg in args:
            if not (0 <= arg <= 7):
                return False
        return True

    @staticmethod
    def get_alphacol(col: int):
        alphacols = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        return alphacols[col]
