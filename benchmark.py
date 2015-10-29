import time
import random

import geister

import player
import montecarloplayer
import manualplayer

def play(times=100):
    random.seed()
    # players = [player.Player(color='White'), player.Player(color='Black')]
    players = [montecarloplayer.MonteCarloPlayer(), player.Player()]
    # players = [montecarloplayer.MonteCarloPlayer(color='White'), montecarloplayer.MonteCarloPlayer(color='Black')]
    start_time = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    file_name = 'score\score_' + start_time + '.json'

    result = {'White': {}, 'Black': {}}
    total_turn = 0

    for i in range(times):
        g = geister.Geister(players)
        while not g.is_finish():
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

    win = {'White': 0, 'Black': 0}
    for c in ['White','Black']:
        for k, v in result[c].items():
            print(c, k, v)
            win[c] += v
    print(win['White'], '/', win['Black'])
    print('total turn:', total_turn)

if __name__ == '__main__':
    start = time.time()
    play(100)
    elasped = time.time() - start
    print('elasped:', elasped, '[s]')
