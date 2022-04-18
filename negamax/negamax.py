import pygame
from copy import deepcopy
from checkers.constants import WHITE, BLACK
from enum import Enum


# Flags for the transposition table records
class Flag(Enum):
    EXACT = 'exact'
    LOWERBOUND = 'lowerbound'
    UPPERBOUND = 'upperbound'


# negamax algorithm with alpha-beta pruning and transposition table
def negamax(board, depth, color, color_num, game, alpha, beta, transposition_table):
    """This function is used to return the optimal next move and the value of eval function for this move"""

    # save original alpha value
    alpha_original = alpha

    # lookup for the board in the transposition table. If it is there, it can speed up the process hugely.
    lookup = transposition_table.get_entry(board.board)
    if lookup is not None and lookup.depth >= depth:
        if lookup.flag == Flag.EXACT:
            return lookup.value, board
        elif lookup.flag == Flag.LOWERBOUND:
            alpha = max(alpha, lookup.value)
        elif lookup.flag == Flag.UPPERBOUND:
            beta = min(beta, lookup.value)

        if alpha >= beta:
            return lookup.value, board

    # base case for the recursion, if we reached up the max depth of search or the game is over
    if depth == 0 or board.winner is not None:
        return color_num * evaluation_function(board), board

    value, next_board = float('-inf'), None

    # recursion through the nodes in the search tree
    for piece in board.get_pieces(color):
        for move, skip in board.get_valid_moves(piece).items():
            # uncomment next line to see how algorithm checks moves to find the optimal one
            # draw_moves(game, board, piece)

            # simulate the move
            simulated_board = simulate_move(board, piece, move, skip)
            opponent_color = BLACK if color == WHITE else WHITE

            # calculate the value of eval function for the new board after the move
            new_value = -1 * negamax(simulated_board, depth - 1, opponent_color, -1 * color_num,
                                     game, -1 * beta, -1 * alpha, transposition_table)[0]

            # if the value is higher than all values we've seen before, store this value and the board after this move
            if new_value > value:
                value, next_board = new_value, simulated_board

            # update alpha value if necessary
            alpha = max(alpha, new_value)

            # if alpha is bigger than beta, cut off the tree
            if alpha >= beta:
                break

    # store the resulting board in the transposition table
    if value <= alpha_original:
        flag = Flag.UPPERBOUND
    elif value >= beta:
        flag = Flag.LOWERBOUND
    else:
        flag = Flag.EXACT
    transposition_table.add_entry(board.board, depth, value, flag)

    return value, next_board


def simulate_move(board, piece, move, skip):
    """This function is used to simulate the move without affecting actual board nd pieces on it"""
    board_copy = deepcopy(board)
    piece_copy = board_copy.get_piece(piece.row, piece.col)
    board_copy.move(piece_copy, *move)
    if len(skip) > 0:
        board_copy.remove(skip)
    return board_copy


def evaluation_function(board):
    """This function calculates the value of evaluation function for particular board configuration."""
    return (board.white_left - board.white_kings) + board.white_kings * 2 - (board.black_left -
                                                                             board.black_kings) - board.black_kings * 2


def draw_moves(game, board, piece):
    """This helper function shows the searching process of the negamax algorithm"""
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(1000)
