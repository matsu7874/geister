import player
import geister
import time


def manual_play():
    players = [player.SAiPlayer(),player.SAiPlayer()]
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
            print(status['turn'])
            print('yx012345')
            for i in range(5, -1, -1):
                print(i, ''.join(cells[i]))
            print('yx012345')
            print(status['captured'])
        g.play()
    status = g.get_status()
    print(status)
    print(status['winner'], status['reason'])
    file_name = 'score\score_'+time.strftime("%Y%m%d_%H%M%S", time.gmtime())+'.json'
    f = open(file_name,'a')
    f.write(g.get_score()+'\n')
    f.close()


if __name__ == '__main__':
    manual_play()
