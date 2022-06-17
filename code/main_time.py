import sys
import numpy as np
from tqdm import tqdm
from scipy import io
from src.pairing import *
from src.tracking import *
from src.rendering import *

if __name__ == '__main__':
    # process_num = int(sys.argv[1])
    # begin = int(sys.argv[2])
    process_num = int(10)
    begin = int(0)
    P = 3
    max_distance = 2
    save_track = True
    interp_factor = 0.1

    for patch in range(begin, 30, process_num):
        locations = [np.loadtxt(
            '../Dataset/locations/locations_raw/' + str(patch*800+frame) + '.txt') for frame in range(800)]
        loc_N = locations[0]
        loc_ave_num = np.mean([len(location) for location in locations])

        # Localization data are [intensity, y, x, frame number]
        frame_N = np.empty((len(loc_N), 2))
        frame_N[:, 0] = loc_N[:, 2]
        frame_N[:, 1] = loc_N[:, 1]
        traj_list = []
        MatOut = np.zeros((1181, 781))
        CNNF = [[] for _ in range(P+1)]
        CNNF_head = 0

        # Progress bar
        with tqdm(total=800) as pbar:
            pbar.set_description(
                'Patch {}, average bubble num: {}'.format(patch+1, loc_ave_num))
            for frame in range(1, 800):
                loc_Np1 = locations[frame]

                frame_Np1 = np.empty((len(loc_Np1), 2))
                frame_Np1[:, 0] = loc_Np1[:, 2]
                frame_Np1[:, 1] = loc_Np1[:, 1]

                # # # Pairing
                # pairs = bipartite_graph_pairing(frame_N, frame_Np1, max_distance, savedata=False,
                #                                 dir='../Dataset/pairs/bpairs_18/'+str(patch*800+frame)+'.txt')
                # pairs = Hungarian_pairing(frame_N, frame_Np1, max_distance, savedata=False,
                #                   dir='../Dataset/pairs/bpairs_18/'+str(patch*800+frame)+'.txt')
                # pairs = semi_KNN_pairing(frame_N, frame_Np1, max_distance, savedata=False,
                #                  dir='../Dataset/pairs/test/'+str(patch*800+frame)+'.txt')
                pairs = KNN_pairing(frame_N, frame_Np1, max_distance, savedata=False,
                                    dir='../Dataset/pairs/kpairs_18/'+str(patch*800+frame)+'.txt')
                CNNF_head, CNNF, traj_list = CNNT(
                    frame, pairs, frame_N, frame_Np1, P,  CNNF, CNNF_head, traj_list)
                pbar.update(1)
                frame_N = frame_Np1
        if save_track:
            MatOut = rendering(traj_list, MatOut, interp_factor)
            result = MatOut.T
            # cv2.imshow('1', result)
            # cv2.waitKey(0)
            io.savemat(
                "../Dataset/results/kpair_ctrack_22/result{}.mat".format(patch), {'MatOut': result})
