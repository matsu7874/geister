import random


class Player:

    def __init__(self, name='Vanilla'):
        self.name = name

    def get_name(self):
        return self.name

    def decide_initial_placement(self):
        return 'eeeegggg'

    def choice_move(self, goods, evils, enemies, captured, histry=[]):
        # choice randomly from legal hands
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


class ManualPlayer(Player):

    def __init__(self, name):
        print('Input your name>>', end='')
        name = input()
        self.name = name

    def decide_initial_placement(self):
        s = ''
        while not(len(s) == 8 and all(c == 'g' or c == 'e' for c in s)):
            print('input initial placement of pieces')
            s = input()
        return s

    def choice_move(self, goods, evils, enemies, captured, histry=[]):
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
        sy, sx, ty, tx = -1, -1, -1, -1
        while (sy, sx, ty, tx) not in queue:
            print(
                'input move four argument split by space\nsource_y source_x target_y target_x\n')
            s = input()
            if len(s.split()) == 4 and all(c.isdigit() for c in s.split()):
                sy, sx, ty, tx = map(int, s.split())

        return (sy, sx, ty, tx)


class AiPlayer(Player):

    def __init__(self, name='AI'):
        self.name = name

    def decide_initial_placement(self):
        placement = 'eeeegggg'
        for i in range(8):
            r = random.randint(0, 8)
            placement = placement[:r] + placement[r:]
        return placement

    def choice_move(self, goods, evils, enemies, captured, histry=[]):
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
