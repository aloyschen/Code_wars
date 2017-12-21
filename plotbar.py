# coding:utf-8
# 该脚本用来统计数据的分布，并画出相应的柱状图
# Author: gaochen3
# Date: 2017.12.20

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc')

def get_median(data):
    """
    针对奇数和偶数的列表情况获取中位数
    Parameters
    ----------
        data: 包含数据的列表
    Return
    ------
        列表中数据的中位数
    """
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2


def plot_data(data):
    """
    该函数求数据的最大值，然后均匀切分成10份，分别统计在每个区间的数量
    Parameters
    ----------
        data: 主播对应的特征数据
    Returns
    -------
        people: 每个数据区间内的人数
        data_range: 数据区间
    """
    data_range = []
    people = []
    feature = []
    for uid in data:
        feature.append(float(data[uid]))
    max_data = max(feature)
    separation = (int(str(max_data)[0]) + 1) * len(str(max_data))
    print('separation: ', separation)
    median = get_median(feature)
    print("max_data: {0} median: {1}".format(max_data, median))
    # separation = 0.1
    for iter in range(11):
        data_range.append(round(separation * iter, 1))
    for iter in range(10):
        count = 0
        for element in feature:
            if element > data_range[iter] and element < data_range[iter + 1]:
                count += 1
        people.append(count)
    return data_range, people


def read_file(data_path):
    """
    该函数读取文件中的内容存储到列表中
    Parameters
    ----------
        data_path: 文件路径
    Returns
    -------
        data: 每个主播uid对应的数据值字典
    """
    data = {}
    for line in open(data_path, encoding = 'utf-8').readlines():
        line = line.strip()
        tmp = line.split('\t')
        if len(tmp) != 2:
            print("数据格式错误")
            continue
        data[tmp[0]] = tmp[1]
    return data



def compute_ratio(people_path, feature_path):
    """
    计算每个主播的对应的特征数据的比率
    Parameters
    ----------
        people_path: 每个主播的观看人数
        feature_path: 每个主播对应的特征数据
    Returns
    -------
        uid: 每个主播的uid
        ratio: 每个主播特征数据的比率
    """
    ratio = {}
    watch_data = read_file(people_path)
    feature_data = read_file(feature_path)
    for uid in feature_data:
        if uid in watch_data.keys():
            ratio[uid] = float(feature_data[uid]) / float(watch_data[uid])
    return ratio


def plot_bar(people_path, feature_path, figure, time):
    """
    绘制不同时间点的数据分布直方图
    Parameters
    ----------
        people_path: 观看人数的数据文件
        feature_path: 特征值的数据文件
        figure: 绘制直方图的序号
        time: 对应的时间点
    """
    ratio = compute_ratio(people_path + str(time) + '.txt', feature_path + str(time) + '.txt')
    data_range, people = plot_data(ratio)
    width = 0.9
    ind = range(len(people))
    print("people: {0} data range {1}".format(people, data_range))
    plt.subplot(131 + figure)
    plt.bar(ind, people, width)
    plt.ylabel(u'对应主播人数', fontproperties = font)
    plt.xlabel(u'评论率(总的观看人数/观看人数)', fontproperties = font)
    plt.title(u'评论率分布({0}点)'.format(time), fontproperties = font)
    plt.xticks(ind, ('[{0},{1}]'.format(data_range[iter], data_range[iter + 1]) for iter in range(len(data_range) - 1)))


def plot_all(feature_path, people_path, total_time):
    """
    将不同时间点的直方图绘制到一个图片中
    Parameters
    ----------
        feature_path: 特征数据文件
        people_path: 观看人数数据文件
        total_time: 所有时间列表
    """
    figure = 0
    for element in total_time:
        plot_bar(people_path, feature_path, figure, element)
        figure += 1
    plt.show()


def plot(feature_path, total_time):
    """
    绘制单独特征的数据直方图，包括所有时间点的数据
    Parameters
    ----------
        feature_path: 特征值的数据文件
        total_time: 所有时间列表
    """
    figure = 0
    for element in total_time:
        plot_one(feature_path, figure,element)
        figure += 1
    plt.show()

def plot_one(feature_path, figure, time):
    """
    绘制单个特征的直方图，一个时间点的数据
    Parameters
    ----------
        feature_path: 特征数据文件
        figure: 绘制直方图的序号
        time: 直方图对应的时间点
    """
    data = read_file(feature_path + str(time) + '.txt')
    data_range, people = plot_data(data)
    width = 0.9
    ind = range(len(people))
    print("people: {0} data range {1}".format(people, data_range))
    plt.subplot(131 + figure)
    plt.bar(ind, people, width)
    plt.ylabel(u'对应主播人数', fontproperties = font)
    plt.xlabel(u'消费金额(单位：万）', fontproperties = font)
    plt.title(u'消费金额分布({0}点)'.format(time), fontproperties = font)
    plt.xticks(ind, ('[{0},{1}]'.format(int(data_range[iter] / 10000), int(data_range[iter + 1] / 10000))  for iter in range(len(data_range) - 1)))



if __name__ == '__main__':
    total_time = [5, 13, 22]
    plot_all('./uid_comment_', './uid_watch_', total_time)
    # plot('./uid_giftamount_', total_time)
