import itertools
import random


class Player:

    def __init__(self, color='Black', name='Vanilla'):
        self.name = name
        self.color = color

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def set_color(self, color):
        if color in ['White', 'Black']:
            self.color = color

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

    def generate_legal_moves(self, friends):
        moves = []
        for y, x in friends:
            if y > 0:
                if (y - 1, x) not in friends:
                    moves.append((y, x, y - 1, x))
            if y < 5:
                if (y + 1, x) not in friends:
                    moves.append((y, x, y + 1, x))
            if x > 0:
                if (y, x - 1) not in friends:
                    moves.append((y, x, y, x - 1))
            if x < 5:
                if (y, x + 1) not in friends:
                    moves.append((y, x, y, x + 1))
        return moves

    def choice_move(self, turn, goods, evils, enemies, captured):
        # choice randomly from legal hands
        return random.choice(self.generate_legal_moves(goods + evils))


class AiPlayer(Player):

    def __init__(self, name='AI'):
        self.name = name

    def decide_initial_placement(self):
        placement = 'eeeegggg'
        for i in range(8):
            r = random.randint(0, 8)
            placement = placement[r:] + placement[:r]
        return placement

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
        pointed_queue = []
        for sy, sx, ty, tx in queue:
            if (sy, sx) in goods:
                move_good = 1
            else:
                move_good = 0
            score = 0
            score -= 5 * ((5 - sy) + min(sx, 5 - sx))**2
            score += 5 * ((5 - ty) + min(tx, 5 - tx))**2
            for dy, dx in d:
                if (sy + dy, sx + dx) in enemies:
                    score -= 20 * move_good + 5
                if (ty + dy, tx + dx) in enemies:
                    score += 20 * move_good + 5
            if (ty, tx) in enemies:
                if captured['evil'] == 3:
                    score += 300
                else:
                    score -= (7 - ty - min(tx, 5 - tx))**4

            pointed_queue.append((score, (sy, sx, ty, tx)))

        pointed_queue.sort()
        return pointed_queue[0][1]


class SakiyokmiAiPlayer(Player):

    def __init__(self, name='Sakiyomi'):
        self.name = name

    def decide_initial_placement(self):
        placement = 'eeeegggg'
        for i in range(8):
            r = random.randint(0, 8)
            placement = placement[r:] + placement[:r]
        return placement

    def generate_legal_hands(self, goods, evils, enemies):
        d = ((1, 0), (-1, 0), (0, 1), (0, -1))
        hands = []
        my_ghosts = []
        for g in goods:
            my_ghosts.append(g)
        for e in evils:
            my_ghosts.append(e)
        for y, x in my_ghosts:
            for dy, dx in d:
                if 0 <= y + dy < 6 and 0 <= x + dx < 6:
                    if (y + dy, x + dx) not in my_ghosts:
                        hands.append((y, x, y + dy, x + dx))
        return hands

    def evaluate(self, fg, fe, eg, ee):
        score = random.randint(1, 15)
        for y, x in fg:
            score += 100 - 10 * ((5 - y) + (5 - min(5 - x, x)))
        for y, x in fe:
            score += 90 - 8 * ((4 - y) + (4 - min(4 - x, x + 1)))
        for y, x in eg:
            score += -30 - 5 * ((5 - y) + (5 - min(5 - x, x)))
        for y, x in ee:
            score += -20 - 5 * ((5 - y) + (5 - min(5 - x, x)))
        for y, x in fg:
            for ey, ex in eg + ee:
                if abs(y - ey) + abs(x - ex) == 1:
                    score -= 50000
                else:
                    score += 5
        return score

    def sakiyomi(self, friend_goods, friend_evils, enemy_goods, enemy_evils, depth):
        d = ((1, 0), (-1, 0), (0, 1), (0, -1))
        fg = friend_goods[:]
        fe = friend_evils[:]
        eg = enemy_goods[:]
        ee = enemy_evils[:]

        if depth == 0:
            return self.evaluate(friend_goods, friend_evils, enemy_goods, enemy_evils)

        elif depth % 2 == 1:
            for sy, sx, ty, tx in self.generate_legal_hands(fg, fe, eg + ee):
                diff = []
                if (sy, sx) in fg:
                    fg.remove((sy, sx))
                    fg.append((ty, tx))
                    diff.append(('fg', sy, sx, ty, tx))
                else:
                    fe.remove((sy, sx))
                    fe.append((ty, tx))
                    diff.append(('fe', sy, sx, ty, tx))
                if (ty, tx) in eg:
                    eg.remove((ty, tx))
                    diff.append(('eg', ty, tx))
                elif (ty, tx) in ee:
                    ee.remove((ty, tx))
                    diff.append(('ee', ty, tx))
                self.sakiyomi(fg[:], fe[:], eg[:], ee[:], depth - 1)
                for di in diff:
                    if di[0] == 'fg':
                        fg.remove((di[3], di[4]))
                        fg.append((di[1], di[2]))
                    if di[0] == 'fe':
                        fe.remove((di[3], di[4]))
                        fe.append((di[1], di[2]))
                    if di[0] == 'eg':
                        eg.append((di[1], di[2]))
                    if di[0] == 'ee':
                        ee.append((di[1], di[2]))
        else:
            fgr = [(5 - y, 5 - x) for y, x in fg]
            fer = [(5 - y, 5 - x) for y, x in fe]
            egr = [(5 - y, 5 - x) for y, x in eg]
            eer = [(5 - y, 5 - x) for y, x in ee]
            for sy, sx, ty, tx in self.generate_legal_hands(egr, eer, fgr + fer):
                diff = []
                if (sy, sx) in egr:
                    egr.remove((sy, sx))
                    egr.append((ty, tx))
                    diff.append(('eg', sy,  sx, ty, tx))
                else:
                    eer.remove((sy, sx))
                    eer.append((ty, tx))
                    diff.append(('ee',  sy,  sx,  ty, tx))
                if (ty, tx) in fgr:
                    fgr.remove((ty, tx))
                    diff.append(('fg',  ty,  tx))
                elif (ty, tx) in fer:
                    fer.remove((ty, tx))
                    diff.append(('fe',  ty,  tx))
                fgrr = [(5 - y, 5 - x) for y, x in fgr]
                ferr = [(5 - y, 5 - x) for y, x in fer]
                egrr = [(5 - y, 5 - x) for y, x in egr]
                eerr = [(5 - y, 5 - x) for y, x in eer]
                self.sakiyomi(fgrr[:], ferr[:], egrr[:], eerr[:],  depth - 1)
                for di in diff:
                    if di[0] == 'fg':
                        fgr.append((di[1], di[2]))
                    if di[0] == 'fe':
                        fer.append((di[1], di[2]))
                    if di[0] == 'eg':
                        egr.remove((di[3], di[4]))
                        egr.append((di[1], di[2]))
                    if di[0] == 'ee':
                        eer.remove((di[3], di[4]))
                        eer.append((di[1], di[2]))

    def choice_move(self, goods, evils, enemies, captured):
        candidate = []
        for sy, sx, ty, tx in self.generate_legal_hands(goods, evils, enemies):
            fg = goods[:]
            fe = evils[:]
            en = enemies[:]
            eg = random.sample(en, 4 - captured['good'])
            ee = []
            for i in range(len(en)):
                if en[i] not in eg:
                    ee.append(en[i][:])
            if (sy, sx) in goods:
                fg.remove((sy, sx))
                fg.append((ty, tx))
            else:
                fe.remove((sy, sx))
                fe.append((ty, tx))
            if (ty, tx) in eg:
                eg.remove((ty, tx))
            elif (ty, tx) in ee:
                ee.remove((ty, tx))
            score = self.sakiyomi(fg, fe, eg, ee, 3)
            candidate.append((score, (sy, sx, ty, tx)))

        candidate.sort()
        candidate.reverse()
        return candidate[0][1]


