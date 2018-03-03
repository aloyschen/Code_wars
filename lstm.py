import numpy as np
import math
import random

def sigmoid(x):
    """
    改函数是对输入变量使用sigmoid函数
    Parameters
    ----------
        x: 输入变量
    Returns
    -------
        sigmoid函数计算结果
    """
    return 1. / (1 + np.exp(-x))


def sigmoid_derivative(values):
    """
    该函数是对sigmoid函数计算求导的结果
    Parameters
    ----------
        values: 求导公式计算输入变量
    Returns
    -------
        求导计算出的结果
    """
    return values * (1 - values)

def tanh_derivative(values):
    """
    该函数是计算tanh函数求导的结果
    Parameters
    ----------
        values: 求导函数输入变量
    Returns
    -------
        求导计算出的结果
    """
    return 1. - values ** 2

def rand_arr(a, b, *args):
    """
    该函数用于生成范围在(a,b)范围内的数组，数组形状为args
    Parameters
    ----------
        a: 随机数组的下限
        b: 随机数组的上限
        args: 随机数组的shape
    Returns
    -------
        随机数组
    """
    np.random.seed(0)
    return np.random.rand(*args) * (b - a) + a

class LSTMParam:
    def __int__(self, mem_cell_ct, x_dim):
        """
        初始化函数
        Parameters
        ----------
            mem_cell_ct: LSTM隐藏层神经元数量
            x_dim: LSTM输入层维度
        Returns
        -------
            None
        """
        self.mem_cell_ct = mem_cell_ct



x_dim = 50
y_list = [-0.5, 0.2, 0.1, -0.5]
input_val_arr = [np.random.random(x_dim) for _ in y_list]
print(input_val_arr)