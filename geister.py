import copy
import json
import time
import collections


class Geister:

    def __init__(self, players):
        self.players = {'White': players[0], 'Black': players[1]}
        self.players['White'].set_color('White')
        self.players['Black'].set_color('Black')
        self.turn = 0
        self.goods = {'White': [], 'Black': []}
        self.evils = {'White': [], 'Black': []}
        self.captured = {'White': {'good': 0, 'evil': 0},
                         'Black': {'good': 0, 'evil': 0}}
        self.initial_placement = {'White': [], 'Black': []}
        self.history = []
        for i in range(2):
            active_player = self.players[self.int_to_color(i)]
            initial_placement = active_player.decide_initial_placement()
            self.set_initial_placement(self.int_to_color(i), initial_placement)
        self.winner = None
        self.reason = None

    def color_to_int(self, color):
        if color == 'White':
            return 0
        elif color == 'Black':
            return 1
        else:
            return -1

    def int_to_color(self, n):
        if n == 0:
            return 'White'
        elif n == 1:
            return 'Black'
        else:
            return None

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

    def set_initial_placement(self, color, pattern):
        active = self.color_to_int(color)
        if self.validate_initial_placement(pattern):
            self.initial_placement[color] = pattern[:]
            for i in range(2):
                for j in range(4):
                    x = j + 1 + (3 - 2 * j) * active
                    y = 1 - i + (3 + 2 * i) * active
                    piece = pattern[i * 4 + j]
                    if pattern[i * 4 + j] == 'g':
                        self.goods[color].append((y, x))
                    else:
                        self.evils[color].append((y, x))
        else:
            self.status['winner'] = self.int_to_color((active + 1) % 2)
            self.status['reason'] = 'opponent did foul (wrong initial).'
            return False
        return True

    def print_status(self):
        status = ''
        status += 'Turn ' + str(self.turn) + self.int_to_color(self.turn % 2)
        board = [['-' for j in range(6)] for i in range(6)]
        for i in range(2):
            for y, x in self.goods[self.int_to_color(i)]:
                board[y][x] = 'gG'[i]
            for y, x in self.evils[self.int_to_color(i)]:
                board[y][x] = 'eE'[i]
        for i in range(6):
            status += ''.join(c for c in board[i]) + '\n'
        if self.winner is not None:
            status += 'Winner is ' + self.winner + '\n'
            status += 'win reason is ' + self.reason + '\n'
        return status

    def get_status(self):
        status = {}
        status.update({'turn': self.turn})
        status.update({'active_player': self.int_to_color(self.turn % 2)})
        status.update({'goods': copy.deepcopy(self.goods)})
        status.update({'evils': copy.deepcopy(self.evils)})
        status.update({'captured': copy.deepcopy(self.captured)})
        status.update({'winner': self.winner})
        status.update({'reason': self.reason})
        return status

    def play(self):
        if self.turn > 200:
            self.winner = 'Black'
            self.reason = 'over 200 turn'
        active = self.turn % 2
        active_color = self.int_to_color(active)
        active_player = self.players[self.int_to_color(active)]
        opponent = 1 - active
        opponent_color = self.int_to_color(opponent)

        goods = self.goods[self.int_to_color(active)][:]
        evils = self.evils[self.int_to_color(active)][:]
        enemies = self.goods[opponent_color][:] + self.evils[opponent_color][:]
        captured = copy.copy(self.captured[opponent_color])

        pieces = self.turn, goods, evils, enemies, captured
        sy, sx, ty, tx = active_player.choice_move(*pieces)

        if (sy, sx) not in goods and (sy, sx) not in evils:
            print((sy, sx), goods, evils)
            print('such ghost does not exist')
            exit()
        if (ty, tx) in goods or (ty, tx) in evils:
            print('there is team ghost')
            exit()
        if (ty, tx) in enemies:
            if (ty, tx) in self.goods[opponent_color]:
                self.goods[opponent_color].remove((ty, tx))
                self.captured[opponent_color]['good'] += 1
            elif (ty, tx) in self.evils[opponent_color]:
                self.evils[opponent_color].remove((ty, tx))
                self.captured[opponent_color]['evil'] += 1
            else:
                print('nanika okashii')
                exit()
        if (sy, sx) in goods:
            self.goods[active_color].remove((sy, sx))
            self.goods[active_color].append((ty, tx))
        elif (sy, sx) in evils:
            self.evils[active_color].remove((sy, sx))
            self.evils[active_color].append((ty, tx))
        else:
            exit()
        self.history.append((sy, sx, ty, tx))
        self.turn += 1

    def is_finish(self):
        # 移動終了後からターンを進めるまでの間に呼ばれることを想定
        if self.winner is not None:
            return True
        elif self.turn % 2 == 0:
            if any(g in [(0, 0), (0, 5)] for g in self.goods['Black']):
                self.winner = 'Black'
                self.reason = 'escapable from the deepest line'
            elif self.captured['Black']['good'] == 4:
                self.winner = 'White'
                self.reason = "captured all opponent's good ghosts"
            elif self.captured['Black']['evil'] == 4:
                self.winner = 'Black'
                self.reason = 'captured all own evil ghosts'
            else:
                return False
        else:
            if any(g in [(5, 0), (5, 5)] for g in self.goods['White']):
                self.winner = 'White'
                self.reason = 'escapable from the deepest line'
                return True
            elif self.captured['White']['good'] == 4:
                self.winner = 'Black'
                self.reason = "captured all opponent's good ghosts"
            elif self.captured['White']['evil'] == 4:
                self.winner = 'White'
                self.reason = 'captured all own evil ghosts'
            else:
                return False
        return True

    def get_score(self):
        score = collections.OrderedDict(
            [('date', time.strftime("%Y-%m-%d", time.gmtime())),
             ('white', self.players['White'].get_name()),
             ('black', self.players['Black'].get_name()),
             ('result', ''),
             ('max', self.turn),
             ('position', [[], []]),
             ('kif', [{'type': 'start'}])])
        for i in range(2):
            pos = []
            for c in self.initial_placement[self.int_to_color(i)]:
                if c == 'g':
                    pos.append(1 + 2 * (1 - i))
                else:
                    pos.append(2 + 2 * (1 - i))
            score['position'][1 - i] = pos[:]
        for i in range(self.turn):
            sy, sx, ty, tx = self.history[i]
            score['kif'].append(
                {'from': [sx + 1, sy + 1], 'to': [tx + 1, ty + 1]})
        score['kif'].append({'type': 'resign'})
        if self.winner is not None:
            winner_int = self.color_to_int(self.winner)
            score['result'] = str(1 - winner_int) + '-' + str(winner_int)
            score.update({'reason': self.reason})
        return json.dumps(score)
