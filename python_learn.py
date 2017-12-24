import collections
from collections import namedtuple
import os, sys
import numpy as np
import bisect

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
    suit_value = dict(黑桃 = 3, 红桃 = 2, 方块 = 1, 梅花 = 0)
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

def bitsect(bisect_fn):
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


if __name__ == "__main__":
    # deck = FrenchDeck()
    # print(len(deck), "\neleven card: ", deck[36])
    # for card in sorted(deck, key = high_card):
    #     print(card)
    # tuple_unpack()
    bitsect(bisect.bisect)
    # Tshirts()