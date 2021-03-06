import numpy as np


def validate_pin(pin):
    """
    判断字符串pin是否为4位或者6位
    """
    print(pin.isdigit())
    if pin.isdigit() and (len(pin) is 4 or len(pin) is 6):
        return True
    else:
        return False


def calculate_years(principal, interest, tax, desired):
    """
    该函数根据本金、利率以及税率计算需要几年达到目标
    """
    years = 0
    while principal < desired:
        principal += principal * interest * (1 - tax)
        years = years + 1
    return years


def mxdiflg(a1, a2):
    """
    求两个字符串数组中最大长度差值
    """
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



def mxdiflg_best(a1, a2):
    """
    上述问题最简洁版本
    """
    if a1 and a2:
        return max(
            len(max(a1, key=len)) - len(min(a2, key=len)),
            len(max(a2, key=len)) - len(min(a1, key=len)))
    return -1


def reverse_words(str):
    """
    该函数利用反向切片反转字符串
    """
    return ' '.join(word[::-1] for word in str.split())


def findSmallestInt(arr):
    """
    该函数找到数组中最小值，然后返回Index
    """
    #Code here
    smallest = arr[0]
    index = 0
    for item in range(len(arr)):
        print(arr[item])
        if smallest > arr[item]:
            smallest = arr[item]
            index = item
    return index

def friend(x):
    """
    找出字符串数组中字符长度为4的字符串
    """
    #Code
    return [friend for friend in x if len(friend) == 4]

def gap(g, m, n):
    """
    该函数判断在[m,n]区间内的质数之间的差值为g的第一组质数
    若没有满足条件的则返回Null
    """
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

def remove_smallest(numbers):
    """
    该函数移除数组中最小的数字，不改变之前的数组顺序
    """
    if(numbers):
        return numbers.remove(min(numbers))
    return numbers

from re import compile, VERBOSE
def regex_test(str):
    """
    正则匹配
    """
    regex = compile("""
    ^              # begin word
    (?=.*?[a-z])   # at least one lowercase letter
    (?=.*?[A-Z])   # at least one uppercase letter
    (?=.*?[0-9])   # at least one number
    [A-Za-z\d]     # only alphanumeric
    {6,}           # at least 6 characters long
    $              # end word
    """, VERBOSE)



def multiplication_table(row,col):
    """
    该函数返回一个指定行数和列数的矩阵数组
    """
    # Good Luck!
    return [[(i + 1) * (j + 1) for j in range(col)] for i in range(row)]


def Xbonacci(signature, n):
    """
    数组第n个数是前n个数之和，最后返回前n个值
    """
    #your code here
    num = len(signature)
    print(num)
    for time in range(n - num):
        print(signature[-num : ])
        signature.append(sum(signature[-num : ]))
    return signature

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
    print(validate_pin("12a4"))
    print(calculate_years(1000, 0.05, 0.18, 1100))
    s1 = ["hoqq", "bbllkw", "oox", "ejjuyyy", "plmiis", "xxxzgpsssa", "xxwwkktt", "znnnnfqknaz", "qqquuhii", "dvvvwz"]
    s2 = ["cccooommaaqqoxii", "gggqaffhhh", "tttoowwwmmww"]
    print(mxdiflg(s1, s2))
    print(reverse_words('This is an example!'))
    print(findSmallestInt([78,56,232,12,11,43]))
    print(friend(["Ryan", "Kieran", "Mark",]))
    print(gap(8,300,400))
    print(remove_smallest([5, 3, 2, 1, 4]))
    print(multiplication_table(3,3))
    print(Xbonacci([0,1], 10))
