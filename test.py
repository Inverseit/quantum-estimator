from functools import reduce
import math
from random import randint, random

from core import get_closest_index, unget_index, unget_index_quantum
from quantum_core import quantum_get_closest_index
from new_quantum_core import get_sim_new

def calculateDiff(x_ap, y_ap, x, y):
  return math.sqrt((x_ap - x) ** 2 + (y_ap - y) ** 2)

def normalizeVector(vector):
  norm = math.sqrt(reduce(lambda x, y: x + y, list(map(lambda x: x * x, vector))))
  return list(map(lambda x: x / norm, vector))


w = 800
h = 450
p = 20
step = 50
magic = h // step

aps = [
  { "x": p, "y": h / 2 },
  { "x": w / 2, "y": p },
  { "x": w - p, "y": h / 2 },
  { "x": w / 2, "y": h - p },
]

def calculateVector(x, y):
  res = []
  for ap in aps:
    x_ap, y_ap = ap["x"], ap["y"]
    d = calculateDiff(x_ap, y_ap, x, y)
    res.append(d)
  raw_norm_vector = normalizeVector(res)
  return normalizeVector(list(map(lambda l:l - 0.5, raw_norm_vector)))


print(calculateVector(10, 200))




error_sum = {
    "classical": 0,
    "quantum_old": 0,
    "quantum_new": 0
}

# num_test = 10
# for i in range(num_test):
#     x, y = randint(0, w), randint(0, h)
#     test_vector = calculateVector(x, y)
#     classical = get_closest_index(test_vector)
#     quantum_old, conf_old = quantum_get_closest_index(test_vector)
#     quantum_new, conf_new = get_sim_new(test_vector, shots=75000)
#     class_loc, old_loc, new_loc = unget_index(classical), unget_index(quantum_old), unget_index(quantum_new)
#     real_location = {'x': x, 'y': y}
#     print(real_location, class_loc, old_loc, new_loc)
#     error_sum["classical"] += math.sqrt((class_loc["x"] - x) ** 2 + (class_loc["y"] - y) ** 2)
#     error_sum["quantum_old"] += math.sqrt((old_loc["x"] - x) ** 2 + (old_loc["y"] - y) ** 2)
#     error_sum["quantum_new"] += math.sqrt((new_loc["x"] - x) ** 2 + (new_loc["y"] - y) ** 2)
#     print("---------------------------------")

# error_sum["classical"]   /= num_test
# error_sum["quantum_old"] /= num_test
# error_sum["quantum_new"] /= num_test

# print(error_sum)


def custom_test():
    x, y = 622, 120
    print(x, y)
    test_vector = calculateVector(x, y)
    classical = get_closest_index(test_vector)
    quantum_old, conf_old = quantum_get_closest_index(test_vector)
    quantum_new, conf_new = get_sim_new(test_vector, shots=75000)
    class_loc, old_loc, new_loc = unget_index(classical), unget_index(quantum_old), unget_index(quantum_new)
    real_location = {'x': x, 'y': y}
    print(real_location, class_loc, old_loc, new_loc)
    error_sum["classical"] += math.sqrt((class_loc["x"] - x) ** 2 + (class_loc["y"] - y) ** 2)
    error_sum["quantum_old"] += math.sqrt((old_loc["x"] - x) ** 2 + (old_loc["y"] - y) ** 2)
    error_sum["quantum_new"] += math.sqrt((new_loc["x"] - x) ** 2 + (new_loc["y"] - y) ** 2)
    print("---------------------------------")

    error_sum["classical"]   /= 1
    error_sum["quantum_old"] /= 1
    error_sum["quantum_new"] /= 1

    print(error_sum)

custom_test()

# 508, 377
