import random
import copy


class Player:

    def __init__(self, name='Alex'):
        self.name = name

    def decide_initial_placement(self):
        return 'xxxxoooo'

    def choice_move(self, board, took_pieces):
        my_pieces = []
        d = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for y in range(6):
            for x in range(6):
                if board[y][x] == 1 or board[y][x] == 2:
                    my_pieces.append((y, x))
        queue = []
        for y, x in my_pieces:
            for dy, dx in d:
                if 0 <= y + dy < 6 and 0 <= x + dx < 6:
                    if board[y + dy][x + dx] == 0: #TODO: To accept take opponent pieces
                        queue.append((y, x, y + dy, x + dx))
        return random.choice(queue)


class Gister:

    def __init__(self, players):
        if isinstance(players, list):
            self.players = players
        else:
            print('a')
            exit()
        self.board = [[0 for i in range(6)] for j in range(6)]
        self.turn = 0
        for i in range(2):
            initial_placement = self.players[i].decide_initial_placement()
            self.set_initial_placement(i, initial_placement)
        self.took_pieces = []

    def validate_initial_placement(self, pattern):
        cnt_o = 0
        cnt_x = 0
        for i in range(8):
            if pattern[i] == 'o':
                cnt_o += 1
            elif pattern[i] == 'x':
                cnt_x += 1
            else:
                return False
        if cnt_o == 4 and cnt_x == 4:
            return True
        return False

    def set_initial_placement(self, initiative, pattern):
        if self.validate_initial_placement(pattern):
            for i in range(2):
                for j in range(4):
                    x = j + 1 + (3 - 2 * j) * initiative
                    y = 1 - i + (3 + 2 * i) * initiative
                    piece = pattern[i * 4 + j]
                    piece_index = 'ox'.index(piece) + 2 * initiative + 1
                    self.board[y][x] = piece_index

    def is_finish(self):
        if (self.board[5][0] == 1 or self.board[5][5] == 1) and self.turn % 2 == 0:
            return True
        if (self.board[0][0] == 3 or self.board[0][5] == 3) and self.turn % 2 == 1:
            return True
        cnt = [0 for i in range(5)]
        for i in range(6):
            for j in range(6):
                cnt[self.board[i][j]] += 1
        if any(cnt[i] == 0 for i in range(1, 5)):
            return True
        return False

        # if self.turn > 10:
        #     return False
        # return True

    def get_status(self):
        status = '----------\n'
        status += 'Turn ' + str(self.turn) + '\n'
        for i in range(6):
            status += str(self.board[i]) + '\n'
        return status

    def play(self):
        sy,sx,ty,tx = self.players[self.turn % 2].choice_move(self.board, self.took_pieces)
        print((sy,sx),(ty,tx))
        source_cell = self.board[sy][sx]
        target_cell = self.board[ty][tx]
        initiative = self.turn%2
        if initiative == 0 and(source_cell==1 or source_cell == 2):
            if target_cell in [0,3,4]:
                self.board[ty][tx] = source_cell
                self.board[sy][sx] = 0
            else:
                print('illegal move')
                exit()
        if initiative == 1 and(source_cell==3 or source_cell == 4):
            if target_cell in [0,1,2]:
                self.board[ty][tx] = source_cell
                self.board[sy][sx] = 0
            else:
                print('illegal move')
                exit()
        self.turn += 1
    def get_winner(self):
        if (self.board[5][0] == 1 or self.board[5][5] == 1) and self.turn % 2 == 0:
            return 0
        if (self.board[0][0] == 3 or self.board[0][5] == 3) and self.turn % 2 == 1:
            return 1
        cnt = [0 for i in range(5)]
        for i in range(6):
            for j in range(6):
                cnt[self.board[i][j]] += 1
        if cnt[2]==0 or cnt[3] == 0:
            return 0
        elif cnt[1]==0 or cnt[4]==0:
            return 0
        else:
            return -1



def play():
    players = [Player(), Player()]
    g = Gister(players)
    print('setup is finish')
    while not g.is_finish():
        print(g.get_status())
        g.play()
    print(g.get_status())
    print(g.get_winner())

if __name__ == '__main__':
    play()
