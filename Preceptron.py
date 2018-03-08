# 该脚本实现一个简单的神经网络感知器
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import matplotlib.gridspec as gridspec
from sklearn.model_selection import train_test_split

#设置Numpy打印精度
np.set_printoptions(precision=5, suppress=True)
def dataset_fixed_cov(n = 300, dim = 2):
    """
    该函数用于生成样本数据, 二维高斯分布
    """
    np.random.seed(42)
    C = np.array([[0., -0.23], [0.83, .23]])
    #np.r_是按照列连接两个矩阵
    X = np.r_[np.dot(np.random.randn(n, dim), C), np.dot(np.random.randn(n, dim), C) + np.array([1, 1])]
    Y = np.hstack((np.zeros(n), np.ones(n))).astype(np.int)
    return X, Y


def plot_data():
    """
    该函数用于将数据样本可视化
    """
    X, Y = dataset_fixed_cov(300, 2)
    print(X, Y)
    plt.scatter(X[Y == 0, 0], X[Y == 0, 1], c = 'g')
    plt.scatter(X[Y == 1, 0], X[Y == 1, 1], c = 'r')
    plt.show()

def sigmoid(x):
    """
    sigmoid函数
    Parameters
    ----------
        x: 输入变量
    Returns
    -------
        sigmoid函数计算结果
    """
    return 1. / (1 + np.exp(-x))

def sigmoid_derivative(x):
    """
    sigmoid函数求导
    Parameters
    ----------
        x: 输入变量
    Returns
    -------
        sigmoid函数求导计算结果
    """
    return sigmoid(x) * (1 - sigmoid(x))


class Perceptron(object):
    def __init__(self, x_dim, activation = 'sigmoid'):
        """
        初始化输入特征维度和激活函数
        Parameters
        ----------
            x_dim: 输入特征维度
            activation: 激活函数
        Returns
        -------
            None
        """
        if activation == 'sigmoid':
            self.activation = sigmoid
            self.activation_deriv = sigmoid_derivative
        else:
            raise ValueError('Unknown activation function {}'.format(activation))
        weights = x_dim + 1
        self.W = (2 * np.random.random(weights)) * 0.25
        self.W = self.W.reshape(-1, 1)
        self.train_errors, self.validation_errors = [], []

    def _add_biax_X(self, X):
        """
        对输入样本特征加入偏置项对应的x0
        Parameters
        ----------
            X: 样本特征
        Returns
        -------
            加入偏置项之后的样本
        """
        temp = np.ones((X.shape[0], X.shape[1] + 1))
        temp[:, :-1] = X
        return temp

    def _error_derivative(self, y_true, y_pred, y_pred_prime):
        """
        误差函数求导
        Parameters
        ----------
            y_true: 真实值
            y_pred: 预测值
            y_pred_prime: 预测值求导
        Returns
        -------
            误差函数求导计算结果
        """
        return -2 * (y_true - y_pred) * y_pred_prime


    def _error(self, y_true, y_pred):
        """
        该函数计算预测值和真实值的误差
        Parameters
        ----------
            y_true: 真实值
            y_pred: 预测值
        Returns
        -------
            计算出的误差值
        """
        return (y_pred - y_true) ** 2


    def train(self, X_train, Y_train, X_validation, Y_validation,
              learningRate = 0.2, epochs = 10, minibatch_size = 10, weight_decay = 0):
        """
        训练神经网络函数
        Parameters
        ----------
            X_train: 训练集样本特征
            Y_train: 训练集样本标签
            X_validation: 验证集样本特征
            Y_validation: 验证集样本标签
            learningRate: 学习率
            epochs: 迭代次数
            minibatch_size: 每次迭代样本数
            weight_decay: 权重衰减，防止过拟合
        """
        assert len(X_train.shape) == 2, 'X must be 2D'
        X_train = self._add_biax_X(X_train)
        X_validation = self._add_biax_X(X_validation)

        self.weights_decay = weight_decay

        for epoch in range(epochs):
            minibatch_indices = np.arange(X_train.shape[0])
            np.random.shuffle(minibatch_indices)
            for start in range(0, len(minibatch_indices), minibatch_size):
                end = start + minibatch_size
                indices = minibatch_indices[start : end]
                Xb = X_train[indices]
                Yb = Y_train[indices]
                l = Xb.dot(self.W).flatten()
                deltas = self._error_derivative(Yb, self.activation(l), self.activation_deriv(l))
                #np.tile函数实现在行列方向上复制
                grad_W = Xb * np.tile(deltas.reshape(-1, 1), (1, Xb.shape[1]))
                #mean是求梯度平均值
                grad_W = np.mean(grad_W, axis = 0).reshape(-1, 1)
                self.W -= learningRate * grad_W + self.weights_decay * self.W
            self.train_errors.append(self._error(Y_train, self.decision_function(X_train, addbias = False)).mean())
            self.validation_errors.append(self._error(Y_validation, self.decision_function(X_validation, addbias = False)).mean())
        return self


    def predict(self, X, addbias = False):
        """
        预测样本的输出类别
        Parameters
        ----------
            X: 需要预测的数据
            addbias: 是否加偏置项
        Returns
        -------
            根据阈值返回样本的类别
        """
        return (self.decision_function(X, addbias) > 0.5).astype(np.int)


    def decision_function(self, X, addbias = True):
        """
        计算激活函数对输入样本的输出值
        Parameters
        ----------
            X: 输入样本值
            addbias: 是否加入偏置项
        Returns
        -------
            返回激活函数计算值
        """
        if addbias:
            X = self._add_biax_X(X)
        return self.activation(X.dot(self.W).flatten())

