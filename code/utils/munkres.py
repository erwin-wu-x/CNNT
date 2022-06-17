import numpy as np


class Hungary(object):
    def __init__(self, cost_matrix):
        self.C = cost_matrix.copy()
        m, n = self.C.shape
        # 用于记录零的标记情况,M(i,j)=1是stared zero,M(i,j)=2是primed zero
        self.M = np.zeros((m, n))
        self.R_cov = np.zeros((m, 1))  # 用于记录行的覆盖情况
        self.C_cov = np.zeros((n, 1))  # 用于记录列的覆盖情况

        self.Z0_r = 0  # 用于存储step4中找到的primed零的位置
        self.Z0_c = 0
        self.index = np.zeros((m+n, 2))  # 用于存储primed和starred零的坐标


def step3(obj):
    # step 3: 覆盖包含带星零的每一列
    m = obj.M.shape[0]
    n = obj.M.shape[1]
    star = (obj.M == 1)
    obj.C_cov[np.any(star, axis=0)] = 1
    if (star.sum() < n):
        step = step4
    else:
        step = None
    return step


def step4(obj):
    # step 4: 找到未覆盖的0，并prime它
    done = False
    m = obj.M.shape[0]
    n = obj.M.shape[1]
    row = -1
    col = -1
    while (not done):
        for i in range(m):
            for j in range(n):
                if (obj.C[i, j] == 0 and obj.R_cov[i] == 0 and obj.C_cov[j] == 0):
                    row = i
                    col = j
                    break
            else:
                continue
            break
        if (row == -1):  # 没有未被覆盖的零
            done = True
            step = step6
            return step
        else:
            obj.M[row, col] = 2
            exist_star = False
            star_col = -1
            for j in range(n):  # 找primed zero的行中是否有stared zero
                if (obj.M[row, j] == 1):
                    exist_star = True
                    star_col = j
            if (exist_star):  # 如果存在stared zero，覆盖stared zero的行，揭开stared zero的列
                obj.R_cov[row] = 1
                obj.C_cov[star_col] = 0
                step = step4
                return step
            else:  # primed zero的行中没有stared zero
                obj.Z0_r = row
                obj.Z0_c = col
                done = True
                step = step5
                return step
    return step


def step5(obj):
    # step 5: 创建一系列交替的primed和starred zero
    count = 0
    index = obj.index
    m = obj.M.shape[0]
    n = obj.M.shape[1]
    index[count, 0] = obj.Z0_r  # Z0表示在step4中找到的未覆盖primed零
    index[count, 1] = obj.Z0_c
    Z1_r = -1
    Z2_c = -1
    done = False
    while(not done):
        # 在Z0的列中找星号0（如果有的话）
        for i in range(m):
            if (obj.M[i, index[count, 1].astype(int)] == 1):
                Z1_r = i
        if (obj.M[Z1_r, index[count, 1].astype(int)] == 1):
            count = count + 1
            index[count, 0] = Z1_r
            index[count, 1] = index[count - 1, 1]
        else:
            done = True
        # 在Z1的行中找primed零（始终为1个）
        if (not done):
            for j in range(n):
                if (obj.M[index[count, 0].astype(int), j] == 2):
                    Z2_c = j
            count = count + 1
            index[count, 0] = index[count - 1, 0]
            index[count, 1] = Z2_c
    # 取消所有starred零的星号，每一个primed零都标星
    for i in range(count + 1):
        if (obj.M[index[i, 0].astype(int), index[i, 1].astype(int)] == 1):
            obj.M[index[i, 0].astype(int), index[i, 1].astype(int)] = 0
        else:
            obj.M[index[i, 0].astype(int), index[i, 1].astype(int)] = 1
    # 取消矩阵所有覆盖
    obj.R_cov[:] = 0
    obj.C_cov[:] = 0
    # 擦除所有的primed
    obj.M[obj.M == 2] = 0
    step = step3
    return step


def step6(obj):
    # 找到最小未覆盖元素
    minx = 1e6
    m = obj.M.shape[0]
    n = obj.M.shape[1]
    for i in range(m):
        for j in range(n):
            if (obj.R_cov[i] == 0 and obj.C_cov[j] == 0):
                if (obj.C[i, j] < minx):
                    minx = obj.C[i, j]
    # 将在第四步中找到的值添加到每个覆盖行的每个元素, 从每个未覆盖列的元素中减去该值
    for i in range(m):
        for j in range(n):
            if (obj.R_cov[i] == 1):
                obj.C[i, j] = obj.C[i, j] + minx
            if (obj.C_cov[j] == 0):
                obj.C[i, j] = obj.C[i, j] - minx
    step = step4
    return step


def munkres(cost_matrix):
    # 代价矩阵行数需要大于列数
    change = False
    if cost_matrix.shape[1] > cost_matrix.shape[0]:
        cost_matrix = cost_matrix.T
        change = True
    obj = Hungary(cost_matrix)
    m = cost_matrix.shape[0]
    n = cost_matrix.shape[1]
    # step 1:找到每一行的最小值并用每一行的元素减去最小值
    for i in range(m):
        minx = min(obj.C[i, :])
        if (minx != np.inf):
            obj.C[i, :] = obj.C[i, :] - minx
    # step 2:找到矩阵中的零
    for i in range(m):
        for j in range(n):
            if (obj.C[i, j] == 0 and obj.R_cov[i] == 0 and obj.C_cov[j] == 0):
                obj.M[i, j] = 1
                obj.R_cov[i] = 1
                obj.C_cov[j] = 1
    # 进行第3步前将覆盖情况清零
    obj.R_cov[:] = 0
    obj.C_cov[:] = 0
    # step3-step6处理
    step = step3
    while (step is not None):
        step = step(obj)
    # 结果提取
    if change:
        M = obj.M.T
        C = cost_matrix.T
    else:
        M = obj.M
        C = cost_matrix
    not_pair = np.where(C == 10000)
    for i in range(len(not_pair[0])):
        M[not_pair[0][i], not_pair[1][i]] = 0
    result = np.where(M == 1)
    pairs = []
    for i in range(len(result[0])):
        pairs.append([result[0][i], result[1][i]])
    pairs = np.array(pairs)
    return pairs
