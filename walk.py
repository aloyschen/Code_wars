"""
每次前进有四个方向，要求十次之后回到原点，返回行走的路径
-----
Param walk: 行走的路径
Return walk: 如果十次之后返回原点返回路径，否则返回False
"""
def isValidWalk(walk):
    #determine if walk is valid
    return len(walk) == 10 and walk.count('s') == walk.count('n') and walk.count('w') == walk.count('e')

if __name__ == "__main__":
    path = ['s', 'e', 's', 'w', 'e', 'w', 'n', 'n', 's', 'n']
    print(isValidWalk(path))