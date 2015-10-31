import time
import random
import itertools

import geister

import player
import montecarloplayer
import manualplayer
import squareplayer


def play(times=100, white_player=player.Player(), black_player=player.Player()):
    players = [white_player, black_player]
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
    for c in ['White', 'Black']:
        for k, v in result[c].items():
            win[c] += v
    return win['White']

if __name__ == '__main__':
    f = open('log_kdk2.txt','a')
    f.close()
    random.seed()
    p1 = squareplayer.SquarePlayer2()
    p2 = squareplayer.SquarePlayer2()
    n = 6
    times = 1
    scores = [[0,[random.randint(0,10000) for j in range(6400)]] for i in range(n)]
    print('n=',n,'times=',times)
    for _ in range(1000):
        print(_)
        for i in range(5):
            scores[i][0] = 0

        # for i in range(5):
        #     scores[i+5] = [0, scores[i][1][:]]
        #     for j in range(5):
        #         scores[i+5][1][random.randint(0,6399)] = random.randint(1,10000)

        # for i in range(5):
        #     scores[i+10] = [0, scores[i][1][:]]
        #     for j in range(15):
        #         scores[i+10][1][random.randint(0,6399)] = random.randint(1,10000)

        # for i in range(5):
        #     scores[i+15] = [0, scores[i][1][:]]
        #     for j in range(25):
        #         scores[i+15][1][random.randint(0,6399)] = random.randint(1,10000)

        for  i in range(20,n):
            scores[i] = [0,[random.randint(0,10000) for j in range(6400)]]

        for i in range(n):
            for j in range(n):
                p1.set_scores(scores[i][1][:])
                p2.set_scores(scores[j][1][:])
                ww = play(times, p1, p2)
                scores[i][0] += ww
        scores.sort()
        scores.reverse()
        f = open('log_kodoku.txt','a')
        for i in range(5):
            f.write(str(scores[0])+'\n')
        f.close()
        print(scores[0])
        print(scores[1])
        print()
