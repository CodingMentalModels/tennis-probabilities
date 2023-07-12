
from math import isclose
import numpy as np
from scipy.linalg import inv

# Define p and q
p = 0.6
q = 1 - p

# Define your transition matrix
P = np.array([
    [1.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0, 0.0],
    [p,   0.0, 0.0, 0.0, q],
    [0.0, q,   0.0, 0.0, p],
    [0.0, 0.0, p,   q,   0.0]
])

# Find Q and R from your transition matrix
Q = P[2:, 2:]
R = P[2:, :2]

# Compute the fundamental matrix N
I = np.eye(Q.shape[0])
N = inv(I - Q)

# Compute the matrix B
B = np.matmul(N, R)

print("Fundamental matrix N:")
print(N)
print("\nMatrix B:")
print(B)

ps_given_ad_in = B[-3]
ps_given_ad_out = B[-2]
ps_given_deuce = B[-1]

class TennisProbabilities:

    def __init__(self):
        self._ps = np.full((5, 5), np.nan)

    def pretty_print(self):
        to_return = []
        for i in range(0, 5):
            for j in range(0, 5):
                if not TennisProbabilities._is_valid_coordinate(i, j):
                    continue
                p_win = round(self._ps[i][j], 3)
                p_loss = round(1 - p_win, 3)
                to_return.append("{}: {} vs. {}".format(TennisProbabilities._i_j_to_string(i, j), p_win, p_loss))
        to_return = "\n".join(to_return)
        return to_return

    def _is_valid_coordinate(i, j):
        if i > 4 or j > 4:
            return False
        if i == 4 and j != 3:
            return False
        if j == 4 and i != 3:
            return False
        return True

    def _i_j_to_string(i, j):
        if i < 3:
            assert j <= 3
        if j < 3:
            assert i <= 3

        if i == j == 3:
            return "Deuce"
        elif i == 4 and j == 3:
            return "Ad In"
        elif i == 3 and j == 4:
            return "Ad Out"
        else:
            return "{}-{}".format(TennisProbabilities._idx_to_string(i), TennisProbabilities._idx_to_string(j))

    def _idx_to_string(i):
        assert i <= 3
        if i == 0:
            return "0"
        elif i == 1:
            return "15"
        elif i == 2:
            return "30"
        elif i == 3:
            return "40"


    def backfill(self, p_ad_in, p_ad_out, p_deuce, p):
        self._ps[4][3] = p_ad_in
        self._ps[3][4] = p_ad_out
        self._ps[3][3] = p_deuce
        self._ps[4][4] = p_deuce

        i = 3
        while i >= 0:
            j = 3
            while j >= 0:
                new_p = self._backpropogate(self._get_good_win_state(i, j), self._get_bad_win_state(i, j), p)
                self._insert_checked(i, j, new_p)
                j = j - 1
            i = i - 1

    def _backpropogate(self, p_win_given_good_state, p_win_given_bad_state, p):
        # P(win | previous_state) = p * P(win | good_state) + (1 - p) * P(win | bad_state)
        return p * p_win_given_good_state + (1 - p) * p_win_given_bad_state

    def _get_good_win_state(self, i, j):
        if i == 3 and j < 3:
            return 1.0
        else:
            return self._ps[i + 1][j]

    def _get_bad_win_state(self, i, j):
        if j == 3 and i < 3:
            return 0.0
        else:
            return self._ps[i][j + 1]


    def _insert_checked(self, i, j, new_p):
        if not np.isnan(self._ps[i][j]):
            assert isclose(self._ps[i][j], new_p), "{} should be close to {} but isn't".format(new_p, self._ps[i][j])
        self._ps[i][j] = new_p



ps = TennisProbabilities()
ps.backfill(ps_given_ad_in[0], ps_given_ad_out[0], ps_given_deuce[0], p)
print(ps.pretty_print())
