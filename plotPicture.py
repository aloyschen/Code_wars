import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc')


def autoLabel(rect):
    """
    该函数用来在柱状图的上显示具体数值
    Parameters
    ----------
        rect: 直方图函数返回的矩形
    Returns
    -------
        None
    """
    for rect in rect:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2. - 0.48, 1.015 * height, '%s' % float(height))

def plot_watchTime():
    """
    该函数根据用户的观看时间统计画出分布直方图
    Parameters
    ----------
        None
    Return
    ------
        None
    """
    watchTime, peopleNumber = [], []
    for line in open('./userWatchTime', encoding = 'utf-8'):
        line = line.strip().split(',')
        if len(line) != 2:
            continue
        watchTime.append(int(line[0]))
        peopleNumber.append(int(int(line[1]) / 10000))
    rect = plt.bar(watchTime, peopleNumber, width = 0.9, fc = 'r')
    autoLabel(rect)
    plt.xlabel(u'用户观看时长(单位：秒)', fontproperties = font)
    plt.ylabel(u'用户数量(单位：百万)', fontproperties = font)
    plt.title(u'用户观看时长在 0-10 秒内分布直方图', fontproperties = font)
    plt.xticks(range(11))
    plt.show()


def plot_increment():
    """
    该函数是统计增量数据画出双柱状图
    Parameters
    ----------
        None
    Returns
    -------
        None
    """
    data1, data2 = dict(), dict()
    for line in open('./increment_little', encoding = 'utf-8'):
        line = line.strip().split(',')
        data1[line[0]] = [line[1], line[2]]
    for line in open('./increment_large', encoding = 'utf-8'):
        line = line.strip().split(',')
        data2[line[0]] = [line[1], line[2]]
    x1 = range(3)
    x2 = range(4)
    relation1 = [int(data1[key][0]) / 10000 for key in data1.keys()]
    total1 = [int(data1[key][1]) / 10000 for key in data1.keys()]
    relation2 = [int(data2[key][0]) / 10000 for key in data2.keys()]
    total2 = [int(data2[key][1]) / 10000 for key in data2.keys()]
    # plt.subplot(121)
    rect1 = plt.bar(x1, relation1, width = 0.3)
    rect2 = plt.bar(x1, total1, bottom = relation1, width = 0.3)
    plt.xlabel(u'用户行为', fontproperties = font)
    plt.ylabel(u'用户人数(单位：万)', fontproperties = font)
    plt.title(u'各种行为非关注关系的增量统计', fontproperties = font)
    plt.xticks(x1, data1.keys(), fontproperties = font)
    # plt.subplot(122)
    # rect3 = plt.bar(x2, relation2, width = 0.5)
    # rect4 = plt.bar(x2, total2, bottom = relation2, width = 0.5)
    # plt.xlabel(u'用户行为', fontproperties = font)
    # plt.ylabel(u'用户人数(单位：万)', fontproperties = font)
    # plt.title(u'各种行为非关注关系的增量统计', fontproperties = font)
    # plt.xticks(x2, data2.keys(), fontproperties = font)
    plt.legend((u'满足关注关系人数', u'非关注关系的增量人数'), prop = font)
    plt.show()

if __name__ == '__main__':
    plot_increment()