import pygame

from board import Board, indexLetters, rankToRow

game_board = Board()

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("pygame")
clock = pygame.time.Clock()

COLOR1 = (255, 255, 255)
COLOR2 = (0, 0, 0)

box_size = 100

font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 40)

running = True

selected_square = None
destination_square = None

button_rect = pygame.Rect(830, 50, 120, 50)

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if button_rect.collidepoint(event.pos):
                game_board.resetBoard()

            elif event.pos[0] < 800 and event.pos[1] < 800:

                x, y = event.pos

                col = x // box_size
                row = y // box_size

                letter = "abcdefgh"[col]
                number = 8 - row

                clicked_square = (letter, number)

                if selected_square is None:
                    selected_square = clicked_square

                else:
                    piece = game_board.board[row][col]

                    selected_row = rankToRow[selected_square[1]]
                    selected_col = indexLetters[selected_square[0]]

                    piece_in_selected_square = game_board.board[selected_row][
                        selected_col
                    ]

                    if (
                        piece != "."
                        and piece.isupper() == piece_in_selected_square.isupper()
                    ):
                        selected_square = clicked_square

                    else:
                        destination_square = clicked_square

                        game_board.movePiece(
                            selected_square[0],
                            selected_square[1],
                            destination_square[0],
                            destination_square[1],
                        )

                        selected_square = None
                        destination_square = None

    # Draw board
    for row in range(8):
        for col in range(8):

            color = COLOR1 if (row + col) % 2 == 0 else COLOR2

            rect = pygame.Rect(col * box_size, row * box_size, box_size, box_size)

            pygame.draw.rect(screen, color, rect)

            piece = game_board.board[row][col]

            if piece != ".":
                text = font.render(piece, True, (128, 128, 128))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    # Draw button
    pygame.draw.rect(screen, (100, 100, 100), button_rect)

    button_text = button_font.render("RESET", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)

    screen.blit(button_text, button_text_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
