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



if __name__ == "__main__":
    print(validate_pin("12a4"))
    print(calculate_years(1000, 0.05, 0.18, 1100))