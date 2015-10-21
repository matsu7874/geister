import player
import geister


def ai_play():
    players = [player.AiPlayer('AI'), player.Player('Random')]
    result = [{} for i in range(2)]
    for i in range(1000):
        g = geister.Geister(players)
        while not g.is_finish():
            status = g.get_status()
            if status['turn'] % 2 == 0:
                cells = [['-' for j in range(6)] for i in range(6)]
                for y, x in status['active_goods']:
                    cells[y][x] = 'g'
                for y, x in status['active_evils']:
                    cells[y][x] = 'e'
                for y, x in status['opponent_goods']:
                    cells[y][x] = 'X'
                for y, x in status['opponent_evils']:
                    cells[y][x] = 'X'

            g.play()
        status = g.get_status()
        if status['reason'] in result[status['winner']]:
            result[status['winner']][status['reason']] += 1
        else:
            result[status['winner']].update({status['reason']: 1})
        if i % 100 == 0:
            print(i)
            win = [0, 0]
            for i in range(2):
                for k, v in result[i].items():
                    print(i, k, v)
                    win[i] += v
            print(win[0], '/', win[1])
    win = [0, 0]
    for i in range(2):
        for k, v in result[i].items():
            print(i, k, v)
            win[i] += v
    print(win[0], '/', win[1])
if __name__ == '__main__':
    ai_play()
