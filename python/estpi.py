from math import sqrt
from time import perf_counter
from random import random
from decimal import *

num_trial = pow(10, 10)

def within_circle(x, y):
    # check if the point is within the circle
    dist = sqrt(x*x + y*y)
    return dist <= 1


in_circle_count = 0
getcontext().prec = 10

start_time = perf_counter()
for i in range(num_trial):
    x = random()
    y = random()
    if within_circle(x, y):
        in_circle_count += 1
end_time = perf_counter()

print("Estimated value of pi is {}".format((Decimal(in_circle_count) / Decimal(num_trial)) * 4))
print("Time taken: {:.2f}s".format(end_time - start_time))

# python estpi.py
# Estimated value of pi is 3.141601314
# Time taken: 4942.45s
