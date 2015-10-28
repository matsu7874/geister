import player


class ManualPlayer(player.Player):

    def __init__(self, color, name):
        print('Input your name\n>>', end='')
        name = input()
        self.name = name

    def decide_initial_placement(self):
        s = ''
        while not(len(s) == 8 and all(c == 'g' or c == 'e' for c in s)):
            print('input initial placement of pieces')
            print('g:good ghost, e:evil ghost. example: eeeegggg')
            print('>>', end='')
            s = input()
        return s

    def choice_move(self, turn,goods, evils, enemies, captured):
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
            print('input move four argument split by space')
            print('source_y source_x target_y target_x\n')
            print('>> ', end='')
            s = input()
            if len(s.split()) == 4 and all(c.isdigit() for c in s.split()):
                sy, sx, ty, tx = map(int, s.split())

        return (sy, sx, ty, tx)
