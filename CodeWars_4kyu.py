bin = '01'
oct = '01234567'
dec = '0123456789'
hex = '0123456789abcdef'
allow = 'abcdefghijklmnopqrstuvwxyz'
allup = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphanum = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
if __name__ == "__main__":
    print(convert("abc", allow, hex))