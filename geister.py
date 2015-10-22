import copy
import json
import time
import collections


class Geister:

    def __init__(self, players):
        if isinstance(players, list):
            self.players = players
        else:
            print('first argument must be list of player')
            exit()
        self.turn = 0
        self.goods = [[] for i in range(2)]
        self.evils = [[] for i in range(2)]
        self.captured = [{'good': 0, 'evil': 0} for i in range(2)]
        self.initial_placement = [[], []]
        self.history = []
        for i in range(2):
            initial_placement = self.players[i].decide_initial_placement()
            self.set_initial_placement(i, initial_placement)
        self.winner = None
        self.reason = None

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
            self.initial_placement[active] = pattern[:]
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

    def print_status(self):
        status = ''
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
        if self.winner is not None:
            status += 'Winner is ' + str(self.winner) + '\n'
            status += 'win reason is ' + self.reason + '\n'
        return status

    def get_status(self):
        status = {}
        status.update({'turn': self.turn, 'active_player': self.turn % 2})
        status.update({'active_goods': copy.copy(self.goods[self.turn % 2])})
        status.update({'active_evils': copy.copy(self.evils[self.turn % 2])})
        status.update({'captured': copy.copy(
            self.captured[(self.turn + 1) % 2])})
        status.update({'opponent_goods': copy.copy(
            self.goods[(self.turn + 1) % 2])})
        status.update({'opponent_evils': copy.copy(
            self.evils[(self.turn + 1) % 2])})
        status.update({'winner': self.winner})
        status.update({'reason': self.reason})
        return status

    def play(self):
        if self.turn > 500:
            self.winner = 1
            self.reason = 'over 500 turn'
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
            elif (ty + (5 - 2 * ty) * active, tx + (5 - 2 * tx) * active) in self.evils[(active + 1) % 2]:
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
        self.history.append((sy, sx, ty, tx))
        self.turn += 1

    def is_finish(self):
        if self.winner is not None:
            return True
        if any((g == (5 * ((self.turn % 2 + 1) % 2) + 0, 0)) or (g == (5 * ((self.turn % 2 + 1) % 2) + 0, 5)) for g in self.goods[self.turn % 2]):
            self.winner = self.turn % 2
            self.reason = 'escapable from the deepest line'
            return True
        for i in range(2):
            if len(self.goods[(i + 1) % 2]) == 0:
                self.winner = i
                self.reason = "captured all opponent's good ghosts"
                return True
            if len(self.evils[i]) == 0:
                self.winner = i
                self.reason = "captured all own evil ghosts"
                return True
        return False

    def get_score(self):
        score = collections.OrderedDict([('date', time.strftime("%Y-%m-%d", time.gmtime())),
                                         ('white', self.players[0].get_name()),
                                         ('black', self.players[1].get_name()),
                                         ('result', ''),
                                         ('max', self.turn),
                                         ('position', [[], []]),
                                         ('kif', [{'type': 'start'}])])
        for i in range(2):
            pos = []
            for c in self.initial_placement[i]:
                if c == 'g':
                    pos.append(1 + 2 * i)
                else:
                    pos.append(2 + 2 * i)
            score['position'][i] = pos[:]
        for i in range(self.turn):
            sy, sx, ty, tx = self.history[i]
            if i % 2 == 1:
                sy = 5 - sy
                sx = 5 - sx
                ty = 5 - ty
                tx = 5 - tx
            score['kif'].append(
                {'from': [sx + 1, sy + 1], 'to': [tx + 1, ty + 1]})
        score['kif'].append({'type': 'resign'})
        if self.winner is not None:
            score['result'] = str(1 - self.winner) + '-' + str(self.winner)
        return json.dumps(score)
