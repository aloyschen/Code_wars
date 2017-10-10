bin = '01'
oct = '01234567'
dec = '0123456789'
hex = '0123456789abcdef'
allow = 'abcdefghijklmnopqrstuvwxyz'
allup = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphanum = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
import numpy as np
"""
该函数用于不同进制之间的转换
"""
def convert(input, source, target):
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
"""
该函数用于将时间转换为对人友好的形式
Param seconds: 代表时间的非0整数
"""
def format_duration(seconds):
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


if __name__ == "__main__":
    # print(convert("abc", allow, hex))
    a = np.zeros((2, 2, 3))
    b = np.ones((2, 2, 3))
    print("a ====", a, "\n", "b ====", b)
    print(np.concatenate((a, b), axis = 2))
    print(format_duration(3600))
