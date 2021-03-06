import collections
from collections import namedtuple
import os, sys
import array
import numpy as np
import random
import bisect
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt

card = collections.namedtuple('card', ['rank', 'suit'])


class FrenchDeck:
    """
    构建一个扑克牌类，定义初始化方法，获取元素方法，以及获取元素长度的方法
    学习特殊方法的使用，如__init__, __getitem__, __len__等
    """
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = ['方块', '红桃', '黑桃', '梅花']

    def __init__(self):
        # 这里利用列表推导式生成笛卡尔积组合
        self._cards = [card(rank, suit) for rank in self.ranks for suit in self.suits]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]


def high_card(card):
    """
    该函数是对纸牌排序的分数值计算
    Parameters
    ----------
        card: 输入的纸牌
    Returns
    -------
        每张牌的得分数
    """
    suit_value = dict(黑桃=3, 红桃=2, 方块=1, 梅花=0)
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_value) + suit_value[card.suit]


def tuple_unpack():
    """
    tuple的意义和Collections.namedtuple的使用
    学习使用python的format格式控制
    """
    location = (23, -100)
    # tuple中数据的位置可以当做字段，这样我们就可以方便对tuple进行拆包，只要元素一一对应
    x, y = location
    print("x = ", x, "y = ", y)
    fillname, _ = os.path.split("/usr/gaochen3/python/test.txt")
    print(fillname)
    person = namedtuple("person", "name, age, gender, city, university")
    you = person("no", 23, "man", "beijing", "qinghua")
    print(you.name)
    metro_areas = [('Tokyo', 'JP', 36.933, (35.689722, 139.61877)),
                   ('Mexico City', 'MX', 20.142, (29.433333, -19.133333))]
    print('{:15} | {:^9} | {:^9} '.format('', 'lat.', 'long.'))
    fmt = '{:15} | {:^9.4f} | {:^9.4f}'
    for city, cc, pop, (latitude, longitude) in metro_areas:
        if longitude < 0:
            print(fmt.format(city, latitude, longitude))


def Tshirts():
    """
    该函数利用列表推导式可以很容易实现两层循环
    Return
    ------
        返回每种颜色和大小组合的T-shirt
    """
    colors = ['red', 'blue', 'black']
    sizes = ['M', 'L', 'XL', 'XXL']
    # 使用列表推导式，先创建一个列表
    Tshirts = [(color, size) for color in colors for size in sizes]
    for Tshirt in Tshirts:
        print("Tshirt: ", Tshirt)
    # 使用生成器表达式代替列表推导式，可以节省内存开销, 逐个产生元素
    for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
        print(tshirt)


def bitsect_demo(bisect_fn):
    """
    该函数利用二分查找搜索列表中指定的元素
    Parameters
    ----------
        bisect_fn: 使用的二分查找函数
    """
    needles = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]
    haystack = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
    row_format = '{0:2d} @ {1:2d}     {2} {0:<2d}'
    print('DEMO: ', bisect_fn.__name__)
    print('haystack -> ', ' '.join('%2d' % hay for hay in haystack))
    for needle in reversed(needles):
        position = bisect_fn(haystack, needle)
        offset = position * '  |'
        print(row_format.format(needle, position, offset))

def bisect_insort():
    """
    该函数利用bisect向有序列表中插入元素
    Return
    ------
        None
    """
    my_list = []
    for i in range(10):
        new_item = random.randrange(10)
        bisect.insort(my_list, new_item)
        print('%2d -> ' % new_item, my_list)


def grade_find(score, breakPoints = None, grades='FDCBA'):
    """
    该函数根据分数进行分段，找到对应的成绩
    Parameters
    ----------
        score: 分数
        breakPoints: 分数上下限
    """
    if breakPoints is None:
        breakPoints = [60, 70, 80, 90, 100]
    for grade in score:
        i = bisect.bisect(breakPoints, grade)
        print(grades[i] + " ")



