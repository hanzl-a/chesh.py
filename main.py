import pygame
from const import *
from sys import exit
from move import Move
from game import Game
from typing import Union
from square import Square


class Main:
    def __init__(self) -> None:
        pygame.init()
        self._init(SIZE, TITLE, ICON_PATH)
        self.game = Game()

    def mainloop(self) -> None:
        screen = self.screen
        game = self.game
        board = game.board
        dragger = game.dragger

        while True:
            game.blit(screen)

            if dragger.dragging:
                game.update_blit(screen)

            game.set_cursor(screen)

            for event in pygame.event.get():
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQUARE_SIZE
                    clicked_col = dragger.mouseX // SQUARE_SIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece

                        if piece.color == game.next_player:
                            board.calc_moves(clicked_row, clicked_col, piece)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            game.blit(screen)

                            game.set_cursor(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.blit(screen)
                        game.update_blit(screen)

                        game.set_cursor(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQUARE_SIZE
                        released_col = dragger.mouseX // SQUARE_SIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            game.next_turn()
                            game.blit(screen)

                    dragger.undrag_piece()

                # keydown
                elif event.type == pygame.KEYDOWN:
                    # reset
                    if event.key == pygame.K_r:
                        pass

                    # theme
                    elif event.key == pygame.K_t:
                        pass

                # quit app
                elif event.type == pygame.QUIT:
                    self._quit()

            pygame.display.update()

    def _init(self, size: Union[tuple, list], title: str, icon_path: str):
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        icon = pygame.image.load(icon_path)
        icon = pygame.transform.smoothscale(icon, (32, 32))
        pygame.display.set_icon(icon)

    def _quit(self):
        pygame.quit()
        exit()


main = Main()
main.mainloop()
