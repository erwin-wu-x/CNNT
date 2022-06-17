import argparse
import multiprocessing as mp

import numpy as np
from scipy import io

from src.pairing import *
from src.tracking import *
from src.rendering import *
from utils.utils import *

# Constants and configurations
interp_factor = 0.1
Data_Path = 'Dataset/locations/locations_raw/'
Save_Path = 'Dataset/results/result'


def parseArguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tracking bubbles.")
    parser.add_argument("-N", "--process_num", type=int, default=30)
    parser.add_argument("-M", "--method", type=int, default=0)
    parser.add_argument("-P", "--pconstant", type=int, default=5)
    parser.add_argument("-D", "--max_distance", type=float, default=2.0)
    parser.add_argument("-S", "--save_track", type=bool, default=True)
    return parser.parse_args()


def track(patch: int, mode: int, P: int, max_distance: float, save_track: bool) -> None:
    locations = [np.loadtxt(
        Data_Path+'{}.txt'.format(patch * 800+frame)) for frame in range(800)]
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
    frames = [[] for _ in range(P+1)]
    pairs_list = [[] for _ in range(P)]
    frames_head = 0
    pairs_head = 0
    frames[0].append(frame_N)

    # Progress bar
    print('Patch {}, average bubble num: {}'.format(patch + 1, loc_ave_num))
    for frame in range(1, 800):
        loc_Np1 = locations[frame]
        frame_Np1 = np.empty((len(loc_Np1), 2))
        frame_Np1[:, 0] = loc_Np1[:, 2]
        frame_Np1[:, 1] = loc_Np1[:, 1]

        # Pairing
        if mode == 0:
            pairs = bipartite_graph_pairing(
                frame_N, frame_Np1, max_distance, savedata=False, dir='Dataset/pairs/bpairs_18/'+str(patch*800+frame)+'.txt')
        elif mode == 1:
            pairs = Hungarian_pairing(frame_N, frame_Np1, max_distance, savedata=False,
                                      dir='Dataset/pairs/bpairs_18/'+str(patch*800+frame)+'.txt')
        elif mode == 2:
            pairs = semi_KNN_pairing(frame_N, frame_Np1, max_distance, savedata=False,
                                     dir='Dataset/pairs/test/'+str(patch*800+frame)+'.txt')
        else:
            pairs = KNN_pairing(frame_N, frame_Np1, max_distance, savedata=False,
                                dir='Dataset/pairs/kpairs_18/'+str(patch*800+frame)+'.txt')
        if frame < P:
            temp_frames_head, temp_pairs_head = 1, 0
            frames[0].append(frame_Np1)
            for _ in range(frame):
                frames[temp_frames_head].append(frame_Np1)
                pairs_list[temp_pairs_head].append(pairs)
                temp_frames_head += 1
                temp_pairs_head += 1
        if frame >= P:
            frames[frames_head].append(frame_Np1)
            temp_frames_head = index_add_1(frames_head, P)
            temp_pairs_head = pairs_head
            for _ in range(P):
                frames[temp_frames_head].append(frame_Np1)
                pairs_list[temp_pairs_head].append(pairs)
                temp_frames_head = index_add_1(temp_frames_head, P)
                temp_pairs_head = index_add_1(temp_pairs_head, P-1)
            trajs = track_frames(
                frames[frames_head], pairs_list[pairs_head], P)
            traj_list += trajs
            frames[frames_head].clear()
            pairs_list[pairs_head].clear()
            frames_head = index_add_1(frames_head, P)
            pairs_head = index_add_1(pairs_head, P-1)

        frame_N = frame_Np1

    if save_track:
        MatOut = rendering(traj_list, MatOut, interp_factor)
        result = MatOut.T
        io.savemat(
            Save_Path+"{}.mat".format(patch), {'MatOut': result})
    print('Patch {} done'.format(patch + 1))


if __name__ == '__main__':
    # Arguments
    args = parseArguments()
    process_num = args.process_num
    M = args.method
    P = args.pconstant
    D = args.max_distance
    S = args.save_track

    process = [mp.Process(target=track, args=(i, M, P, D, S))
               for i in range(process_num)]
    [p.start() for p in process]
    [p.join() for p in process]