class SAiPlayer(Player):

    def __init__(self, name='Sai'):
        self.name = name

    def decide_initial_placement(self):
        placement = 'eeeegggg'
        for i in range(24):
            r = random.randint(0, 8)
            placement = placement[r:] + placement[:r]
        return placement

    def generate_legal_hands(self, goods, evils, enemies):
        d = ((1, 0), (-1, 0), (0, 1), (0, -1))
        hands = []
        my_ghosts = []
        for g in goods:
            my_ghosts.append(g)
        for e in evils:
            my_ghosts.append(e)
        for y, x in my_ghosts:
            for dy, dx in d:
                if 0 <= y + dy < 6 and 0 <= x + dx < 6:
                    if (y + dy, x + dx) not in my_ghosts:
                        hands.append((y, x, y + dy, x + dx))
        return hands

    def evaluate(self, fg, fe, eg, ee):
        d = ((1, 0), (-1, 0), (0, 1), (0, -1))
        score = random.randint(1, 10)
        for y, x in fg:
            score -= [1000, 500, 300, 200, 100, 50, 25, 15,
                      10, 0, 0][(10 - (5 - y) - (5 - min(5 - x, x)))]
        for y, x in fe:
            score -= 0.3 * [1000, 500, 300, 200, 100, 50, 25,
                            15, 10, 0, 0][(10 - (5 - y) - (5 - min(5 - x, x)))]
        for y, x in eg + ee:
            score += -1 * [10000, 1500, 300, 200, 100, 50, 25, 15,
                           10, 0, 0][(10 - (5 - y) - (5 - min(5 - x, x)))] - 10
        for y, x in fg:
            for ey, ex in eg + ee:
                d = abs(y - ey) + abs(x - ex)
                if d == 1:
                    score -= 1000
        return score

    def sakiyomi(self, friend_goods, friend_evils, enemy_goods, enemy_evils, depth):
        d = ((1, 0), (-1, 0), (0, 1), (0, -1))
        fg = friend_goods[:]
        fe = friend_evils[:]
        eg = enemy_goods[:]
        ee = enemy_evils[:]
        return random.randint(1, 10000)

    def choice_move(self, goods, evils, enemies, captured):
        candidate = []
        for sy, sx, ty, tx in self.generate_legal_hands(goods, evils, enemies):
            fg = goods[:]
            fe = evils[:]
            en = enemies[:]
            eg = random.sample(en, 4 - captured['good'])
            ee = []
            for i in range(len(en)):
                if en[i] not in eg:
                    ee.append(en[i][:])
            if (sy, sx) in goods:
                fg.remove((sy, sx))
                fg.append((ty, tx))
            else:
                fe.remove((sy, sx))
                fe.append((ty, tx))
            if (ty, tx) in eg:
                eg.remove((ty, tx))
            elif (ty, tx) in ee:
                ee.remove((ty, tx))
            score = self.evaluate(fg, fe, eg, ee)
            candidate.append((score, (sy, sx, ty, tx)))

        candidate.sort()
        candidate.reverse()
        return candidate[0][1]
