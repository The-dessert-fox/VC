import cv2
import numpy as np


BOARD_SIZE = 800
SQUARES = 8
SQUARE_SIZE = BOARD_SIZE // SQUARES


def create_chess_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE, 3), dtype=np.uint8)
    light_square = (240, 240, 240)
    dark_square = (30, 30, 30)

    for row in range(SQUARES):
        for col in range(SQUARES):
            color = light_square if (row + col) % 2 == 0 else dark_square
            y1 = row * SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE
            x1 = col * SQUARE_SIZE
            x2 = x1 + SQUARE_SIZE
            board[y1:y2, x1:x2] = color

    return board


def main():
    chess_board = create_chess_board()
    cv2.imshow("800x800 Chess Board", chess_board)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
