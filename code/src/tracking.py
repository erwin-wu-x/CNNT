import numpy as np
from utils.utils import *


def backtrack(bubble_prev_list, P, traj_list, traj_index):
    if P == 0:
        return traj_list
    cash_list = []
    for bubble_prev in bubble_prev_list:
        if bubble_prev.prev_num < P-1:
            continue
        cash_list.append(bubble_prev)
    for bubble_prev in cash_list:
        traj_list[traj_index].append(bubble_prev.point)
        traj_list = backtrack(
            bubble_prev.prev, P-1, traj_list, traj_index)
    return traj_list


def CNNT(frame, pairs, frame_N, frame_Np1, P, CNNF, CNNF_head, traj_list):
    traj_index = len(traj_list) - 1
    if frame == 1:
        # init the CNNF
        for pair in pairs:
            if frame_N[pair[0]][0] == frame_Np1[pair[1]][0] and frame_N[pair[0]][1] == frame_Np1[pair[1]][1]:
                continue
            bubble_prev = Bubble(frame_N[pair[0]], pair[0], None, 0)
            CNNF[0].append(bubble_prev)
            existence_monitor = 0
            # if the bubble is added
            for bubble in CNNF[1]:
                if bubble.id == pair[1]:
                    bubble.prev.append(bubble_prev)
                    existence_monitor = 1
                    break
            # if the bubble is not added
            if existence_monitor == 0:
                CNNF[1].append(Bubble(frame_Np1[pair[1]],
                               pair[1], [bubble_prev], 1))
        CNNF_head = 1
    else:
        # bubbles added by last frame
        bubbles_prev = CNNF[index_minus_1(CNNF_head, P)]
        for pair in pairs:
            if frame_N[pair[0]][0] == frame_Np1[pair[1]][0] and frame_N[pair[0]][1] == frame_Np1[pair[1]][1]:
                continue
            # Processing pair[0] bubble
            # if the bubble is added by last frame
            bubble_prev = None
            existence_monitor = 0
            for bubble_prev_exist in bubbles_prev:
                if bubble_prev_exist.id == pair[0]:
                    bubble_prev = bubble_prev_exist
                    existence_monitor = 1
                    break
            # if the bubble is not added by last frame
            if existence_monitor == 0:
                bubble_prev = Bubble(frame_N[pair[0]], pair[0], None, 0)
                CNNF[index_minus_1(CNNF_head, P)].append(bubble_prev)
            # Processing pair[1] bubble
            bubble = None
            existence_monitor = 0
            # if the bubble is added by past pairs
            for bubble_exist in CNNF[CNNF_head]:
                if bubble_exist.id == pair[1]:
                    bubble = bubble_exist
                    bubble.prev.append(bubble_prev)
                    bubble.prev_num = max(
                        bubble.prev_num, bubble_prev.prev_num+1)
                    existence_monitor = 1
                    break
            # if the bubble is not added by past pairs.
            if existence_monitor == 0:
                bubble = Bubble(frame_Np1[pair[1]], pair[1], [
                                bubble_prev], bubble_prev.prev_num+1)
                CNNF[CNNF_head].append(bubble)
            # add points to traj_list
            if bubble_prev.traj_index != None and bubble.prev_num >= P:
                temp_traj_index = bubble_prev.traj_index
                traj_list[temp_traj_index].append(bubble.point)
                bubble.traj_index = traj_index
            if bubble_prev.traj_index == None and bubble.prev_num == P:
                # back track for depth P
                traj_list.append([bubble.point])
                traj_index += 1
                bubble.traj_index = traj_index
                traj_list = backtrack(
                    bubble.prev, P, traj_list, traj_index)
    CNNF_head = index_add_1(CNNF_head, P)
    CNNF[CNNF_head].clear()
    #         if save_track:
    #             # interpolation
    #             interp_points = np.empty((2, 2))
    #             if bubble.prev_num > P:
    #                 interp_points = interpolater(
    #                     bubble_prev.point, bubble.point, interp_factor)
    #             if bubble.prev_num == P:
    #                 # back track for depth P
    #                 interp_points = backtrack(bubble.prev, P, bubble.point,
    #                                         interp_factor, interp_points)
    #             # rending
    #             for point in interp_points[2:]:
    #                 MatOut[int(point[0]), int(point[1])] += 1
    # CNNF_head = index_add_1(CNNF_head, P)
    # CNNF[CNNF_head].clear()
    return CNNF_head, CNNF, traj_list