def show_decision_boundary(clf, X, Y, subplot_spec = None):
    """
    该函数将分割平面可视化
    clf:
    :param X:
    :param Y:
    :param subplot_spec:
    :return:
    """
    assert X.shape[1] == 2
    wration = (15, 1)
    # 调整图之间布局
    if subplot_spec is None:
        gs = gridspec.GridSpec(1, 2, width_ratios = wration)
    else:
        gs = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec = subplot_spec, width_ratios = wration)
    ax = plt.subplot(gs[0])
    ax.set_title('Dataset and decision function')
    X_min, X_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    Y_min, Y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    h = 0.2
    xx, yy = np.meshgrid(np.arange(X_min, X_max, h),
                         np.arange(Y_min, Y_max, h))
    #np.c_是将一维数组转成二维数组
    z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)
    ctr = ax.contourf(xx, yy, z, cmap = plt.cm.get_cmap('gray'), vmin = 0, vmax = 1)
    unique_labels = np.unique(Y)
    colors = ['orchid', 'dodgerblue']
    for i, yi in enumerate(unique_labels):
        color = colors[i]
        ax.scatter(X[ Y == yi, 0], X[Y == yi, 1], c = color, linewidth = 0, label='%d' % yi)
    ax.legend()
    ax.set_xlim((X_min, X_max))
    ax.set_ylim((Y_min, Y_max))
    plt.colorbar(ctr, cax = plt.subplot(gs[1]))
    # plt.show()


if __name__ == "__main__":
    X, Y = dataset_fixed_cov()
    X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size = 0.33)
    AVConvWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Perceptron training', artist='gaochen', comment='')
    writer = AVConvWriter(fps=4, metadata=metadata)
    perceptron = Perceptron(X.shape[1])

    fig = plt.figure(figsize=(10, 5))
    gs = gridspec.GridSpec(1, 2, wspace=0.4)

    nepochs = 50

    err_ymax = None

    with writer.saving(fig, './test.mp4', 100):
        for epoch in range(nepochs):
            perceptron.train(X_train, Y_train, X_validation, Y_validation, epochs=1, minibatch_size=10)
            if err_ymax is None:
                err_ymax = max(np.max(perceptron.train_errors),
                                np.max(perceptron.validation_errors)) * 1.1
            show_decision_boundary(perceptron, X, Y, gs[0])

            ax = plt.subplot(gs[1])
            ax.set_title('Error')
            ax.plot(perceptron.train_errors, color = 'r')
            ax.plot(perceptron.validation_errors, color = 'g')
            ax.set_xlim(0, nepochs)
            ax.set_ylim(0, err_ymax)
            ax.set_xlabel('epochs')
            ax.set_ylabel('error')
            # ax.legend(loc = 'upper right')
            plt.legend(['train', 'validation'])
            writer.grab_frame()
