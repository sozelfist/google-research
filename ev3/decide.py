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

"""Methods for the decide stage of EV3."""

import optax

from ev3 import base


def get_decide_tx(
    decide_state,
    decide_init_fn,
    decide_update_fn,
):
  """Generates an Optax transformation that decides how to evolve the model(s).

  Note on tx: In the JAX ecosystem, it is customary to refer to the gradient
  transformation as tx.

  Args:
    decide_state: Parameters for the decide stage.
    decide_init_fn: A function that initializes the state object of the decide
      step.
    decide_update_fn: A function that decides how to update the model given the
      most promising update generated by the propose and optimize stages.

  Returns:
    An Optax transformation object consisting of a pair of functions that
    encode how to initialize the decision state and how to evolve the model(s)
    being optimized.
  """

  def init_fn(model):
    return decide_init_fn(decide_state, model)

  def update_fn(updates, state, model, **extra_args):
    if 'message' in extra_args and extra_args['message'] is not None:
      state = state.replace(message=extra_args['message'])
    return decide_update_fn(updates, state, model)

  return optax.GradientTransformationExtraArgs(init_fn, update_fn)
