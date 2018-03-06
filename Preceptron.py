# 该脚本实现简单的神经网络感知器

class Perceptron(object):
    def __int__(self, input_num, activator):
        """
        初始化感知器权重参数和偏置，设置输入样本特征维度和激活函数
        Parameters
        ----------
            input_num: 输入样本特征维度
            activator: 激活函数
        Returns
        -------
            None
        """
        self.activator = activator
        self.weights = [0.0 for _ in range(input_num)]
        self.bias = 0.0

    def __str__(self):
        """
        打印输出学习到的权重，偏置项
        Parameters
        ----------
            None
        Returns
        -------
            None
        """
        return 'weights\t:{}\nbias\t:{}\n'.format(self.weights, self.bias)

    def predict(self, input_vec):
        """
        输入感知器的输入，打印感知器的计算结果
        :param input_vec:
        :return:
        """