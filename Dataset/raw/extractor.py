import scipy.io as scio
import numpy as np
import cv2
import matplotlib.pyplot as plt


# for name in range(30):
#     dataFile = str(name+1)+'.mat'
#     data = scio.loadmat(dataFile)
#     data = data['x']
#     for frame in range(800):
#         locations = np.array([item for item in data if item[3] == frame+1])
#         np.savetxt('locations/'+str(name*800+frame)+'.txt', locations)


for name in range(30):
    dataFile = str(name+1)+'.mat'
    data = scio.loadmat(dataFile)
    data = data['x']
    data = cv2.magnitude(data[:, :].real, data[:, :].imag)
    fig = data[:, :, -1]
    # plt.imsave(str(name+1)+'_n1.png', fig, cmap='gray')
    for frame in range(800):
        fig = data[:, :, frame]
        plt.imsave('../figs/'+str(name*800+frame)+'.png', fig, cmap='gray')
