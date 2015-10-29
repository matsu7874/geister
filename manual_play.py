import time
import random

import geister

import player
import montecarloplayer
import manualplayer


def play(times=100):
    random.seed()
    players = [montecarloplayer.MonteCarloPlayer(), manualplayer.ManualPlayer()]
    start_time = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    file_name = 'score\score_' + start_time + '.json'

    result = {'White': {}, 'Black': {}}
    for _ in range(times):
        g = geister.Geister(players)
        while not g.is_finish():
            status = g.get_status()
            cells = [['-' for j in range(6)] for i in range(6)]
            for y, x in status['goods']['White']:
                cells[y][x] = 'g'
            for y, x in status['evils']['White']:
                cells[y][x] = 'e'
            for y, x in status['goods']['Black']:
                cells[y][x] = 'X'
            for y, x in status['evils']['Black']:
                cells[y][x] = 'X'
            print(status['turn'])
            print('yx012345')
            for i in range(5, -1, -1):
                print(i, ''.join(cells[i]))
            print('yx012345')
            print(status['captured']['Black'])
            g.play()
        status = g.get_status()

        if status['reason'] in result[status['winner']]:
            result[status['winner']][status['reason']] += 1
        else:
            result[status['winner']].update({status['reason']: 1})

        f = open(file_name, 'a')
        f.write(g.get_score() + '\n')
        f.close()
        print(status['winner'],status['reason'])

if __name__ == '__main__':
    play(1)
