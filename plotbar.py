# coding:utf-8
# 该脚本用来统计数据的分布，并画出相应的柱状图
# Author: gaochen3
# Date: 2017.12.20

import numpy as np
import matplotlib.pyplot as plt

def min_max(uid, data):
    """
    该函数求数据的最大值和最小值，然后均匀切分成10份，分别统计在每个区间的数量
    Parameters
    ----------
        uid: 主播的uid
        data:
    :return:
    """
    data_range = []
    people = []

