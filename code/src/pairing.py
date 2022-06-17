import numpy as np
from scipy.spatial import distance, KDTree
from utils.munkres import *


def D_calculator(source_frame, target_frame, max_distance):
    '''
        Form a 2-D distance matrix.
        The matrix entry (i,j) is calculated from distance between the ith bubble
        in source_frame and the jth bubble in target_frame.
        If the distance > max_distance (in pixel units), the corresponding entry
        will be set as 10000.
    '''
    D = distance.cdist(source_frame, target_frame, 'euclidean')
    D[D > max_distance] = 10000
    return D


def bipartite_graph_pairing(frame_N, frame_Np1, max_distance=2, dir='', savedata=True):
    '''
        Partial assignment algorithm for bipartite graph pairing
        which does not require all targets to be paired.
        Return pairs.
    '''
    D = D_calculator(frame_N, frame_Np1, max_distance)
    unpaired_list = list(range(len(frame_N)))
    pairs = []
    while len(unpaired_list) != 0:
        # Dp means D_1\times p
        Dp = D[unpaired_list[0], :].copy()
        index = unpaired_list[0]
        while (Dp[Dp < 10000]).size != 0 and index >= 0:
            Dp_min_index = np.argmin(Dp)
            Dp_min = Dp[Dp_min_index]

            # Dq means D_1\times q
            Dq = D[:, Dp_min_index].copy()
            Dq_min_index = np.argmin(Dq)
            Dq_min = Dq[Dq_min_index]
            if Dq_min == Dp_min:
                unpaired_list.pop(0)
                pairs.append([Dq_min_index, Dp_min_index])
                break

            # search for corresponding bubble for J bubble
            while (Dq[Dq < 10000]).size != 0:
                Dk = D[Dq_min_index, :].copy()
                Dk_min_index = np.argmin(Dk)
                Dk_min = Dk[Dk_min_index]
                if Dk_min == Dq_min:
                    if Dq_min_index in unpaired_list:
                        unpaired_list.remove(Dq_min_index)
                        pairs.append([Dq_min_index, Dk_min_index])
                        if index == Dq_min_index:
                            index = -1
                            break
                    if index > Dq_min_index:
                        Dp = np.array([])
                        break
                    else:
                        Dp[Dp_min_index] = 10000
                        break
                Dq[Dq_min_index] = 10000
                Dq_min_index = np.argmin(Dq)
                Dq_min = Dq[Dq_min_index]
                if Dq_min == Dp_min:
                    unpaired_list.pop(0)
                    pairs.append([Dq_min_index, Dp_min_index])
                    index = -1
                    break
                continue

        if (Dp[Dp < 10000]).size == 0:
            unpaired_list.pop(0)
            continue
    pairs = np.array(pairs)
    if savedata:
        np.savetxt(dir, pairs)
    return pairs


def semi_KNN_pairing(frame_N, frame_Np1, max_distance=2, dir='', savedata=True):
    '''
        Partial assignment algorithm with KD-tree.
        Return pairs.
    '''
    tree_N = KDTree(frame_N)
    tree_Np1 = KDTree(frame_Np1)

    unpaired_list = list(range(len(frame_N)))
    pairs = []
    while len(unpaired_list) != 0:
        # Dp means D_1\times p
        Dp = tree_Np1.query_ball_point(
            frame_N[unpaired_list[0]], max_distance, workers=-1, return_sorted=True).copy()
        index = unpaired_list[0]
        while len(Dp) != 0 and index >= 0:
            Dp_min_index = Dp[0]
            Dp_min = distance.euclidean(
                frame_N[unpaired_list[0]], frame_Np1[Dp_min_index])
            # Dq means D_1\times q
            Dq = tree_N.query_ball_point(
                frame_Np1[Dp_min_index], max_distance, workers=-1, return_sorted=True).copy()
            Dq_min_index = Dq[0]
            Dq_min = distance.euclidean(
                frame_N[Dq_min_index], frame_Np1[Dp_min_index])
            if Dq_min == Dp_min:
                unpaired_list.pop(0)
                pairs.append([Dq_min_index, Dp_min_index])
                break

            # search for corresponding bubble for J bubble
            while len(Dq) != 0:
                Dk = tree_Np1.query_ball_point(
                    frame_N[Dq_min_index], max_distance, workers=-1, return_sorted=True).copy()
                Dk_min_index = Dk[0]
                Dk_min = distance.euclidean(
                    frame_N[Dq_min_index], frame_Np1[Dk_min_index])
                if Dk_min == Dq_min:
                    if Dq_min_index in unpaired_list:
                        unpaired_list.remove(Dq_min_index)
                        pairs.append([Dq_min_index, Dk_min_index])
                        if index == Dq_min_index:
                            index = -1
                            break
                    if index > Dq_min_index:
                        Dp.clear()
                        break
                    else:
                        Dp.pop(0)
                        break
                if len(Dq) == 1:
                    break
                Dq.pop(0)
                Dq_min_index = Dq[0]
                Dq_min = distance.euclidean(
                    frame_N[Dq_min_index], frame_Np1[Dp_min_index])
                if Dq_min == Dp_min:
                    unpaired_list.pop(0)
                    pairs.append([Dq_min_index, Dp_min_index])
                    index = -1
                    break
                continue

        if len(Dp) == 0:
            unpaired_list.pop(0)
            continue
    pairs = np.array(pairs)
    if savedata:
        np.savetxt(dir, pairs)
    return pairs


def KNN_pairing(frame_N, frame_Np1, max_distance=2, dir='', savedata=True):
    '''
        Classical KNN pairing algorithm.
        Return nearest neighbors in radius max distance.
    '''
    tree_N = KDTree(frame_N)
    tree_Np1 = KDTree(frame_Np1)
    nn_list = tree_N.query_ball_tree(tree_Np1, max_distance)
    pairs = []
    for bubble in range(len(nn_list)):
        for nn in nn_list[bubble]:
            pairs.append([bubble, nn])
    pairs = np.array(pairs)
    if savedata:
        np.savetxt(dir, pairs)
    return pairs


def Hungarian_pairing(frame_N, frame_Np1,  max_distance=2, dir='', savedata=True):
    '''
        Classical Hungarian pairing algorithm.
    '''
    D = D_calculator(frame_N, frame_Np1, max_distance)
    pairs = munkres(D)
    pairs = np.array(pairs)
    if savedata:
        np.savetxt(dir, pairs)
    return pairs