def track_frames(n_points, n_pairs, P):
    # n_points: 连续P帧所有点的坐标
    # n_pairs：帧与帧之间的匹配结果
    # P: 连续帧个数
    # there are P frames points and P-1 frames pairs.
    P = P+1
    n_tracks_coordinate = []  # 保存tracks的坐标
    points_1 = n_pairs[0][:, 0]
    frame1_coordinates = n_points[0]
    frame2_coordinates = n_points[1]
    for i0 in range(points_1.shape[0]):  # first frame paired points num
        track = []
        track_coordinate = []
        point = points_1[i0]  # first point
        track.append(point)
        point2 = n_pairs[0][:, 1][i0]  # correspoding point
        track.append(point2)

        point_coordinate = frame1_coordinates[point]
        track_coordinate.append(point_coordinate)
        point2_coordinate = frame2_coordinates[point2]
        track_coordinate.append(point2_coordinate)
        p = point2

        frame_2 = 2
        # find point2 (the corresopoding paired points) in following frames
        # i correspond to the pairs, which actually the paired[0] part counters
        for i in range(1, P-1):
            pair = n_pairs[i]
            frame_2_coordinates = n_points[frame_2]
            if (pair[:, 0].__contains__(p)):  # if the point2 in these pairs
                # find the correspoding pair
                p_index = np.argwhere(pair[:, 0] == p)[0, 0]
                track.append(pair[:, 1][p_index])

                p_coordinate = frame_2_coordinates[pair[:, 1][p_index]]
                track_coordinate.append(p_coordinate)
                # update point2
                p = pair[:, 1][p_index]
                frame_2 += 1
            else:
                break
        # the trajs can not be longer than P, which is not so well
        if (len(track) > P-1):
            n_tracks_coordinate.append(track_coordinate)
    return n_tracks_coordinate


# if __name__ == '__main__':
#     # process_num = int(sys.argv[1])
#     # begin = int(sys.argv[2])
#     process_num = int(10)
#     begin = int(0)
#     P = 2
#     max_distance = 2
#     save_track = True
#     interp_factor = 0.1

    # for patch in range(begin, 30, process_num):
    #     locations = [np.loadtxt(
    #         '../Dataset/locations/locations_18/' + str(patch*800+frame) + '.txt') for frame in range(800)]
    #     loc_N = locations[0]
    #     loc_ave_num = np.mean([len(location) for location in locations])

    #     # Localization data are [intensity, y, x, frame number]
    #     frame_N = np.empty((len(loc_N), 2))
    #     frame_N[:, 0] = loc_N[:, 2]
    #     frame_N[:, 1] = loc_N[:, 1]
    #     MatOut = np.zeros((1181, 781))
    #     CNNF = [[] for _ in range(P+1)]
    #     CNNF_head = 0

    #     # Progress bar
    #     for frame in range(1, 800):
    #         loc_Np1 = locations[frame]

    #         frame_Np1 = np.empty((len(loc_Np1), 2))
    #         frame_Np1[:, 0] = loc_Np1[:, 2]
    #         frame_Np1[:, 1] = loc_Np1[:, 1]

    #         # # Pairing
    #         pairs = bipartite_graph_pairing(frame_N, frame_Np1, max_distance, savedata=False,
    #                                         dir='../Dataset/pairs/bpairs_18/'+str(patch*800+frame)+'.txt')
    #         # pairs = Hungarian_pairing(frame_N, frame_Np1, max_distance, savedata=False,
    #         #                   dir='../Dataset/pairs/bpairs_18/'+str(patch*800+frame)+'.txt')
    #         # pairs = semi_KNN_pairing(frame_N, frame_Np1, max_distance, savedata=False,
    #         #                  dir='../Dataset/pairs/test/'+str(patch*800+frame)+'.txt')
    #         # pairs = KNN_pairing(frame_N, frame_Np1, max_distance, savedata=False,
    #         #                     dir='../Dataset/pairs/kpairs_18/'+str(patch*800+frame)+'.txt')
    #         CNNF_head, CNNF, MatOut = CNNT(
    #             frame, pairs, frame_N, frame_Np1, P, interp_factor, CNNF, CNNF_head, MatOut)
    #         frame_N = frame_Np1
    #     result = MatOut.T
    #     io.savemat("result{}.mat".format(patch), {'MatOut': result})
    #     cv2.imshow('image:', MatOut.T)
    #     cv2.waitKey(0)
