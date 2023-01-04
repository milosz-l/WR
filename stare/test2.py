from math import dist


def euclidean_distance(vx, vy):
    return sum((y-x)**2 for x, y in zip(vx, vy)) ** 0.5


print(euclidean_distance([0, 0, 0, 0], [255, 255, 255, 255]))

print(dist([0, 0, 0, 0], [255, 255, 255, 255]))
