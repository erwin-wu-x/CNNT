import numpy as np


def interpolater(point_front, point_cur, interp_factor):
    x = np.linspace(point_front[0]*10, point_cur[0]*10, 1+int(1/interp_factor))
    y = np.linspace(point_front[1]*10, point_cur[1]*10, 1+int(1/interp_factor))
    result = np.array([[int(x[point]), int(y[point])]
                      for point in range(len(x))])
    return np.unique(result, axis=0)


class Bubble():
    def __init__(self, point, id, prev, prev_num, traj_index=None):
        self.point = point
        self.id = id
        self.prev = prev
        self.prev_num = prev_num
        self.traj_index = traj_index


def index_add_1(index, P):
    if index == P:
        return 0
    return index + 1


def index_minus_1(index, P):
    if index == 0:
        return P
    return index - 1


if __name__ == '__main__':
    a = [[1.2, 1.2]]
    b = [[2.0, 2.0]]
    k = interpolater(a[0], b[0], 0.1)
    print(k)
