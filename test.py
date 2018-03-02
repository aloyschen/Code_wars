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

def plot():
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

if __name__ == '__main__':
    plot()