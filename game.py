from const import *
from board import Board
from dragger import Dragger
from typing import Union, Tuple, Any
from pygame import draw, Surface, image, transform, mouse, font


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.dragger = Dragger()

        self.next_player = "white"

    def blit(self, surface: Surface) -> None:
        self._show_bg(surface)
        self._show_last_move(surface)
        self._show_moves(surface)
        self._show_pieces(surface)

        if self.mouse_in():
            self._show_hover(surface)

    def update_blit(self, surface: Surface) -> None:
        piece = self.dragger.piece
        img = transform.smoothscale(image.load(piece.texture), (110, 110))
        img_center = (self.dragger.mouseX, self.dragger.mouseY)
        piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, piece.texture_rect)

    def set_cursor(self, surface: Surface) -> None:
        grab = image.load("assets/cursors/grab.png")
        grabbed = image.load("assets/cursors/grabbed.png")

        cursor = grabbed if self.dragger.dragging else grab

        cursor_img_rect = cursor.get_rect()
        cursor_img_rect.center = mouse.get_pos()

        if self.mouse_in():
            pos = mouse.get_pos()

            row = pos[1] // SQUARE_SIZE
            col = pos[0] // SQUARE_SIZE

            if self.board.squares[row][col].has_piece() or self.dragger.dragging:

                mouse.set_visible(False)
                surface.blit(cursor, cursor_img_rect)
            else:
                mouse.set_visible(True)
        else:
            mouse.set_visible(True)

    def _show_bg(self, surface: Surface) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                colors = ("#edeed1", "#779952")
                self._draw_rect(surface, colors, row, col)

    def _show_pieces(self, surface: Surface) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:

                        img = transform.smoothscale(image.load(piece.texture), (80, 80))
                        img_center = (
                            col * SQUARE_SIZE + SQUARE_SIZE // 2,
                            row * SQUARE_SIZE + SQUARE_SIZE // 2,
                        )
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def _show_hover(self, surface: Surface) -> None:
        pos = mouse.get_pos()

        row = pos[1] // SQUARE_SIZE

        col = pos[0] // SQUARE_SIZE

        if self.board.squares[row][col].has_piece() or self.dragger.dragging:
            self._draw_rect(surface, "#cccccc", row, col, width=3)

    def _show_moves(self, surface: Surface) -> None:
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                self._draw_rect(
                    surface, ("#c86464", "#c84646"), move.final.row, move.final.col
                )

    def _show_last_move(self, surface: Surface) -> None:
        last_move = self.board.last_move

        if last_move:
            initial = last_move.initial
            final = last_move.final
            colors = (
                (244, 247, 116),
                (
                    172,
                    195,
                    51,
                ),
            )
            for pos in [initial, final]:
                self._draw_rect(
                    surface,
                    colors,
                    pos.row,
                    pos.col,
                )

    def _draw_rect(
        self,
        surface: Surface,
        colors: Union[
            Tuple[int, int, int], Tuple[Tuple[int, int, int], Tuple[int, int, int]], str
        ],
        row: int,
        col: int,
        square_size: int = SQUARE_SIZE,
        **kwargs: Any
    ) -> None:
        if isinstance(colors, tuple) and len(colors) <= 2:
            color = colors[0] if (row + col) % 2 == 0 else colors[1]
        else:
            color = colors

        rect = (col * square_size, row * square_size, square_size, square_size)
        draw.rect(surface, color, rect, **kwargs)

    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"

    @staticmethod
    def mouse_in() -> bool:
        mouse_pos = mouse.get_pos()

        if not (0 < mouse_pos[0] < WIDTH - 1 and 0 < mouse_pos[1] < HEIGHT - 1):
            return False

        return True
