import random

import player
# Monte Carlo method


class MonteCarloPlayer(player.Player):

    def __init__(self, name='PrimevalMonteCarlo'):
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

    def choice_move(self, turn, goods, evils, enemies, captured):
        moves = []
        for move in self.generate_legal_moves(goods + evils):
            score = self.evaluate(goods, evils, enemies, captured, move)
            moves.append((score, move[:]))
        moves.sort()
        moves.reverse()
        # f=open('log.txt','a')
        # for move in moves:
        #     f.write(str(move)+'\n')
        # f.close()
        return moves[0][1]

    def evaluate(self, goods, evils, enemies, captured, move):
        opponent_color = 'Black' if self.color == 'White' else 'White'
        win = 0
        for i in range(100):
            fg = goods[:]
            fe = evils[:]
            if (move[0],move[1]) in fg:
                fg.remove((move[0],move[1]))
                fg.append((move[2],move[3]))
            else:
                fe.remove((move[0],move[1]))
                fe.append((move[2],move[3]))
                if len(fe)==0:
                    continue
            eg = random.sample(enemies, 4 - captured['good'])[:]
            ee = [e[:] for e in enemies if e not in eg]
            if (move[2],move[3]) in eg:
                eg.remove((move[2],move[3]))
            elif (move[2],move[3]) in ee:
                ee.remove((move[2],move[3]))
            if self.playout(opponent_color, fg[:], fe[:], eg[:], ee[:]):
                win += 1
        return win

    def playout(self, active, friend_goods, friend_evils, enemy_goods, enemy_evils):
        turn = 0
        while not self.is_finish(active, friend_goods, friend_evils, enemy_goods, enemy_evils) and turn<100:
            if active == self.color:
                moves = self.generate_legal_moves(friend_goods + friend_evils)
                move = random.choice(moves)
                if (move[0], move[1]) in friend_goods:
                    friend_goods.remove((move[0], move[1]))
                    friend_goods.append((move[2], move[3]))
                else:
                    friend_evils.remove((move[0], move[1]))
                    friend_evils.append((move[2], move[3]))
                if (move[2], move[3]) in enemy_goods:
                    enemy_goods.remove((move[2], move[3]))
                elif(move[2], move[3]) in enemy_evils:
                    enemy_evils.remove((move[2], move[3]))
            else:
                moves = self.generate_legal_moves(enemy_goods + enemy_evils)
                move = random.choice(moves)
                if (move[0], move[1]) in enemy_goods:
                    enemy_goods.remove((move[0], move[1]))
                    enemy_goods.append((move[2], move[3]))
                else:
                    enemy_evils.remove((move[0], move[1]))
                    enemy_evils.append((move[2], move[3]))
                if (move[2], move[3]) in friend_goods:
                    friend_goods.remove((move[2], move[3]))
                elif(move[2], move[3]) in friend_evils:
                    friend_evils.remove((move[2], move[3]))
            if active == 'White':
                active = 'Black'
            else:
                active = 'White'
            turn += 1
        return self.did_won(active,friend_goods, friend_evils, enemy_goods, enemy_evils)

    def is_finish(self, active, friend_goods, friend_evils, enemy_goods, enemy_evils):
        # ターン開始直前に呼ばれることを想定
        if self.color == 'Black':
            goods = {'Black': friend_goods, 'White': enemy_goods}
            evils = {'Black': friend_evils, 'White': enemy_evils}
        else:
            goods = {'White': friend_goods, 'Black': enemy_goods}
            evils = {'White': friend_evils, 'Black': enemy_evils}

        if active == 'Black':
            if any(g in [(0, 0), (0, 5)] for g in goods['Black']):
                pass
            elif len(goods['Black']) == 0:
                pass
            elif len(evils['Black']) == 0:
                pass
            else:
                return False
        else:
            if any(g in [(5, 0), (5, 5)] for g in goods['White']):
                pass
            elif len(goods['White']) == 0:
                pass
            elif len(evils['White']) == 0:
                pass
            else:
                return False
        return True

    def did_won(self,active, friend_goods, friend_evils, enemy_goods, enemy_evils):
        # ゲームが終了していることが確かめられた上で呼ばれる
        if len(friend_evils) == 0 or len(enemy_goods) == 0:
            return True
        if self.color == active:
            if self.color == 'White':
                if any(friend_goods) in [(5, 0), (5, 5)]:
                    return True
            else:
                if any(friend_goods) in [(0, 0), (0, 5)]:
                    return True
        return False
