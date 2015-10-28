import time
import random

import geister

import player
import montecarloplayer
import manualplayer


def play(times=100):
    random.seed()
    players = [player.Player(), player.Player()]
    start_time = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    file_name = 'score_' + start_time + '.json'

    result = [{} for i in range(2)]
    total_turn = 0

    for i in range(times):
        g = geister.Geister(players)
        while not g.is_finish():
            # status = g.get_status()
            g.play()
        status = g.get_status()

        if status['reason'] in result[status['winner']]:
            result[status['winner']][status['reason']] += 1
        else:
            result[status['winner']].update({status['reason']: 1})

        f = open(file_name, 'a')
        f.write(g.get_score() + '\n')
        f.close()
        total_turn += status['turn']
    win = [0, 0]
    for i in range(2):
        for k, v in result[i].items():
            print(i, k, v)
            win[i] += v
    print(win[0], '/', win[1])
    print('total turn:', total_turn)

if __name__ == '__main__':
    start = time.time()
    play(100)
    elasped = time.time() - start
    print('elasped:', elasped, '[s]')
