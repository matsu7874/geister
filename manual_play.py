import player
import geister


def play():
    players = [player.ManualPlayer(), player.Player()]
    g = geister.Geister(players)
    while not g.is_finish():
        print(g.get_status())
        g.play()
    print(g.get_status())

if __name__ == '__main__':
    play()
