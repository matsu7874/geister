import random
import copy


class Player:

    def __init__(self, name='Alex'):
        self.name = name

    def get_name(self):
        return self.name

    def decide_initial_placement(self):
        return 'eeeegggg'

    def choice_move(self, goods, evils, enemies, captured):
        d = ((1, 0), (-1, 0), (0, 1), (0, -1))
        queue = []
        my_ghosts = []
        for g in goods:
            my_ghosts.append(g)
        for e in evils:
            my_ghosts.append(e)
        for y, x in my_ghosts:
            for dy, dx in d:
                if 0 <= y + dy < 6 and 0 <= x + dx < 6:
                    if (y + dy, x + dx) not in my_ghosts:
                        queue.append((y, x, y + dy, x + dx))
        return random.choice(queue)


class Geister:

    def __init__(self, players):
        if isinstance(players, list):
            self.players = players
        else:
            print('second argument must be list of player')
            exit()
        self.turn = 0
        self.goods = [[] for i in range(2)]
        self.evils = [[] for i in range(2)]
        self.captured = [{'good': 0, 'evil': 0} for i in range(2)]
        for i in range(2):
            initial_placement = self.players[i].decide_initial_placement()
            self.set_initial_placement(i, initial_placement)

    def validate_initial_placement(self, pattern):
        cnt_g = 0
        cnt_e = 0
        for i in range(8):
            if pattern[i] == 'g':
                cnt_g += 1
            elif pattern[i] == 'e':
                cnt_e += 1
            else:
                return False
        if cnt_g == 4 and cnt_e == 4:
            return True
        return False

    def set_initial_placement(self, active, pattern):
        if self.validate_initial_placement(pattern):
            for i in range(2):
                for j in range(4):
                    x = j + 1 + (3 - 2 * j) * active
                    y = 1 - i + (3 + 2 * i) * active
                    piece = pattern[i * 4 + j]
                    piece_index = 'ge'.index(piece) + 2 * active + 1
                    if pattern[i * 4 + j] == 'g':
                        self.goods[active].append((y, x))
                    else:
                        self.evils[active].append((y, x))
        else:
            print('In set_initial_placement(), pattern is wrong pattern')

    def is_finish(self):
        active = self.turn % 2
        if any((g == (5 * ((active + 1) % 2) + 0, 0)) or (g == (5 * 5 * ((active + 1) % 2) + 0, 5)) for g in self.goods[active]):
            return True
        if any(len(self.goods[i]) == 0 for i in range(2)) or any(len(self.evils[i]) == 0 for i in range(2)):
            return True
        return False

    def get_status(self):
        status = '----------\n'
        status += 'Turn ' + str(self.turn) + ' Player ' + \
            str(self.turn % 2) + '\n'
        board = [['-' for j in range(6)] for i in range(6)]
        for i in range(2):
            for y, x in self.goods[i]:
                board[y][x] = 'gG'[i]
            for y, x in self.evils[i]:
                board[y][x] = 'eE'[i]
        for i in range(6):
            status += ''.join(c for c in board[i]) + '\n'
        return status

    def play(self):
        active = self.turn % 2
        active_player = self.players[active]

        goods = copy.copy(self.goods[active])
        evils = copy.copy(self.evils[active])
        enemies = copy.copy(self.goods[1 - active])
        for e in copy.copy(self.evils[1 - active]):
            enemies.append(e)
        captured = self.captured[1 - active]

        if active == 1:
            goods = [(5 - y, 5 - x) for y, x in goods]
            evils = [(5 - y, 5 - x) for y, x in evils]
            enemies = [(5 - y, 5 - x) for y, x in enemies]

        sy, sx, ty, tx = active_player.choice_move(
            goods, evils, enemies, captured)

        if (sy, sx) not in goods and (sy, sx) not in evils:
            print((sy, sx), goods, evils)
            print('such ghost does not exist')
            exit()
        if (ty, tx) in goods or (ty, tx) in evils:
            print('there is team ghost')
            exit()
        if (ty, tx) in enemies:
            if (ty + (5 - 2 * ty) * active, tx + (5 - 2 * tx) * active) in self.goods[(active + 1) % 2]:
                self.goods[(active + 1) % 2].remove((ty + (5 - 2 * ty)
                                                     * active, tx + (5 - 2 * tx) * active))
                self.captured[(active + 1) % 2]['good'] += 1
            elif (ty + (5 - 2 * ty) * active, tx + (5 - 2 * tx) * active) in self.goods[(active + 1) % 2]:
                self.evils[(active + 1) % 2].remove((ty + (5 - 2 * ty)
                                                     * active, tx + (5 - 2 * tx) * active))
                self.captured[(active + 1) % 2]['evil'] += 1
            else:
                print('nanika okashii')
        if (sy, sx) in goods:
            self.goods[active].remove(
                (sy + (5 - 2 * sy) * active, sx + (5 - 2 * sx) * active))
            self.goods[active].append(
                (ty + (5 - 2 * ty) * active, tx + (5 - 2 * tx) * active))
        else:
            self.evils[active].remove(
                (sy + (5 - 2 * sy) * active, sx + (5 - 2 * sx) * active))
            self.evils[active].append(
                (ty + (5 - 2 * ty) * active, tx + (5 - 2 * tx) * active))

        self.turn += 1

    def get_winner(self):
        for i in range(2):
            if any((g == (5 * ((i + 1) % 2) + 0, 0)) or (g == (5 * ((i + 1) % 2) + 0, 5)) for g in self.goods[i]):
                return i
            if len(self.goods[(i + 1) % 2]) == 0 or len(self.evils[i]) == 0:
                return i
        return -1


def play():
    players = [Player(), Player()]
    g = Geister(players)
    print('setup is finish')
    while not g.is_finish():
        print(g.get_status())
        g.play()
    print(g.get_status())
    print(g.get_winner())

if __name__ == '__main__':
    play()
