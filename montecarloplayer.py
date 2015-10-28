import random

import player
# Monte Carlo method


class MonteCarloPlayer(player.Player):

    def __init__(self, color='Black', name='PrimevalMonteCarlo'):
        self.name = name

    def decide_initial_placement(self):
        placement = ''
        for i in range(8):
            if placement.count('g') >= 4:
                placement += 'e'
            elif placement.count('e') >= 4:
                placement += 'g'
            else:
                placement += 'ge'[random.randint(0, 1)]
        return placement

    def choice_move(self,turn, goods, evils, enemies, captured):
        moves = []
        for move in self.genelate_legal_moves(goods + evils):
            score = self.evaluate(goods, evils, enemies, captured, move)
            moves.append((score, move[:]))
        moves.sort()
        moves.reverse
        return moves[0][1]

    def genelate_legal_moves(self, friends):
        d = ((1, 0), (-1, 0), (0, 1), (0, -1))
        moves = []
        for y, x in friends:
            for dy, dx in d:
                if 0 <= y + dy < 6 and 0 <= x + dx < 6:
                    if (y + dy, x + dx) not in friends:
                        moves.append((y, x, y + dy, x + dx))
        return moves

    def evaluate(self, goods, evils, enemies, captured, move):
        return random.randint(1, 100)

    def playout(self, active, friend_goods, friend_evils, enemy_goods, enemy_evils):
        while not self.is_finish(active, friend_goods, friend_evils, enemy_goods, enemy_evils):
            pass
        return did_won(friend_goods, friend_evils, enemy_goods, enemy_evils)

    def is_finish(self, active, friend_goods, friend_evils, enemy_goods, enemy_evils):
        # 移動終了後からターンを進めるまでの間に呼ばれることを想定
        if active == 0:
            if any(g in [(0, 0), (0, 5)] for g in goods['Black']):
                pass
            elif captured['Black']['good'] == 4:
                pass
            elif captured['Black']['evil'] == 4:
                pass
            else:
                return False
        else:
            if any(g in [(5, 0), (5, 5)] for g in goods['White']):
                pass
            elif captured['White']['good'] == 4:
                pass
            elif captured['White']['evil'] == 4:
                pass
            else:
                return False
        return True
