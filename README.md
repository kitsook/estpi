# Estimating the value of PI

Assuming a circle with radius r fitted inside a square with sides of 2r in length.

If we randomly generate points within the square, the ratio of
```
"points inside the circle" : "total number of the points"
= "area of the circle" : "area of the square"
= pi * r^2 : 4 * r^2
```
So pi can be estimated by:
```
pi = 4 * "points inside the circle" / "total number of the points"
```
For ease of calculation, we can just consider a quarter of the circle with r = 1 and the enclosing square with sides of 1.

## Python
* `estpi.py`: simple serial calculation with `for` loop
* `estpi_ray.py`: parallel calculation with [ray farmework](https://github.com/ray-project/ray)


*TODO Other languages*
