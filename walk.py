"""
每次前进有四个方向，要求十次之后回到原点，返回行走的路径
-----
Param walk: 行走的路径
Return walk: 如果十次之后返回原点返回路径，否则返回False
"""


def isValidWalk(walk):
    # determine if walk is valid
    return len(walk) == 10 and walk.count('s') == walk.count('n') and walk.count('w') == walk.count('e')


"""
该函数是对字符串中的单词分割，然后去出其中的数字，根据数字进行排序
Param sentence: 输入的字符串句子
Return order_sentence: 排序之后的句子
"""

def order(sentence):
    # code here
    result = ''
    order_sentence = dict()
    order_result = []
    for word in sentence.split(' '):
        index = list(filter(str.isdigit, word))
        order_sentence[index[0]] = word
    order_sentence = sorted(order_sentence.items(), key = lambda d : d[0])
    for item in order_sentence:
        result += item[1] + ' '
    return result.strip()
"""
和上个函数实现的功能一样
"""
def order_modify(sentence):
    return " ".join(sorted(sentence.split(), key = lambda x: int("".join(filter(str.isdigit, x)))))

"""
将每个单词的首字母转换为大写
"""
def toJadenCase(string):
    return " ".join(word.capitalize() for word in string.split())


"""
统计字符串中重复出现的字符个数
"""
def duplicate_count(text):
    # Your code goes here
    count = 0
    for character in "".join(set(text)):
        if text.lower().count(character) > 1:
            count = count + 1
    return count
"""
python的三元表达式
"""
def hoopCount(n):
    # Good Luck!
    return "Great, now move on to tricks" if n >= 10 else "Keep at it until you get it"

if __name__ == "__main__":
    path = ['s', 'e', 's', 'w', 'e', 'w', 'n', 'n', 's', 'n']
    print(isValidWalk(path))
    print(order_modify("is2 Thi1s T4est 3a"))
    print(toJadenCase("how i can"))
    print(duplicate_count("abcdeaaa"))
    print(hoopCount(5))
