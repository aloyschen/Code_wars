import re


"""
该函数用来返回url中的主域名
"""
def domain_name(url):
    return re.search('(https?://)?(www\d?\.)?(?P<name>[\w-]+)\.', url).group('name')


"""
该函数用来检测一个整数n是否可以表示为m的k次方
Param n: 待检测的整数n
"""
def isPP(n):
    current = 2
    while(current <= n ** .5):
        power = 2
        while(pow(current, power) <= n):
            if pow(current, power) == n:
                return [current, power]
            else:
                power = power + 1
        current = current + 1



if __name__ == "__main__":
    print(domain_name("http://www.zombie-bites.com"))
    print(isPP(81))