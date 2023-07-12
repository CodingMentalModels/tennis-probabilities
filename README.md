# Tennis Probabilities

Script to calculate the probability of winning a tennis game given that the serving player has probability `p` of winning a point.

## Methodology

Models Deuce, Ad In, and Ad Out using a Markov chain with an adjacency matrix, computes `(1 - Q)^{-1}` which yields the expected number of visits before wins / losses, and then sums out the probabilities.

Then, backfills the earlier points by backpropogating through the conditional probabilities from Deuce, Win, and Loss states.

