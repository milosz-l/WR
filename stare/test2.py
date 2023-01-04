from math import dist


def euclidean_distance(vx, vy):
    return sum((y-x)**2 for x, y in zip(vx, vy)) ** 0.5


# print(euclidean_distance([0, 0, 0, 0], [255, 255, 255, 255]))

# print(dist([0, 0, 0, 0], [255, 255, 255, 255]))


BLUE_L = [17, 59, 90]
BLUE_R = [25, 57, 180]
GREEN_L = [12, 75, 32]
GREEN_R = [22, 70, 63]
BLACK_L = [16, 22, 19]
BLACK_R = [22, 22, 38]


rgb_l = [23, 23, 23]
distances_l = {}
distances_l['Black'] = euclidean_distance(rgb_l, BLACK_L)
distances_l['Blue'] = euclidean_distance(rgb_l, BLUE_L)
distances_l['Green'] = euclidean_distance(rgb_l, GREEN_L)
# print(min(distances_l.values()).index())
print(min(distances_l, key=distances_l.get))
