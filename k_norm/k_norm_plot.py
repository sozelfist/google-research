# coding=utf-8
# Copyright 2025 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script for computing K-norm plot."""

import matplotlib.pyplot as plt
import numpy as np

from k_norm import count_mechanism
from k_norm import lp_mechanism
from k_norm import sum_mechanism
from k_norm import vote_mechanism


d = 50

# Sum experiments
# The following code computes the mean squared l_2 norms of samples from the
# minimal l_1, l_\infty, and Sum balls over 1000 trials, fixing the ambient
# dimension d = 50 and varying the l_0 bound k from 1 to 50. We record the ratio
# (mean squared l_2 norm of Sum ball sample) /
# min(mean squared l_2 norm of l_1 ball sample, mean squared l_2 norm of
# l_\infty ball sample) for each k in sum_ratios.
eulerian_numbers = sum_mechanism.compute_eulerian_numbers(d)
k_range = np.arange(1, 51)
num_trials = 1000
avg_squared_norms = np.zeros((3, len(k_range)))
for i, k in enumerate(k_range):
  if not i % 5:
    print(k)
  avg_squared_norms[0, i] = np.mean(
      np.square(
          np.linalg.norm(
              [
                  k * lp_mechanism.sample_lp_ball(d, 1)
                  for _ in range(num_trials)
              ],
              axis=1,
          )
      )
  )
  avg_squared_norms[1, i] = np.mean(
      np.square(
          np.linalg.norm(
              [
                  lp_mechanism.sample_lp_ball(d, np.inf)
                  for _ in range(num_trials)
              ],
              axis=1,
          )
      )
  )
  avg_squared_norms[2, i] = np.mean(
      np.square(
          np.linalg.norm(
              [
                  sum_mechanism.sample_sum_ball(eulerian_numbers, k)
                  for _ in range(num_trials)
              ],
              axis=1,
          )
      )
  )
sum_ratios = np.divide(
    avg_squared_norms[2], np.minimum(avg_squared_norms[0], avg_squared_norms[1])
)

# Count experiments
# The following code is similar to the Sum code above but uses the Count ball.
k_range = np.arange(1, 51)
num_trials = 1000
avg_squared_norms = np.zeros((3, len(k_range)))
error_norm = 2
for i, k in enumerate(k_range):
  if not i % 5:
    print(k)
  avg_squared_norms[0, i] = np.mean(
      np.square(
          np.linalg.norm(
              [
                  k * lp_mechanism.sample_lp_ball(d, 1)
                  for _ in range(num_trials)
              ],
              axis=1,
          )
      )
  )
  avg_squared_norms[1, i] = np.mean(
      np.square(
          np.linalg.norm(
              [
                  lp_mechanism.sample_lp_ball(d, np.inf)
                  for _ in range(num_trials)
              ],
              axis=1,
          )
      )
  )
  avg_squared_norms[2, i] = np.mean(
      np.square(
          np.linalg.norm(
              [
                  count_mechanism.sample_count_ball(eulerian_numbers, k)
                  for _ in range(num_trials)
              ],
              axis=1,
          )
      )
  )
count_ratios = np.divide(
    avg_squared_norms[2], np.minimum(avg_squared_norms[0], avg_squared_norms[1])
)

# Vote experiments
# The following code is similar to the Sum code above, but uses the Vote ball.
# Since Vote has a single parameter d, with no l_0 bound k, we vary d.
d_range = np.arange(2, d + 1)
num_trials = 1000
avg_squared_norms = np.zeros((3, len(d_range)))
for i, d in enumerate(d_range):
  if not i % 5:
    print(d)
  avg_squared_norms[0, i] = np.mean(
      np.square(
          np.linalg.norm(
              [
                  d * (d - 1) * lp_mechanism.sample_lp_ball(d, 1) / 2
                  for _ in range(num_trials)
              ],
              axis=1,
          )
      )
  )
  avg_squared_norms[1, i] = np.mean(
      np.square(
          np.linalg.norm(
              [
                  (d - 1) * lp_mechanism.sample_lp_ball(d, np.inf)
                  for _ in range(num_trials)
              ],
              axis=1,
          )
      )
  )
  avg_squared_norms[2, i] = np.mean(
      np.square(
          np.linalg.norm(
              [
                  vote_mechanism.sample_vote_ball(eulerian_numbers)
                  for _ in range(num_trials)
              ],
              axis=1,
          )
      )
  )
vote_ratios = np.divide(
    avg_squared_norms[2], np.minimum(avg_squared_norms[0], avg_squared_norms[1])
)

# Plot
# The following code plots the data generated by the three experiments above, on
# a single plot.
plt.plot(
    k_range,
    sum_ratios,
    label="Sum",
    linestyle="solid",
    color="orange",
    linewidth=2
    )
plt.plot(
    k_range,
    count_ratios,
    label="Count",
    linestyle="dotted",
    color="olive",
    linewidth=2
    )
plt.plot(
    d_range,
    vote_ratios,
    label="Vote",
    linestyle="dashed",
    color="teal",
    linewidth=2
    )
plt.xlabel("$k$ or $d$", fontsize=12)
plt.ylabel("expected squared $\ell_2$ norm ratio",  # pylint: disable=anomalous-backslash-in-string
           fontsize=12)
plt.legend(fontsize=12)
plt.title("$K$-norm vs. $\ell_p$",  # pylint: disable=anomalous-backslash-in-string
          fontsize=12)
title = "k_norm_plot"
plt.savefig(title + ".pdf", bbox_inches="tight")
