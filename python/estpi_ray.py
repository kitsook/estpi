from math import sqrt
from random import random
from time import perf_counter
from decimal import *
import ray

num_trial = pow(10, 10)

@ray.remote
def random_dot_in_circle(size):
    count = 0
    for s in range(size):
        x = random()
        y = random()

        # check if the point is within the circle
        dist = sqrt(x*x + y*y)
        if dist <= 1:
            count += 1
    return count

in_circle_count = 0
getcontext().prec = 10

start_time = perf_counter()
chunk_size = 1000000000
completed = 0
objects = []
ray.init()
while completed < num_trial:
    round_size = min(chunk_size, num_trial - completed)
    obj_id = random_dot_in_circle.remote(round_size)
    objects.append(obj_id)
    completed += round_size
ray.wait(objects)
for obj_id in objects:
    in_circle_count += ray.get(obj_id)
end_time = perf_counter()

print("Estimated value of pi is {}".format((Decimal(in_circle_count) / Decimal(num_trial)) * 4))
print("Time taken: {:.2f}s".format(end_time - start_time))

# python estpi_ray.py 
# 2020-04-26 19:57:10,597 INFO resource_spec.py:204 -- Starting Ray with 5.47 GiB memory available for workers and up to 2.74 GiB for objects. You can adjust these settings with ray.init(memory=<bytes>, object_store_memory=<bytes>).
# 2020-04-26 19:57:10,940 INFO services.py:1146 -- View the Ray dashboard at localhost:8266
# Estimated value of pi is 3.141579106
# Time taken: 1540.11s
