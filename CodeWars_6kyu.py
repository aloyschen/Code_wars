
def data_reverse(data):
    """
    该函数是将输入的列表中的数字，每8个
    """
    split_data = []
    result = []
    for i in range(0, len(data), 8):
        split_data.insert(0, data[i : i + 8])
    for item in split_data:
        result = result + item
    return result

def rot(string):
    """
    该函数先将字符串按照\n分割，然后反转
    Parameters
    ----------
        string: 输入字符串
    Returns
    -------
        反转后的字符串
    """
    result = []
    for item in string.split("\n"):
        result.insert(0, item[ : : -1])
    return "\\n".join(result)



def selfie_and_rot(string):
    """
    该函数在翻转的同时，将过程打印出来
    Parameters
    ----------
        string: 输入字符串
    """
    split_str = string.split("\n")
    result = []
    for item in split_str:
        result.insert(0, item[ : : -1])
    point = "." * len(split_str[0])
    print((point + "\\n").join(split_str) + point + "\\n" + point +(point + "\\n").join(result))


def oper(fct, s):
    return fct(s)

if __name__ == "__main__":
    data3 = [0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1]
    data4 = [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0]
    print(data_reverse(data3))
    print(rot('xZBV\njsbS\nJcpN\nfVnP'))
    selfie_and_rot('xZBV\njsbS\nJcpN\nfVnP')
    print(oper(rot, "fijuoo\nCqYVct\nDrPmMJ\nerfpBA\nkWjFUG\nCVUfyL"))