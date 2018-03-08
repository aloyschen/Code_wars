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
        self.x_dim = x_dim
        concat_len = x_dim + mem_cell_ct
        #权值矩阵初始化
        self.wg = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)
        self.wi = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)
        self.wf = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)
        self.wo = rand_arr(-0.1, 0.1, mem_cell_ct, concat_len)
        #偏置矩阵初始化
        self.bg = rand_arr(-0.1, 0.1, mem_cell_ct)
        self.bo = rand_arr(-0.1, 0.1, mem_cell_ct)
        self.bi = rand_arr(-0.1, 0.1, mem_cell_ct)
        self.bf = rand_arr(-0.1, 0.1, mem_cell_ct)
        #损失函数求导矩阵初始化
        self.wg_diff = np.zeros((mem_cell_ct, concat_len))
        self.wi_diff = np.zeros((mem_cell_ct, concat_len))
        self.wf_diff = np.zeros((mem_cell_ct, concat_len))
        self.wo_diff = np.zeros((mem_cell_ct, concat_len))
        self.bg_diff = np.zeros(mem_cell_ct)
        self.bi_diff = np.zeros(mem_cell_ct)
        self.bo_diff = np.zeros(mem_cell_ct)
        self.bf_diff = np.zeros(mem_cell_ct)

    def apply_diff(self, lr = 1):
        """

        :param lr:
        :return:
        """
        self.wg -= lr * self.wg_diff
        self.wi -= lr * self.wi_diff
        self.wo -= lr * self.wo_diff
        self.wf -= lr * self.wf_diff
        self.bg -= lr * self.bg_diff
        self.bi -= lr * self.bi_diff
        self.bo -= lr * self.bo_diff
        self.bf -= lr * self.bf_diff
        #重置求导矩阵
        self.wg_diff = np.zeros_like(self.wg)
        self.wi_diff = np.zeros_like(self.wi)
        self.wo_diff = np.zeros_like(self.wo)
        self.wf_diff = np.zeros_like(self.wf)
        self.bg_diff = np.zeros_like(self.bg)
        self.bi_diff = np.zeros_like(self.bi)
        self.bo_diff = np.zeros_like(self.bo)
        self.bf_diff = np.zeros_like(self.bf)
class LSTMState:
    def __init__(self, lstm_param, lstm_state):
        """
        初始化LSTM的状态
        Parameters
        ----------
            lstm_param: lstm参数
            lstm_state: lstm状态
        Returns
        -------
            None
        """
        self.state = lstm_state
        self.param = lstm_param
        #与递归输入连接的非递归输入
        self.xc = None

    def bottom_data_is(self, x, s_prev = None, h_prev = None):
        if s_prev is None:
            s_prev = np.zeros_like(self.state.s)
        if h_prev is None:
            h_prev = np.zeros_like(self.state.h)
        self.s_prev = s_prev
        self.h_prev = h_prev
        xc = np.hstack((x, h_prev))
        self.state.g = np.tanh(np.dot(self.param.wg, xc) + self.param.bg)
        self.state.i = sigmoid(np.dot(self.param.wi, xc) + self.param.bi)
        self.state.f = sigmoid(np.dot(self.param.wf, xc) + self.param.bf)
        self.state.o = sigmoid(np.dot(self.param.wo, xc) + self.param.bo)
        self.state.s = self.state.g * self.state.i + s_prev * self.state.f
        self.state.h = self.state.o * self.state.s
        self.xc = xc


    def top_diff_is(self, top_diff_h, top_diff_s):
        ds = self.state.o * top_diff_h + top_diff_s
        do = self.state.s * top_diff_h
        di = self.state.g * ds
        dg = self.state.i * ds
        df = self.s_prev * ds

        di_input = sigmoid_derivative(self.state.i) * di
        df_input = sigmoid_derivative(self.state.f) * df
        do_input = sigmoid_derivative(self.state.o) * do
        dg_input = tanh_derivative(self.state.g) * dg

        self.param.wi_diff += np.outer(di_input, self.xc)
        self.param.wf_diff += np.outer(df_input, self.xc)
        self.param.wo_diff += np.outer(do_input, self.xc)
        self.param.wg_diff += np.outer(dg_input, self.xc)
        self.param.bi_diff += di_input
        self.param.bf_diff += df_input
        self.param.bo_diff += do_input
        self.param.bg_diff += dg_input

        dxc = np.zeros_like(self.xc)
        dxc += np.dot(self.param.wi.T, di_input)
        dxc += np.dot(self.param.wf.T, df_input)
        dxc += np.dot(self.param.wo.T, do_input)
        dxc += np.dot(self.param.wg.T, dg_input)

        self.state.bottom_diff_s = ds * self.state.f
        self.state.bottom_diff_h = dxc[self.param.x_dim : ]
class LSTMNetwork():
    def __init__(self, lstm_param):
        self.lstm_params = lstm_param
        self.lstm_node_list = []
        self.x_list = []


    def y_list_is(self, y_list, loss_layer):
        assert len(y_list) == len(self.x_list)
        idx = len(self.x_list) - 1
        loss = loss_layer.loss(self.lstm_node_list[idx].state.h, y_list[idx])
        diff_h = loss_layer.bottom_diff(self.lstm_node_list[idx].state.h, y_list[idx])
        diff_s = np.zeros(self.lstm_params.mem_cell_ct)
        self.lstm_node_list[idx].top_diff_is(diff_h, diff_s)
        idx -= 1

        while idx >= 0:
            loss += loss_layer.loss(self.lstm_node_list[idx], y_list[idx])
            diff_h = loss_layer.bottom_diff(self.lstm_node_list[idx].state.h, y_list[idx])
            diff_h += self.lstm_node_list[idx + 1].state.bottom_diff_h
            diff_s = self.lstm_node_list[idx + 1].state.bottom_diff_s
            self.lstm_node_list[idx].top_diff_is(diff_h, diff_s)
            idx -= 1
        return loss









x_dim = 50
y_list = [-0.5, 0.2, 0.1, -0.5]
input_val_arr = [np.random.random(x_dim) for _ in y_list]
print(input_val_arr)