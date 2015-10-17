from copy import copy, deepcopy
import random
import cv2
import numpy as np
import tree
from tree import Node, expand_tree
import time

def parse(R,C,A,L):
    targets = []
    winds = [[[] for r in range(R)] for a in range(A)]
    with open("final_round.in","r") as f:
        for i in range(3):
            f.readline()
        for l in range(L):
            target = f.readline().split()
            targets.append((int(target[0]),int(target[1])))
        for a in range(A):
            for r in range(R):
                wind = f.readline().split()
                winds[a][r] = [(int(wind[2*c]),int(wind[2*c+1])) for c in range(C)]
    return targets, winds

def get_allowed_pos():
    allowed_pos = [[[True for c in range(C)] for r in range(R)] for a in range(A)]
    removed = 0
    for a in range(A):
        for r in range(R):
            for c in range(C):
                next_r = r+winds[a][r][c][0]
                if next_r < 0 or next_r >= R:
                    allowed_pos[a][r][c] = False
                    removed += 1
    # print(removed)
    for k in range(7):
        removed = 0
        for a in range(A):
            for r in range(R):
                for c in range(C):
                    if allowed_pos[a][r][c]:
                        try:
                            next_r = r+winds[a][r][c][0]
                            next_c = (c+winds[a][r][c][1])%C
                            pos1 = allowed_pos[a][next_r][next_c]
                            pos2 = allowed_pos[max(0,a-1)][next_r][next_c]
                            pos3 = allowed_pos[min(A-1,a+1)][next_r][next_c]
                            if not(pos1) and not(pos2) and not(pos3):
                                allowed_pos[a][r][c] = False
                                removed += 1
                        except:
                            print(a,next_r,next_c,winds[a][r][c][0],winds[a][r][c][1])
                            raise Exception
        # print(removed)
    return allowed_pos

R = 75
C = 300
A = 8
L = 2250
V = 7
B = 53
T = 400
# targets = liste de L couples
# winds = matrice3D de couples
targets, winds = parse(R,C,A,L)
allowed_pos = get_allowed_pos()

def get_score(sky):
    score = 0
    for target in targets:
        if sky[target[0]][target[1]]>0:
            score += 1
    return score

def get_temp_score(node):
    node.apply_action()
    score = get_score(node.sky)
    node.remove_action()
    return score

def get_total_coverage(sky):
    return sum(map(sum,sky))

def get_temp_coverage(node):
    node.apply_action()
    coverage = get_total_coverage(node.sky)
    node.remove_action()
    return coverage

def get_lost(balloons):
    return B-len([1 for balloon in balloons if 0<=balloon[0]<R])

def save_result_in_file(actions, filename):
    with open(filename,"w") as f:
        for action in actions:
            f.write(' '.join(map(str,action))+'\n')

def run_algorithm():
    balloons = [(24, 167, -1) for b in range(B)] # liste de B triplets
    sky = [[0 for c in range(C)] for r in range(R)]
    sky[24][167] = B
    actions = [] # liste de T tours contenant une liste de B actions (-1,0,1)
    current_node = Node(balloons, sky, [(24, 167, -1), (24, 167, -1), (24, 167, -1), None])
    current_score = 0
    depth = 1
    for current_T in range(T):
        action = []
        for current_B in range(B):
            expand_tree(current_node, current_B, depth, expand_function, heuristic)
            print(current_node.balloons[current_B])
            # time.sleep(1)
            current_node = max(current_node.children, key=lambda x: x.heuristic_value)
            action.append(current_node.prev_action[3])
            current_node.apply_action()
            current_node.prev_action[0]=current_node.balloons[current_B%B]
            current_node.prev_action[2]=current_node.balloons[current_B%B]
            current_node.prev_action[3]=None
            print(get_score(current_node.sky))
            time.sleep(1)
        actions.append(action)
        tour_score = get_score(current_node.sky)
        current_score += tour_score
        if current_T%1 == 0:
            print("tour %i: %i"%(current_T, tour_score))
    # print("lost: %i"%get_lost(current_node.balloons))
    save_result_in_file(actions, "lolilol.txt")
    return current_score

