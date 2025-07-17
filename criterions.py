import numpy as np

FREQUENCY = 1000
M = 100 # Масса манекена
G = 9.8071 # Ускорение свободного падения

def calculate_HIC(time, a, N=15):
    '''
    Критерий повреждения головы (HIC).
    Датчик 1
    a - np.array (3, M)
    time - время в секундах
    '''
    hic = 0
    m = 1000 * N // FREQUENCY
    hic_locs = []
    a = np.sqrt(np.sum(a ** 2, axis=0))
    for i in range(0, a.shape[0]-m, m):
        dt = time[i + m] - time[i]

        hic_loc = dt * (abs(sum([a[j] * (time[j+1] - time[j]) for j in range(i, i+m)]) / dt) ** 2.5)
        hic = max(hic_loc, hic)
        hic_locs.append(hic_loc)
    return hic, hic_locs
    

def calculate_N(time, a):
    '''
    time - время в секундах
    a - np.array (3, M)
    '''
    a = np.sqrt(np.sum(a ** 2, axis=0))
    g = a / G
    N = 0
    for i in range(0, a.shape[0]-1):
        n = (g[i+1] - g[i]) / (time[i+1] - time[i])
        N = max(N, n)
    return N

def calculate_Neck_Force(a1: np.array, a2: np.array, time, m=60):
    f1 = a1 * m
    f2 = a2 * m
    f = f1 + f2
    return max(f)

def calculate_CWVP(time, ax, ay, az):
    '''
    Расчет скорости стенки грудной клетки CWVP,
    датчик 4
    ax, ay, az - проекции ускорений датчиков 
    time -  время в секундах 
    '''
    v = [0, 0, 0]
    vs = []
    a_xyz = [ax, ay, az]
    for i in range(len(ax) - 1):
        v = np.array([v[j] + a_xyz[j][i] * (time[i+1] - time[i]) for j in range(3)])
        vs.append(np.sqrt(np.sum(v ** 2, axis=0)))
    return max(vs)

