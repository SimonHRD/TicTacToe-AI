from enum import Enum
import math


class Player(Enum):
    AI = 1
    Human = 2


class Board:
    __board = None

    def __init__(self):
        self.__board = [' '] * 9

    def print(self):
        for i in range(0, 3):
            print(f'| {self.__board[i * 3]} | {self.__board[i * 3 + 1]} | {self.__board[i * 3 + 2]} |')

    def is_field_available(self, field:int):
        if self.__board[field] == ' ':
            return True
        else:
            return False

    def add(self, field: int, symbol: str) -> bool:
        if self.__board[field] == ' ':
            self.__board[field] = symbol
            return True
        return False

    def available_fields(self) -> []:
        columns = []
        for i in range(0, 9):
            if self.__board[i] == ' ':
                columns.append(i)
        return columns

    def check_finished(self) -> str:

        # check rows and columns
        for i in range(0, 3):
            # check rows
            if self.__board[i * 3] == self.__board[i * 3 + 1] == self.__board[i * 3 + 2] and self.__board[i * 3] != ' ':
                return self.__board[i * 3]
            # check columns
            if self.__board[i] == self.__board[i + 3] == self.__board[i + 6] and self.__board[i] != ' ':
                return self.__board[i]

        # check diagonals
        if (self.__board[0] == self.__board[4] == self.__board[8] or self.__board[2] == self.__board[4] == self.__board[
            6]) and self.__board[4] != ' ':
            return self.__board[4]

        # check tie
        if not self.available_fields(): return 'tie'

        return None

    def remove(self, field: int):
        self.__board[field] = ' '


def minimax(board: Board, depth: int, is_maximizing: bool):
    # Look up table
    scores = {'X': 1,
              'O': -1,
              'tie': 0}
    result = board.check_finished()
    if result is not None:
        return scores[result]
    if is_maximizing:
        best_score = -math.inf
        for i in board.available_fields():
            board.add(i, 'X')
            score = minimax(board, depth + 1, False)
            board.remove(i)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in board.available_fields():
            board.add(i, 'O')
            score = minimax(board, depth + 1, True)
            board.remove(i)
            best_score = min(score, best_score)
        return best_score


def best_move(board: Board):
    best_score = -math.inf
    move = None
    for i in board.available_fields():
        board.add(i, 'X')
        score = minimax(board, 0, False)
        board.remove(i)
        if score > best_score:
            best_score = score
            move = i
    return move


def main():
    board = Board()

    game_is_finished = False
    last_played = None

    print('Board Values: ')
    for i in range(0,3):
        print(f'| {i*3} | {i*3+1} | {i*3+2} |')

    while not game_is_finished:
        if last_played == Player.Human or last_played == None:
            field = best_move(board)
            board.add(field, 'X')
            last_played = Player.AI
        else:
            field = int(input("Played row from human: "))
            if 0 <= field <= 8 and board.is_field_available(field):
                board.add(field, 'O')
                last_played = Player.Human
            else:
                print('Invalid field. Choose a free valid field')

        print('')
        board.print()
        print('')

        winner = board.check_finished()
        if winner:
            game_is_finished = True
            if winner == 'tie':
                print("It's a tie!")
            else:
                print(f'{winner} has won!')

    print('game is finished')


if __name__ == '__main__':
    main()
