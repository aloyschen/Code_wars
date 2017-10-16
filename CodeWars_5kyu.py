import re



def domain_name(url):
    """
    该函数用来返回url中的主域名
    """
    return re.search('(https?://)?(www\d?\.)?(?P<name>[\w-]+)\.', url).group('name')



def isPP(n):
    """
    该函数用来检测一个整数n是否可以表示为m的k次方
    Parameters
    ----------
        n: 待检测的整数n
    Returns
    -------
        ps: input 9 return [3, 2]
    """
    current = 2
    while(current <= n ** .5):
        power = 2
        while(pow(current, power) <= n):
            if pow(current, power) == n:
                return [current, power]
            else:
                power = power + 1
        current = current + 1



def to_camel_case(text):
    """
    该函数将字符串中的每个单词首字母大写，然后将—_字符替换调
    Parameters
    ----------
        text: 输入字符串
    Returns
    -------
        过滤之后的字符串
    """
    if text == '':
        return ''
    return text[0] + text.title().replace('-', '').replace('_', '')[1 : ]

def who_eats_who(zoo):
    """
    描述动物园内互相吃的关系
    Parameters
    ----------
        zoo:
    Returns
    -------
    """
    relations = {"antelope" : "grass", "big-fish" : "little-fish", "bug" : "leaves", "bear" : "big-fish,bug,chicken,cow,leaves,sheep", "chicken" : "bug", "cow" : "grass", "fox" : "chicken,sheep", "giraffe" : "leaves", "lion" : "antelope,cow", "panda" : "leaves", "sheep" : "grass"}
    ansLst, zooLst, n = [zoo], zoo.split(","), 0
    print(relations.get("bear", set()))
    while n < len(zooLst):
        while n > 0 and zooLst[n - 1] in relations.get(zooLst[n], set()):  # Eats on its left
            ansLst.append("{} eats {}".format(zooLst[n], zooLst.pop(n - 1)))
            n -= 2

        while n >= 0 and n != len(zooLst) - 1 and zooLst[n + 1] in relations.get(zooLst[n], set()):  # Eats on its right
            ansLst.append("{} eats {}".format(zooLst[n], zooLst.pop(n + 1)))

        n += 1  # Nothing to eat, step forward

    return ansLst + [','.join(zooLst)]



def my_very_own_split(string, delimiter = None):
    """
    该函数实现split的功能，并且使用生成器generator实现
    Parameters
    ----------
        string: 输入字符串
        delimiter: 字符串分隔符
    Returns
    -------
        string: 分割后的字符串列表
    """
    pos = 0
    if delimiter == '':
        raise ValueError('empty delimiter')
    if delimiter == None:
        delimiter = '\s+'
    else:
        delimiter = re.escape(delimiter)
    for m in re.finditer(delimiter, string):
        yield string[pos:m.start()]
        pos = m.end()
    yield string[pos:]


if __name__ == "__main__":
    print(domain_name("http://www.zombie-bites.com"))
    print(isPP(81))
    print(to_camel_case("A-Pippi-is_pippi"))
    print(who_eats_who("sheep,leaves,panda,sheep,bicycle,chicken,leaves,grass,big-fish,sheep,grass"))
    generator = my_very_own_split('abc,#def#,ghi,#jkl', ',#')
    print(next(generator))
    print(next(generator))