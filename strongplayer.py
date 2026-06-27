"""A stronger CPU player for the imperfect-information game Geister.

The player keeps the public state as a belief distribution over the opponent's
hidden good/evil assignments and chooses moves by averaging a shallow minimax
search over all assignments that are still possible.
"""

import itertools
import random

import player


class StrongCpuPlayer(player.Player):
    """Belief-based CPU for Geister.

    The engine receives the true identity of its own ghosts and only the
    positions plus capture counts for the opponent.  For each move it enumerates
    every legal assignment of the visible enemy ghosts to good/evil, evaluates
    the resulting position, and pessimistically accounts for the opponent's best
    one-ply reply.  This is not a perfect-information cheat: enemy identities are
    used only as sampled/weighted possibilities consistent with public capture
    information.
    """

    DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    WHITE_ESCAPE = ((5, 0), (5, 5))
    BLACK_ESCAPE = ((0, 0), (0, 5))

    def __init__(self, name='StrongCPU', reply_weight=0.72):
        super().__init__(name=name)
        self.reply_weight = reply_weight

    def decide_initial_placement(self):
        # Put good ghosts nearer the escape side, but randomize left/right so the
        # pattern is not completely predictable.
        rows = [list('gggg'), list('eeee')]
        for row in rows:
            random.shuffle(row)
        return ''.join(rows[0] + rows[1])

    def choice_move(self, turn, goods, evils, enemies, captured):
        moves = self.generate_legal_moves(goods + evils)
        if not moves:
            return None

        assignments = self._enemy_assignments(enemies, captured)
        scored_moves = []
        for move in moves:
            score = self._evaluate_move(turn, goods, evils, enemies, captured,
                                        assignments, move)
            scored_moves.append((score, random.random(), move))
        scored_moves.sort(reverse=True)
        return scored_moves[0][2]

    def _enemy_assignments(self, enemies, captured):
        remaining_good = max(0, min(len(enemies), 4 - captured['good']))
        assignments = []
        for good_tuple in itertools.combinations(enemies, remaining_good):
            enemy_goods = set(good_tuple)
            enemy_evils = set(enemies) - enemy_goods
            assignments.append((list(enemy_goods), list(enemy_evils)))
        return assignments or [([], enemies[:])]

    def _evaluate_move(self, turn, goods, evils, enemies, captured, assignments, move):
        total = 0.0
        for enemy_goods, enemy_evils in assignments:
            fg, fe = goods[:], evils[:]
            eg, ee = enemy_goods[:], enemy_evils[:]
            fg, fe, eg, ee = self._apply_move(fg, fe, eg, ee, move)

            terminal = self._terminal_score(fg, fe, eg, ee)
            if terminal is not None:
                total += terminal
                continue

            own_score = self._static_score(fg, fe, eg, ee, turn + 1)
            reply_score = self._best_opponent_reply_score(fg, fe, eg, ee, turn + 1)
            total += own_score - self.reply_weight * reply_score
        return total / len(assignments)

    def _best_opponent_reply_score(self, fg, fe, eg, ee, turn):
        # Opponent positions are evaluated from their point of view by mirroring
        # colors, then converted back to a penalty for us.
        opponent_moves = self.generate_legal_moves(eg + ee)
        if not opponent_moves:
            return -100000.0

        best = -1000000.0
        for move in opponent_moves:
            neg_eg, neg_ee, neg_fg, neg_fe = self._apply_move(
                eg[:], ee[:], fg[:], fe[:], move)
            if len(neg_fg) < len(fg):
                capture_bonus = 550.0
            elif len(neg_fe) < len(fe):
                capture_bonus = -420.0
            else:
                capture_bonus = 0.0
            terminal = self._terminal_score_for_opponent(neg_eg, neg_ee, neg_fg, neg_fe)
            if terminal is not None:
                score = terminal
            else:
                score = self._static_score_for_color(neg_eg, neg_ee, neg_fg, neg_fe,
                                                     self._opponent_color(), turn)
            best = max(best, score + capture_bonus)
        return best

    def _apply_move(self, fg, fe, eg, ee, move):
        sy, sx, ty, tx = move
        if (sy, sx) in fg:
            fg.remove((sy, sx))
            fg.append((ty, tx))
        else:
            fe.remove((sy, sx))
            fe.append((ty, tx))
        if (ty, tx) in eg:
            eg.remove((ty, tx))
        elif (ty, tx) in ee:
            ee.remove((ty, tx))
        return fg, fe, eg, ee

    def _terminal_score(self, fg, fe, eg, ee):
        if self._has_escape(fg, self.color) or not eg:
            return 100000.0
        if not ee or self._has_escape(eg, self._opponent_color()):
            return -100000.0
        return None

    def _terminal_score_for_opponent(self, og, oe, myg, mye):
        if self._has_escape(og, self._opponent_color()) or not myg:
            return 100000.0
        if not mye or self._has_escape(myg, self.color):
            return -100000.0
        return None

    def _static_score(self, fg, fe, eg, ee, turn):
        return self._static_score_for_color(fg, fe, eg, ee, self.color, turn)

    def _static_score_for_color(self, fg, fe, eg, ee, color, turn):
        score = 0.0
        escape_targets = self.WHITE_ESCAPE if color == 'White' else self.BLACK_ESCAPE
        enemy_color = 'Black' if color == 'White' else 'White'

        score += (4 - len(eg)) * 560.0
        score -= (4 - len(ee)) * 430.0
        score += len(fg) * 180.0 + len(fe) * 80.0

        for g in fg:
            dist = min(abs(g[0] - y) + abs(g[1] - x) for y, x in escape_targets)
            score += 900.0 / (dist + 1) - 35.0 * dist
            if dist == 1:
                score += 650.0
            score -= 220.0 * self._adjacent_count(g, eg + ee)

        for e in fe:
            score += 45.0 * self._adjacent_count(e, eg + ee)
            score += 10.0 * self._forward_progress(e, color)

        enemy_escape = self.WHITE_ESCAPE if enemy_color == 'White' else self.BLACK_ESCAPE
        for g in eg:
            dist = min(abs(g[0] - y) + abs(g[1] - x) for y, x in enemy_escape)
            score -= 650.0 / (dist + 1) - 25.0 * dist
            if dist <= 1:
                score -= 900.0
        return score - 1.5 * turn

    def _adjacent_count(self, pos, others):
        y, x = pos
        return sum((y + dy, x + dx) in others for dy, dx in self.DIRECTIONS)

    def _forward_progress(self, pos, color):
        return pos[0] if color == 'White' else 5 - pos[0]

    def _has_escape(self, goods, color):
        targets = self.WHITE_ESCAPE if color == 'White' else self.BLACK_ESCAPE
        return any(g in targets for g in goods)

    def _opponent_color(self):
        return 'Black' if self.color == 'White' else 'White'
