from CodeTest import Test
"""
该函数将二进制数组转换为10进制数字
"""
def binary_array_to_number(arr):
    result = 0
    for num in range(len(arr)):
        result += arr[-num-1] * (2 ** num)
        print(result)
    return result
def binary_array_to_number_best(arr):
    return int(''.join(map(str, arr)), 2)


if __name__ == "__main__":
    test = Test()
    test.describe("One's and Zero's")
    test.it("Example tests")
    test.assert_equals(binary_array_to_number_best([0, 0, 0, 1]), 1)
    test.assert_equals(binary_array_to_number_best([0, 0, 1, 0]), 2)
    test.assert_equals(binary_array_to_number_best([1, 1, 1, 1]), 15)
    test.assert_equals(binary_array_to_number_best([0, 1, 1, 0]), 6)


