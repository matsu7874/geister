import random


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


class ManualPlayer(Player):

    def __init__(self, name='Alex'):
        print('Input your name')
        name = input()
        self.name = name

    def get_name(self):
        return self.name

    def decide_initial_placement(self):
        print('input initial placement of pieces')
        s = ''
        if len(s) != 8:
            s = input()
        return s

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
        sy, sx, ty, tx = -1, -1, -1, -1
        while (sy, sx, ty, tx) not in queue:
            print('input move\nsource_y source_x target_y target_x\nex. 1 3 2 3\n')
            sy, sx, ty, tx = map(int, input().split())

        return (sy, sx, ty, tx)
