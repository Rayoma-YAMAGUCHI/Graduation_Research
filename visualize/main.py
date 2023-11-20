import random 
import math
import numpy as np
import pyvista as pv  # PyVista (3D可視化)
import pandas as pd
import copy
import homcloud.interface as hc
import matplotlib.pyplot as plt
pv.start_xvfb()

def tsutsu(n):
    for i in range(n):
        theta = 2.0 * math.pi * random.random()
        radius = math.sqrt(random.uniform(0.25,1.0))
        p = [[radius * math.cos(theta), radius * math.sin(theta), np.random.rand()]]
        if i == 0:
            data = p
        else:
            data = np.append(data, p, axis=0)
    return data

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

# データファイルを扱いやすいように成形する関数
def get_pairs(DataFrame):
    df = copy.deepcopy(DataFrame)
    pairs = []
    pair = []
    paths = []
    for i in range(len(df)):
        s = df.iloc[i, 0]
        if s[0] == ';':
            l = [pair, paths]
            pairs.append(l)
            pair = []
            paths = []
            l = []
            f = ''
            for j in range(len(s)-2):
                if not s[j+2] == '  ':
                    f += s[j+2]
            g = f.split()
            pair.append(float(g[0]))
            pair.append(float(g[1]))
        else:
            path = []
            if s == '1':
                path.append(df.iloc[i, 1])
                path.append(df.iloc[i, 2])
            elif s == '-1':
                path.append(df.iloc[i, 2])
                path.append(df.iloc[i, 1])
            paths.append(path)
    l = [pair, paths]
    pairs.append(l)
    pairs.pop(0) 
  return pairs

# 頂点をインデックス表示から座標に変換する関数
def get_pairs_coordinate(pairs, points):
    c_pairs = copy.deepcopy(pairs)
    d = points
    for i in range(len(c_pairs)):
        for j in range(len(c_pairs[i][1])):
            p = c_pairs[i][1][j]
            for k in range(2):
                for l in range(len(d)):
                    if p[k] == d[l][0]:
                        p[k] = [d[l][1], d[l][2], d[l][3]]
                        break
    return c_pairs

# 特定の区間(b, d)の最適サイクルを返す関数
def nearest_pair(pairs, b):
    b_n = pairs[0][0][0]
    d_n = pairs[0][0][1]
    for i in range(len(pairs)-1):
        if math.fabs(b - b_n) > math.fabs(b - pairs[i][0][0]):
            b_n = pairs[i][0][0]
            d_n = pairs[i][0][1]
            pair = pairs[i][1]
    return (b_n, d_n, pair)

def make_image_optiperlp(pair, op_i2p, op_1):
    points = np.loadtxt(op_i2p)
    df = pd.read_csv(op_1, names=('birth/death', 'v0', 'v1'))
    pairs = get_pairs(df)
    c_pairs = get_pairs_coordinate(pairs, points)
    
    # optiperlpの特定のペアのpathの部分だけの情報を取得する
    line = nearest_pair(c_pairs, pair.birth)[2]
    mesh = pv.Line(line[0][0], line[0][1])
    for i in range(len(line)-1):
        mesh += pv.Line(line[i+1][0], line[i+1][1])
    return mesh

#データに対してPDを計算し解析対象のペアを得る

def make_image(pair):
    lifetime = pair.lifetime()
    lifetime_1_10 = lifetime/10
    lifetime_1_50 = lifetime/50
    lifetime_1_100 = lifetime/100
    stable_volume_1_10 = pair.stable_volume(lifetime_1_10)
    stable_volume_1_50 = pair.stable_volume(lifetime_1_50)
    stable_volume_1_100 = pair.stable_volume(lifetime_1_100)
    optimal_volume = pair.optimal_volume()
    return stable_volume_1_10.to_pyvista_boundary_mesh(), stable_volume_1_50.to_pyvista_boundary_mesh(), stable_volume_1_100.to_pyvista_boundary_mesh(), optimal_volume.to_pyvista_boundary_mesh()
data_tsutsu = p

def show_via_pyvista(data, pair):
  mesh_sv_1_10, mesh_sv_1_50, mesh_sv_1_100, mesh_ov = make_image(pair)
  pl_t = pv.Plotter()
  pl_t.add_mesh(pv.PointSet(data), point_size=2)
  pl_t.add_mesh(mesh_op, color="black", line_width=5)
  #pl_t.add_mesh(mesh_ov, color="yellow", line_width=2)
  #pl_t.add_mesh(mesh_sv_1_10, color="blue", line_width=2)
  #pl_t.add_mesh(mesh_sv_1_50, color="red", line_width=2)
  #pl_t.add_mesh(mesh_sv_1_100, color="white", line_width=2)
  pl_t.show()
