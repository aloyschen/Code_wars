import numpy as np
"""
判断字符串pin是否为4位或者6位
"""
def validate_pin(pin):
    print(pin.isdigit())
    if pin.isdigit() and (len(pin) is 4 or len(pin) is 6):
        return True
    else:
        return False
"""
该函数根据本金、利率以及税率计算需要几年达到目标
"""

def calculate_years(principal, interest, tax, desired):
    years = 0
    while principal < desired:
        principal += principal * interest * (1 - tax)
        years = years + 1
    return years

"""
求两个字符串数组中最大长度差值
"""
def mxdiflg(a1, a2):
    if len(a1) is 0 or len(a2) is 0:
        return -1
    max_a1, min_a1 = 0, 1000000
    max_a2, min_a2 = 0, 1000000
    result = 0
    for word in a1:
        length_first = len(word)
        if length_first > max_a1:
            max_a1 = length_first
        if length_first < min_a1:
            min_a1 = length_first
    for word in a2:
        length_second = len(word)
        if length_second > max_a2:
            max_a2 = length_second
        if length_second < min_a2:
            min_a2 = length_second
    if(abs(max_a2 - min_a1) > abs(max_a1 - min_a2)):
        result = abs(max_a2 - min_a1)
    else:
        result = abs(max_a1 - min_a2)
    return result
"""
上述问题最简洁版本
"""
def mxdiflg_best(a1, a2):
    if a1 and a2:
        return max(
            len(max(a1, key=len)) - len(min(a2, key=len)),
            len(max(a2, key=len)) - len(min(a1, key=len)))
    return -1

"""
该函数利用反向切片反转字符串
"""
def reverse_words(str):
    return ' '.join(word[::-1] for word in str.split())

"""
该函数找到数组中最小值，然后返回Index
"""
def findSmallestInt(arr):
    #Code here
    smallest = arr[0]
    index = 0
    for item in range(len(arr)):
        print(arr[item])
        if smallest > arr[item]:
            smallest = arr[item]
            index = item
    return index
"""
找出字符串数组中字符长度为4的字符串
"""
def friend(x):
    #Code
    return [friend for friend in x if len(friend) == 4]
"""
该函数判断在[m,n]区间内的质数之间的差值为g的第一组质数
若没有满足条件的则返回Null
"""

def gap(g, m, n):
    # your code
    result = []
    last_prime = 2
    for number in range(m, n):
        prime = True
        if number < 2:
            prime = False
        if number == 3:
            prime = True
        if number % 2 == 0:
            prime = False
        if number % 3 == 0:
            prime = False
        i = 5
        while i ** 2 <= number:
            if number % i == 0 or number % (i + 2) == 0:
                prime = False
            i += 6
        if(prime):
            if number - last_prime == g:
                return [last_prime, number]
            else:
                last_prime = number
    if last_prime == 2:
        return None






if __name__ == "__main__":
    print(validate_pin("12a4"))
    print(calculate_years(1000, 0.05, 0.18, 1100))
    s1 = ["hoqq", "bbllkw", "oox", "ejjuyyy", "plmiis", "xxxzgpsssa", "xxwwkktt", "znnnnfqknaz", "qqquuhii", "dvvvwz"]
    s2 = ["cccooommaaqqoxii", "gggqaffhhh", "tttoowwwmmww"]
    print(mxdiflg(s1, s2))
    print(reverse_words('This is an example!'))
    print(findSmallestInt([78,56,232,12,11,43]))
    print(friend(["Ryan", "Kieran", "Mark",]))
    print(gap(8,300,400))