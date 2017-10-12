bin = '01'
oct = '01234567'
dec = '0123456789'
hex = '0123456789abcdef'
allow = 'abcdefghijklmnopqrstuvwxyz'
allup = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphanum = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
import numpy as np
from CodeTest import Test

def convert(input, source, target):
    """
    该函数用于不同进制之间的转换
    """
    base_in = len(source)
    base_out = len(target)
    acc = 0
    out = ''
    for d in input:
        acc *= base_in
        print(source.index(d))
        acc += source.index(d)
    while acc != 0:
        d = target[acc % base_out]
        acc = acc/base_out
        out = d + out
    return out if out else target[0]

def format_duration(seconds):
    """
    该函数用于将时间转换为对人友好的形式
    Parameters
    ----------
        seconds: 代表时间的非0整数
    """
    times = [("year", 365 * 24 * 60 * 60),
             ("day", 24 * 60 * 60),
             ("hour", 60 * 60),
             ("minute", 60),
             ("second", 1)]

    if not seconds:
        return "now"

    chunks = []
    for name, secs in times:
        qty = seconds // secs
        if qty:
            if qty > 1:
                name += "s"
            chunks.append(str(qty) + " " + name)

        seconds = seconds % secs

    return ', '.join(chunks[:-1]) + ' and ' + chunks[-1] if len(chunks) > 1 else chunks[0]


class PokerHand(object):
    """
    该类是用于德州扑克两个人比较大小
    """
    CARD = "23456789TJQKA"
    RESULT = ["Loss", "Tie", "Win"]

    def __init__(self, hand):
        values = ''.join(sorted(hand[::3], key = self.CARD.index))
        suits = set(hand[1::3])
        is_straight = values in self.CARD
        is_flush = len(suits) == 1
        self.score = (2 * sum(values.count(card) for card in values)
                      + 13 * is_straight + 15 * is_flush,
                      [self.CARD.index(card) for card in values[::-1]])
        print(self.score)
    def compare_with(self, other):
        return self.RESULT[(self.score > other.score) - (self.score < other.score) + 1]


def runTest(msg, expected, hand, other):
    test = Test()
    player, opponent = PokerHand(hand), PokerHand(other)
    test.assert_equals(player.compare_with(opponent), expected, "{}: '{}' against '{}'".format(msg, hand, other))


if __name__ == "__main__":
    # print(convert("abc", allow, hex))
    a = np.zeros((2, 2, 3))
    b = np.ones((2, 2, 3))
    print("a ====", a, "\n", "b ====", b)
    print(np.concatenate((a, b), axis = 2))
    print(format_duration(3600))
    runTest("Highest straight flush wins", "Loss", "2H 3H 4H 5H 6H", "KS AS TS QS JS")
