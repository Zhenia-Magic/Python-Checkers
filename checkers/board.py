import pygame

from checkers.constants import ROWS, BLACK, SQUARE_SIZE, COLS, WHITE, GREY
from checkers.piece import Piece
from enum import Enum


class Direction(Enum):
    LEFT = 'left'
    RIGHT = 'right'


class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()

    @staticmethod
    def draw_squares(win):
        win.fill(GREY)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_pieces(self, color):
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1

    @property
    def winner(self):
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self._traverse(row - 1, max(row - 3, -1), -1, piece.color, left, Direction.LEFT))
            moves.update(self._traverse(row - 1, max(row - 3, -1), -1, piece.color, right, Direction.RIGHT))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse(row + 1, min(row + 3, ROWS), 1, piece.color, left, Direction.LEFT))
            moves.update(self._traverse(row + 1, min(row + 3, ROWS), 1, piece.color, right, Direction.RIGHT))
        return moves

    def get_all_valid_moves(self, color):
        moves = []
        for piece in self.get_pieces(color):
            for move in self.get_valid_moves(piece).items():
                moves.append((piece, move))
        return moves

    def _traverse(self, start, stop, step, color, direction_num, direction, skipped=None):
        if skipped is None:
            skipped = []
        moves = {}
        last = []

        for r in range(start, stop, step):
            if direction == Direction.RIGHT:
                if direction_num >= COLS:
                    break
            elif direction == Direction.LEFT:
                if direction_num < 0:
                    break

            current = self.board[r][direction_num]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, direction_num)] = last + skipped
                else:
                    moves[(r, direction_num)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse(r + step, row, step, color, direction_num - 1, Direction.LEFT,
                                                skipped=last))
                    moves.update(self._traverse(r + step, row, step, color, direction_num + 1, Direction.RIGHT,
                                                skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            if direction == Direction.RIGHT:
                direction_num += 1
            elif direction == Direction.LEFT:
                direction_num -= 1

        return moves

    def __eq__(self, other):
        return self.board == other.board
