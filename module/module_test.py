import module_cert
import module_ph
import numpy as np
import pandas as pd
import random 
import math
import time

def randomincircle(n):
    for i in range(n):
        theta = 2.0 * math.pi * random.random()
        radius = math.sqrt(random.uniform(0.25,1.0))
        p = [[radius * math.cos(theta), radius * math.sin(theta)]]
        if i == 0:
            data = p
        else:
            data = np.append(data, p, axis=0)
    return data

def pinched_circle(n):
    for i in range(n):
        theta = 1.8 * math.pi * random.random()
        radius = math.sqrt(random.uniform(0.5,1.0))
        p = [[-radius * math.cos(theta), -radius * math.sin(theta)]]
        if i == 0:
            data = p
        else:
            if i <= n*0.8:
                data = np.append(data, p, axis=0)
            else:
                theta_s = 1.25*math.pi * random.random()
                radius_s = 0.5 * math.sqrt(random.uniform(0.25,1.0))
                x = radius_s * math.cos(theta_s)
                y = radius_s * math.sin(theta_s)
                p = [[-0.85+0.5*x - 0.86*y, 0.3 + 0.86*x +0.5*y]]
                data = np.append(data, p, axis=0)
    return data

#number of points = n
#number of trial = m

def test_pinched_circle(n,m):
    lis_t = []
    for i in range(m):
        data = pinched_circle(n)
        data_3 = np.column_stack((data, 0.00005*np.random.rand(data.shape[0],1)))
        l = module_ph.main(data_3)
        lis_t += [l]
    df = pd.DataFrame(lis_t,columns=['L-sv(10%)', 'L-sv(1%)', 'L-ov', 'L-op1c', 'S-sv(10%)', 'S-sv(1%)', 'S-ov', 'S-op1c', 'T-sv(10%)', 'T-sv(1%)', 'T-ov', 'T-op1c'])
    return df

def test_circle(n,m):
    lis_t = []
    for i in range(m):
        data = randomincircle(n)
        data_3 = np.column_stack((data, 0.00005*np.random.rand(data.shape[0],1)))
        l = module_ph.main(data_3)
        lis_t += [l]
    df = pd.DataFrame(lis_t,columns=['L-sv(10%)', 'L-sv(1%)', 'L-ov', 'L-op1c', 'S-sv(10%)', 'S-sv(1%)', 'S-ov', 'S-op1c', 'T-sv(10%)', 'T-sv(1%)', 'T-ov', 'T-op1c'])
    return df

if __name__ == '__main__':
    n_i = input('点の数を入力>>')
    m_i = input('試行回数の入力>>')
    arg = input('データを選択>ドーナツは「a」>ピンチドは「b」>>')
    n = int(n_i)
    m = int(m_i)
    if arg == "a":
        start = time.time()
        df = test_circle(n, m)
        end = time.time()
    elif arg == "b":
        start = time.time()
        df = test_pinched_circle(n, m)
        end = time.time()
    else:
        print("入力が正しくありません")
    t = end-start
    df.to_csv("result.csv")
    print("計算時間", t)
