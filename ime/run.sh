#!/bin/bash
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


set -e
set -x

virtualenv -p python3 .
source ./bin/activate


pip install -r requirements.txt
python -m main.py --model IME_WW --data ECL --num_experts 10  --seq_len 336 --pred_len 24  --learning_rate 0.0001 --learning_rate_gate 0.001 --utilization_hp 10 --smoothness_hp 0.1 --diversity_hp 0