def doule_arr():
    """
    该函数利用array创建一个1000万数据的数组，然后存储到本地文件中，再读取出来
    Parameters
    ----------
        None
    Return:
        None
    """
    float_arr = array.array('d', (random.random() for i in range(10 ** 7)))
    fp = open('float.bin', 'wb')
    float_arr.tofile(fp)
    fp.close()
    float_arr_read = array.array('d')
    fp_read = open('float.bin', 'rb')
    float_arr_read.fromfile(fp_read, 10 ** 7)
    fp_read.close()
    if float_arr_read == float_arr:
        print('this is same')



def memory_test():
    """
    该函数是利用内存视图共享数据，不复制的情况下使用同一块内存内容
    Parameters
    ----------
        None
    Return:
    ------
        None
    """
    array_memory = array.array('h', [-2, 6, 1, 0, 7])
    octets = bytes(array_memory)
    print(octets)


class BingoCage:
    """
    定义一个类的时候，可以使用__call__方法使其成为可调用对象
    """
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)
    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            return LookupError('pick from empty BingoCage')
    def __call__(self):
        return self.pick()


def pandas_loc():
    """
    该函数是使用pandas的loc和iloc的区别，如果是使用行号作为index最好使用iloc，而如果使用其他的字母作为index则需要使用loc遍历
    Parameters
    ----------
        None
    Returns
    -------
        None
    """
    data = np.random.randn(3, 3)
    a = pd.DataFrame(data, index=['A', 'B', 'C'], columns=['a', 'b', 'c'])
    b = pd.DataFrame(data, index=['A', 'B', 'C'], columns=['d', 'c', 'b'])
    temp = pd.Series(None, index=[40, 41, 42, 1, 2, 3])
    print("iloc: \n {} \n loc: \n {}".format(temp.iloc[: 3], temp.loc[1: 3]))


def pandas_join():
    """
    该函数是使用pandas做表的join操作
    Parameters
    ----------
        None
    Returns
    -------
        None
    """

    data1 = {"data1" : [1, 2, 3, 4], "key1" : ['a', 'b', 'c', 'd']}
    data2 = {"data2" : [5, 6, 7], "key2" : ['a', 'c', 'd']}
    frame1 = pd.DataFrame(data1)
    frame2 = pd.DataFrame(data2)
    print(pd.merge(frame1, frame2, how = "outer", right_on = "key2", left_on = "key1"))
    print("-----------")
    data3 = pd.DataFrame(np.arange(6).reshape(3, 2), index = ['a', 'b', 'c'], columns = ['key1', 'key2'])
    data4 = pd.DataFrame(np.arange(4).reshape(2, 2), index = ['c', 'e'], columns = ['key1', 'key2'])
    print(pd.concat([data3, data4]))
    print('-----------')
    data5 = pd.DataFrame(np.arange(6).reshape(2, 3), columns = pd.Index(['a', 'b', 'c'], name = 'columns'), index = pd.Index(['one', 'two'], name = 'index'))
    print(data5.stack())
    a = np.arange(10)
    print(pd.cut(a, 4))
    data6 = pd.DataFrame(np.random.randn(100, 3), columns = ['a', 'b', 'c'])
    data6.plot(title = 'test')
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
    df = df.cumsum()
    plt.figure()
    df.plot()
    plt.show()

if __name__ == "__main__":
    # deck = FrenchDeck()
    # print(len(deck), "\neleven card: ", deck[36])
    # for card in sorted(deck, key = high_card):
    #     print(card)
    # tuple_unpack()
    # bitsect(bisect.bisect)
    # Tshirts()
    # grade_find([22, 78])
    # bisect_insort()
    # doule_arr()
    # mem = memory_test
    # __doc__可以打印函数的返回信息
    # bingo = BingoCage(range(3))
    # print(bingo.pick())
    # pandas_loc()
    pandas_join()