# to get pair of PD which has the logest lifespan using homcloud

import homcloud.interface as hc #Homcloud
import copy
import math
import sympy
from sympy.geometry import *
import time
import pandas as pd
# import sys
# import os

#ライフスパンの長さを比較する（一番大きいのを得る）
def the_longest_lifespan_pair(pd1):
    pair = 0
    for i in range(len(pd1.births)):
        life = pd1.deaths[i] - pd1.births[i]
        if pair < life:
            pair = life
            b = pd1.births[i]
            d = pd1.deaths[i]
        else:
            continue
    return pd1.nearest_pair_to(b, d)

#具体的なペアを取得する
def get_pair_with_PD(pointcloud):
    hc.PDList.from_alpha_filtration(pointcloud, save_to="pointcloud.pdgm",save_boundary_map=True)
    pdlist = hc.PDList("pointcloud.pdgm")
    pd1 = pdlist.dth_diagram(1)
    pair = the_longest_lifespan_pair(pd1)
    return pair

# 3次元データを2次元に変換する（z軸のデータを消す）
def three_to_two(p):
    newp = [[(p[i][0][0], p[i][0][1]), (p[i][1][0], p[i][1][1])] for i in range(len(p))]
    return newp

#サイクルの長さを取得する
def length(path):
    length = 0
    for i in range(len(path)):
        leng = math.dist(path[i][0], path[i][1])
        length += leng
    return length

#サイクルを構成する単体を並び順に整列する
def n_order(boundary):
    s = copy.deepcopy(boundary)
    order = [s[0]]
    s.remove(s[0])
    l = len(s)
    for i in range(len(s)):
        for j in range(len(s)):
            try:
                if order[i][0] in s[j] or order[i][1] in s[j]:
                    order.append(s[j])
                    s.remove(s[j])
                    break
            except:
                if len(order) > l/2:
                    return order
                else:
                    return None
    return order

#サイクルの面積を計算する
def area(boundary):
    new_order = n_order(boundary)
    if new_order == None:
        return math.nan
    path = copy.deepcopy(new_order)
    b = []
    if path[0][0] in path[1]:
        b.append(path[0][0])
    else:
        b.append(path[0][1])
    for i in range(len(path)-1):
        for j in range(2):
            if path[i+1][j] not in b:
                b.append(path[i+1][j])
    #print(b)
    polygon = Polygon( *b )
    area = math.fabs(polygon.area)
    return area


def get_sv(pair, r):
    n = pair.lifetime()/r
    start = time.time()
    stable_volume = pair.stable_volume(n)
    end = time.time()
    path = three_to_two(stable_volume.boundary())
    q = len(stable_volume.simplices())
    l = length(path)
    s = area(path)
    t = end-start
    return [q, l, s, t]

def get_ov(pair):
    start = time.time()
    optimal_volume = pair.optimal_volume()
    end = time.time()
    path = three_to_two(optimal_volume.boundary())
    q = len(optimal_volume.simplices())
    l = length(path)
    s = area(path)
    t = end-start
    return [q, l, s, t]



def get_op1(pair):
    start = time.time()
    optimal_1_cycle = pair.optimal_1_cycle()
    end = time.time()
    path = three_to_two(optimal_1_cycle.path())
    l = length(path)
    s = area(path)
    t = end-start
    return [l, s, t]

def main(data):
    pair = get_pair_with_PD(data)
    sv5 = get_sv(pair, 5)
    sv10 = get_sv(pair, 10)
    sv50 = get_sv(pair, 50)
    sv100 = get_sv(pair, 100)
    ov = get_ov(pair)
    #op1 = get_op1(pair)
    return [sv5[0],sv10[0],sv50[0],sv100[0],ov[0],sv5[1],sv10[1],sv50[1],sv100[1],ov[1],sv5[2],sv10[2],sv50[2],sv100[2],ov[2],sv5[3],sv10[3],sv50[3],sv100[3],ov[3]]
