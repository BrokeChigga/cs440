import numpy as np
from util import save_obj, load_obj

Q = {}
N = {}
NE = 10
def QInit(ne = 10, board_x_d = 12, board_y_d = 12, paddle_d = 12):
    global NE
    NE = ne
    for xp in range(0, board_x_d):
        for yp in range(0, board_y_d):
            for xvel in [-1, 1]:
                for yvel in [-1, 0, 1]:
                    for pp in range(0, paddle_d):
                        for action in [-1, 0, 1]:
                            Q[(xp, yp, xvel, yvel, pp, 0, action)] = 0
                            N[(xp, yp, xvel, yvel, pp, 0, action)] = 0
    Q[(0, 0, 0, 0, 0, 1, 0)] = 0
    N[(0, 0, 0, 0, 0, 1, 0)] = 0
    Q[(-1, 0, 0, 0, 0, 0, 0)] = 0
    N[(-1, 0, 0, 0, 0, 0, 0)] = 0

def QInitFromFile(filename, ne):
    global NE, Q, N
    NE = ne
    Q = load_obj(filename + "_q.tbl")
    N = load_obj(filename + "_n.tbl")

def QSaveToFile(filename):
    save_obj(Q, filename + "_q.tbl")
    save_obj(N, filename + "_n.tbl")

def getQ(s, a):
    (xp, yp, xvel, yvel, pp, lose) = s
    if lose == 1:
        return Q[(0, 0, 0, 0, 0, 1, 0)]
    elif xp < 0:
        return Q[(-1, 0, 0, 0, 0, 0, 0)]
    else:
        return Q[s + (a,)]

def setQ(s, a, val):
    (xp, yp, xvel, yvel, pp, lose) = s
    if lose == 1:
        Q[(0, 0, 0, 0, 0, 1, 0)] = val
    elif xp < 0:
        Q[(-1, 0, 0, 0, 0, 0, 0)] = val
    else:
        Q[s + (a,)] = val

def getN(s, a):
    (xp, yp, xvel, yvel, pp, lose) = s
    if lose == 1:
        return N[(0, 0, 0, 0, 0, 1, 0)]
    elif xp < 0:
        return N[(-1, 0, 0, 0, 0, 0, 0)]
    else:
        return N[s + (a,)]

def inc_N(s, a):
    (xp, yp, xvel, yvel, pp, lose) = s
    if lose == 1:
        N[(0, 0, 0, 0, 0, 1, 0)] += 1
    elif xp < 0:
        N[(-1, 0, 0, 0, 0, 0, 0)] += 1
    else:
        N[s + (a,)] += 1

def expl_policy(s, a):
    if getN(s, a) < NE:
        return 10 + np.random.rand()
    else:
        return getQ(s, a)