import random
import unittest

import geister
import player
import strongplayer


class StrongCpuPlayerTest(unittest.TestCase):

    def setUp(self):
        self.cpu = strongplayer.StrongCpuPlayer()
        self.cpu.set_color('White')

    def test_initial_placement_is_valid_and_escape_oriented(self):
        random.seed(0)
        placement = self.cpu.decide_initial_placement()

        self.assertEqual(len(placement), 8)
        self.assertEqual(placement.count('g'), 4)
        self.assertEqual(placement.count('e'), 4)
        self.assertEqual(placement[:4], 'gggg')
        self.assertEqual(placement[4:], 'eeee')

    def test_enemy_assignments_match_public_capture_counts(self):
        enemies = [(0, 1), (0, 2), (1, 1), (1, 2), (2, 1)]
        captured = {'good': 2, 'evil': 1}

        assignments = self.cpu._enemy_assignments(enemies, captured)

        # Five visible enemies with two remaining good ghosts means C(5, 2)
        # identity assignments are possible.
        self.assertEqual(len(assignments), 10)
        for enemy_goods, enemy_evils in assignments:
            self.assertEqual(len(enemy_goods), 2)
            self.assertEqual(len(enemy_evils), 3)
            self.assertEqual(set(enemy_goods) | set(enemy_evils), set(enemies))
            self.assertFalse(set(enemy_goods) & set(enemy_evils))

    def test_apply_move_moves_friend_and_captures_enemy(self):
        fg = [(4, 0)]
        fe = [(1, 1)]
        eg = [(5, 0)]
        ee = [(3, 3)]

        new_fg, new_fe, new_eg, new_ee = self.cpu._apply_move(
            fg[:], fe[:], eg[:], ee[:], (4, 0, 5, 0))

        self.assertIn((5, 0), new_fg)
        self.assertNotIn((4, 0), new_fg)
        self.assertEqual(new_fe, fe)
        self.assertNotIn((5, 0), new_eg)
        self.assertEqual(new_ee, ee)

    def test_choice_move_takes_immediate_escape_win(self):
        random.seed(0)
        goods = [(4, 0), (0, 1), (0, 2), (0, 3)]
        evils = [(1, 1), (1, 2), (1, 3), (2, 2)]
        enemies = [
            (3, 0), (3, 1), (3, 2), (3, 3),
            (4, 4), (5, 4), (2, 4), (2, 5),
        ]
        captured = {'good': 0, 'evil': 0}

        move = self.cpu.choice_move(10, goods, evils, enemies, captured)

        self.assertEqual(move, (4, 0, 5, 0))

    def test_black_choice_move_takes_immediate_escape_win(self):
        random.seed(0)
        self.cpu.set_color('Black')
        goods = [(1, 5), (5, 1), (5, 2), (5, 3)]
        evils = [(4, 1), (4, 2), (4, 3), (3, 3)]
        enemies = [
            (2, 0), (2, 1), (2, 2), (2, 3),
            (1, 1), (0, 1), (3, 1), (3, 0),
        ]
        captured = {'good': 0, 'evil': 0}

        move = self.cpu.choice_move(10, goods, evils, enemies, captured)

        self.assertEqual(move, (1, 5, 0, 5))

    def test_terminal_scores_distinguish_wins_and_losses(self):
        self.assertEqual(
            self.cpu._terminal_score([(5, 0)], [(0, 0)], [(2, 2)], [(3, 3)]),
            100000.0)
        self.assertEqual(
            self.cpu._terminal_score([(2, 0)], [(0, 0)], [(2, 2)], []),
            -100000.0)
        self.assertIsNone(
            self.cpu._terminal_score([(2, 0)], [(0, 0)], [(2, 2)], [(3, 3)]))

    def test_complete_game_runs_to_finish_against_random_player(self):
        random.seed(1)
        game = geister.Geister([strongplayer.StrongCpuPlayer(), player.Player()])

        while not game.is_finish():
            game.play()

        self.assertIn(game.winner, ['White', 'Black'])
        self.assertIsNotNone(game.reason)
        self.assertGreater(game.turn, 0)
        self.assertLessEqual(game.turn, 101)


if __name__ == '__main__':
    unittest.main()
