import module_cert
import module_ph
import numpy as np
import pandas as pd
import random 
import math

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

def test_circle(n, m):
    data = randomincircle(n)
    data_3 = np.column_stack((data, 0.00005*np.random.rand(data.shape[0],1)))
    df = module_ph.main(data_3)
    for i in range(m-1):
        data = randomincircle(n)
        data_3 = np.column_stack((data, 0.00005*np.random.rand(data.shape[0],1)))
        df_i = module_ph.main(data_3)
        df = pd.concat([df, df_i], axis = 1)
    return df

def test_100(n):
    data = np.random.rand(n, 2)
    data_3 = np.column_stack((data, 0.00005*np.random.rand(data.shape[0],1)))
    df = module_ph.main(data_3)
    for i in range(99):
        data = np.random.rand(50, 2)
        data_3 = np.column_stack((data, 0.00005*np.random.rand(data.shape[0],1)))
        df_i = module_ph.main(data_3)
        df = pd.concat([df, df_i], axis = 1)
    return df

#number of points = n
#number of trial = m
def test(n, m):
    if m <= 100:
        data = np.random.rand(n, 2)
        data_3 = np.column_stack((data, 0.00005*np.random.rand(data.shape[0],1)))
        df = module_ph.main(data_3)
        for i in range(m-1):
            data = np.random.rand(50, 2)
            data_3 = np.column_stack((data, 0.00005*np.random.rand(data.shape[0],1)))
            df_i = module_ph.main(data_3)
            df = pd.concat([df, df_i], axis = 1)
        return df
    else:
        r = m / 100
        i = int(r)
        df = test_100(n)
        for i in range(i-1):
            df_i = test_100(n)
            df = pd.concat([df, df_i], axis = 1)
        return df

def cert(df, stri, a, b, l):
    if stri == "L":
        df_len = df.iloc[[4,5,6,7], :]
        leng = df_len.T
        return module_cert.main(leng[[a]], leng[[b]], l)
    elif stri == "S":
        df_s = df.iloc[[8,9,10,11], :]
        s = df_s.T
        return module_cert.main(s[[a]], s[[b]], l)
    elif stri == "T":
        df_time = df.iloc[[12,13,14,15], :]
        time = df_time.T
        return module_cert.main(time[[a]], time[[b]], l)
    else:
        return print("argument is not appropriate")
