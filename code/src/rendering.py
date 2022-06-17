import numpy as np
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def rendering(n_tracks_coordinate, MatOut, interp_factor):
    n_interp_tracks = []
    for tracks in n_tracks_coordinate:
        all_points = []
        all_x = []
        all_y = []
        interp_track = []
        for point in tracks:
            all_points.append(point)
            all_x.append(point[0]*10)
            all_y.append(point[1]*10)

        all_x = np.array(all_x)
        all_y = np.array(all_y)
        sample = np.linspace(1, all_x.shape[0], all_x.shape[0])
        sample_reshape = np.reshape(sample, (-1, 1))

        # poly_reg = PolynomialFeatures(degree=5)
        # sample_ploy = poly_reg.fit_transform(sample_reshape)
        # lr = LinearRegression()
        # lr.fit(sample_ploy, all_x)
        # all_x = lr.predict(sample_ploy)
        # lr = LinearRegression()
        # lr.fit(sample_ploy, all_y)
        # all_y = lr.predict(sample_ploy)

        func_x = interp1d(sample, all_x, kind='linear')
        func_y = interp1d(sample, all_y, kind='linear')

        numx = int(len(all_x) / interp_factor)
        x_sample_new = np.linspace(1, all_x.shape[0], numx)
        y_sample_new = np.linspace(1, all_y.shape[0], numx)

        x_res = func_x(x_sample_new)
        y_res = func_y(y_sample_new)
        x_res = x_res.reshape(-1, 1)
        y_res = y_res.reshape(-1, 1)

        for i in range(x_res.shape[0]):
            if x_res[i] > 0 and x_res[i] <= 1181 and y_res[i] > 0 and y_res[i] <= 781:
                point = (x_res[i], y_res[i])
                interp_track.append(point)
        n_interp_tracks.append(interp_track)

    # 将轨迹累积到MatOut网格, 每有一个轨迹经过，像素值+1
    # for track in n_interp_tracks:
    #     for point in track:
    #          MatOut[int(point[0]), int(point[1])] += 1
    for track in n_interp_tracks:
        flag = np.zeros((1181, 781))
        for point in track:
            if (flag[int(point[0]), int(point[1])] == 0):
                MatOut[int(point[0]-1), int(point[1]-1)] += 1
            flag[int(point[0]), int(point[1])] = 1
    return MatOut
