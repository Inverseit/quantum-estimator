from trained import trained_vector
from math import sqrt
w = 800
h = 450
p = 20
step = 50
magic = h // step

def get_index(x, y):
    return (x// step) * magic +  y // step

def unget_index(i):
    y = i % magic
    x = (i - y) // magic
    return {"x": x * step, "y": y * step}

def unget_index_quantum(i, confidence):
    y = i % magic
    x = (i - y) // magic
    return {"x": x * step, "y": y * step, "confidence": sqrt(confidence)}

def get_sim(v, t):
    score = 0
    for i in range(len(v)):
        score += v[i] * t[i]
    return score * score

def get_closest_index(vector):
    ans = None
    max_sim = 0
    for (i, t) in enumerate(trained_vector):
        score = get_sim(vector, t)
        if score > max_sim:
            ans = i
            max_sim = score
    return ans