def heuristic(node):
    # optimiser nombre de cibles couvertes, couverture geographique de facon generale
    return (get_temp_score(node), get_temp_coverage(node), random.random())
    # return random.random()


def expand_function(root_node, current_B):
    # 3 possibilites, enlever la descente si 0 ou 1, enlever si le vent va faire sortir le ballon
    # par defaut, renvoyer 0
    children = []
    start_pos = root_node.prev_action[0]
    prev_pos = root_node.prev_action[2]
    if prev_pos[2] > 0 and allowed_pos[prev_pos[2]-1][prev_pos[0]][prev_pos[1]]:
        new_pos = get_new_position(prev_pos, -1)
        new_balloons = copy(root_node.balloons)
        new_balloons[current_B] = new_pos
        children.append(Node(new_balloons, root_node.sky, [start_pos, prev_pos, new_pos, -1]))
    if prev_pos[2] < A-1 and allowed_pos[prev_pos[2]+1][prev_pos[0]][prev_pos[1]]:
        new_pos = get_new_position(prev_pos, 1)
        new_balloons = copy(root_node.balloons)
        new_balloons[current_B] = new_pos
        children.append(Node(new_balloons, root_node.sky, [start_pos, prev_pos, new_pos, 1]))
    if prev_pos[2] > -1 and allowed_pos[prev_pos[2]][prev_pos[0]][prev_pos[1]]:
        new_pos = get_new_position(prev_pos, 0)
        new_balloons = copy(root_node.balloons)
        new_balloons[current_B] = new_pos
        children.append(Node(new_balloons, root_node.sky, [start_pos, prev_pos, new_pos, 0]))
    return children

# def get_new_balloons(balloons, current_B, pos, change):
#     new_balloons = copy(balloons)
#     new_balloons[current_B] = get_new_position(pos, change)
#     return new_balloons

def get_new_position(pos, change):
    if 0<=pos[0]<R:
        wind = winds[pos[2]+change][pos[0]][pos[1]]
        new_pos = (pos[0]+wind[0], (pos[1]+wind[1])%C, pos[2]+change)
        return new_pos
    return pos

# def get_new_sky(sky, prev_pos, new_pos):
#     return sky
#     new_sky = deepcopy(sky)
#     if 0<=prev_pos[0]<R:
#         for i in range(-V, V+1):
#             for j in range(-V, V+1):
#                 if i*i+j*j<=V*V and 0 <= prev_pos[0]+i < R:
#                     new_sky[prev_pos[0]+i][(prev_pos[1]+j)%C] -= 1
#     if 0<=new_pos[0]<R:
#         for i in range(-V, V+1):
#             for j in range(-V, V+1):
#                 if i*i+j*j<=V*V and 0 <= new_pos[0]+i < R:
#                     new_sky[new_pos[0]+i][(new_pos[1]+j)%C] += 1
#     return new_sky

if __name__ == "__main__":
    print(run_algorithm())
    # count = 0
    # for r in range(R):
    #     for c in range(C):
    #         a = 0
    #         wind = False
    #         a_min = 0
    #         while a<A:
    #             if not(wind) and not(allowed_pos[a][r][c]) and a>a_min:
    #                 count+=1
    #             if not(allowed_pos[a][r][c]):
    #                 wind = False
    #                 a_min = a
    #             if winds[a][r][c]!=(0,0):
    #                 wind = True
    #             a+=1
    #     if not(wind) and a_min<A-1:
    #         count+=1
    # print(count)
    # for a in range(A):
    #     img = np.asarray(map(lambda row: map(lambda col: [255,255,255] if col else [0,0,0], row),allowed_pos[a])).astype(np.uint8)
    #     print(img[0,0])
    #     cv2.imshow("loon",img)
    #     cv2.waitKey(1000)
    #     cv2.destroyAllWindows()
    # mean = 0
    # for i in range(10):
    #     score = run_algorithm()
    #     mean += score
    #     print(score)
    # print(mean/10)

