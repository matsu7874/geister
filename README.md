# geister
you can play geister with AI written by Python.

## Strong CPU

`strongplayer.StrongCpuPlayer` is a stronger CPU for imperfect-information play.
It enumerates the opponent ghost identities that are consistent with public
capture counts, evaluates candidate moves across that belief distribution, and
accounts for the opponent's likely reply with a shallow minimax search.

```python
import geister
import player
import strongplayer

game = geister.Geister([strongplayer.StrongCpuPlayer(), player.Player()])
while not game.is_finish():
    game.play()
```
