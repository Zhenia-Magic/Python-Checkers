import pickle
from functools import lru_cache
from os.path import exists

from checkers.constants import WHITE, BLACK, TRANSPOSITION_TABLE_FILENAME
import secrets


class TranspositionTable:
    """This class represents the transposition table that stores the board configurations and their attributes"""

    def __init__(self):
        self.d = {}

        # I used Zobrist Hashing to hash board configurations. It is a common way to hash board games states.
        # I took the implementation of Zobrist Hashing from https://iq.opengenus.org/zobrist-hashing-game-theory/
        self.zobTable = [[[secrets.SystemRandom().randint(1, 2**64 - 1) for _ in range(12)] for _ in range(8)] for _ in range(8)]

    @staticmethod
    def index(piece):
        """Method to calculate the index of the piece based on its color"""
        if piece == WHITE:
            return 0
        if piece == BLACK:
            return 1
        else:
            return -1

    # Added cash to store the hashes of boards to not recalculate them
    @lru_cache(maxsize=1024)
    def compute_hash(self, board):
        """Method to calculate hash of the board configuration using Zobrist Hashing"""
        h = 0
        for i in range(8):
            for j in range(8):
                place = board[i][j]
                if board[i][j] != 0:
                    piece = self.index(place)
                    h ^= self.zobTable[i][j][piece]
        return h

    def add_entry(self, board, depth, value, flag):
        """Method to add entry to the transposition table"""
        entry_hash = self.compute_hash(tuple(tuple(sublist) for sublist in board))
        if self.d.get(entry_hash) is None:
            self.d[entry_hash] = TableEntry(depth, value, flag)

    def get_entry(self, board):
        """Method to retrieve entry from the transposition table"""
        entry_hash = self.compute_hash(tuple(tuple(sublist) for sublist in board))
        return self.d.get(entry_hash)

    def to_file(self, name=TRANSPOSITION_TABLE_FILENAME):
        """Method to save the transposition table to binary file"""
        a_file = open(name, "wb")
        pickle.dump(self.d, a_file)
        a_file.close()

    def from_file(self, name=TRANSPOSITION_TABLE_FILENAME):
        """Method to retrieve the transposition table from binary file"""
        file_exists = exists(name)
        if file_exists:
            a_file = open(name, "rb")
            self.d = pickle.load(a_file)


class TableEntry:
    """Class for transposition table entry"""

    def __init__(self, depth, value, flag):
        self.depth = depth
        self.value = value
        self.flag = flag
