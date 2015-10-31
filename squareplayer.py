import random

import player


class SquarePlayer(player.Player):

    def __init__(self, name='Square'):
        self.name = name
        self.scores = [865, 838, 901, 792, 224, 657, 527, 754, 423, 496, 112,
                    603, 776, 413, 932, 780, 387, 315, 218, 958, 941, 86,
                    961,478, 783, 474, 347, 161, 558, 691, 82, 396, 104,
                    762, 101, 909, 110, 112, 475, 570, 382, 207, 2, 124,
                    239, 447, 611, 140, 506, 461, 616, 571, 904, 138, 639,
                     281, 991, 939, 785, 367, 791, 669, 642, 303, 365, 564,
                      48, 133, 665, 552, 237, 361, 991, 340, 478, 610, 275, 844, 720, 25, 340]

    def set_scores(self, scores):
        self.scores = scores

    def choice_move(self, turn, goods, evils, enemies, captured):
        moves = []
        for move in self.generate_legal_moves(goods + evils):
            score = self.evaluate(turn, goods, evils, enemies, captured, move)
            moves.append((score, move[:]))
        moves.sort()
        moves.reverse()
        return moves[0][1]

    def evaluate(self, turn, goods, evils, enemies, captured, move):
        fg = goods[:]
        fe = evils[:]
        if (move[0], move[1]) in fg:
            fg.remove((move[0], move[1]))
            fg.append((move[2], move[3]))
        else:
            fe.remove((move[0], move[1]))
            fe.append((move[2], move[3]))
        en = enemies[:]
        if (move[2], move[3]) in en:
            en.remove((move[2], move[3]))

        score = 0
        d = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for y, x in fg:
            p = 0
            for i in range(4):
                if (y + d[i][0], x + d[i][1]) in fg + fe:
                    p += 1 * 3**i
                elif (y + d[i][0], x + d[i][1]) in en:
                    p += 2 * 3**i
            score += self.scores[p]

        return score
class SquarePlayer2(player.Player):

    def __init__(self, name='Square'):
        self.name = name
        self.scores = [random.randint(1,10000) for i in range(6400)]

    def set_scores(self, scores):
        self.scores = scores

    def choice_move(self, turn, goods, evils, enemies, captured):
        moves = []
        for move in self.generate_legal_moves(goods + evils):
            score = self.evaluate(turn, goods, evils, enemies, captured, move)
            moves.append((score, move[:]))
        moves.sort()
        moves.reverse()
        return moves[0][1]

    def evaluate(self, turn, goods, evils, enemies, captured, move):
        fg = goods[:]
        fe = evils[:]
        if (move[0], move[1]) in fg:
            fg.remove((move[0], move[1]))
            fg.append((move[2], move[3]))
        else:
            fe.remove((move[0], move[1]))
            fe.append((move[2], move[3]))
        en = enemies[:]
        if (move[2], move[3]) in en:
            en.remove((move[2], move[3]))

        score = 0
        d = [(0,0),(0,1),(1,0),(1,1)]
        for i in range(5):
            for j in range(5):
                p = (i*5+j)*256
                for k in range(4):
                    if (i+d[k][0], j+d[k][1]) in fg:
                        p += 1*4**k
                    elif (i+d[k][0], j+d[k][1]) in fe:
                        p += 2*4**k
                    elif (i+d[k][0], j+d[k][1]) in en:
                        p += 3*4**k
                score += self.scores[p]
        return score
