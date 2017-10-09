"""
该函数是将输入的列表中的数字，每8个
"""
def data_reverse(data):
    split_data = []
    result = []
    for i in range(0, len(data), 8):
        split_data.insert(0, data[i : i + 8])
    for item in split_data:
        result = result + item
    return result


if __name__ == "__main__":
    data3 = [0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1]
    data4 = [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0]
    print(data_reverse(data3))