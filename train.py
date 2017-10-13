# coding:utf-8
# 该脚本是用于训练模型
# Author: gaochen
# Date: 2017.10.09
import tensorflow as tf
import numpy as np
import time
import os
import random
import tifffile as tiff


train_Path = '../training_pic/'
Model_Path = 'model0.ckpt'


def shuffle_namelist(Path):
    """
    该函数是用于将所有样本图像的名字打乱
    Parameters
    ----------
        Path:训练样本根目录
    Returns
    -------
        name_list: 打乱之后的样本名字列表
    """
    name_list = list(set([name.split('_')[0] for name in os.listdir(Path)]))
    random.shuffle(name_list)
    return name_list



def read_2_namelist(name_list, batch_size, start_index):
    """
    该函数用于获取每次迭代所需的正负样本图像名字列表
    Parameters
    ----------
        name_list: 所有正负样本的名字列表
        batch_size: 每次训练迭代需要的样本数
        start_index: 开始的编号
    Returns
    -------
        image_batch: 包含正负样本名字的数组
        label_batch: 包含标签的样本名字和数组
    """
    image_batch = []
    label_batch = []
    if start_index + batch_size > len(name_list):
        random.shuffle(name_list)
        start_index = start_index + batch_size - len(name_list)
    for name in name_list[start_index:start_index + batch_size]:
        image_batch.append(tiff.imread(train_Path + name + '_input.tif'))
        label_batch.append(tiff.imread(train_Path + name + '_output.tif'))
    return np.array(image_batch), np.array(label_batch), (start_index + batch_size) % len(name_list)




def variable_with_weight_loss(shape, stddev, wl):
    """
    该函数按照正态分布初始化权重
    Parameters
    ----------
        shape: 权值矩阵大小
        stddev: 正态分布标准差
        wl: 是否采用L2正则化
    Returns
    -------
        var: 随机生成的权值初始值
    """
    # truncated_normal从截断的正态分布中输出随机值。
    var = tf.Variable(tf.truncated_normal(shape, stddev = stddev))
    if wl is not None:
        weight_loss = tf.multiply(tf.nn.l2_loss(var), wl, name = 'weight_loss')
        tf.add_to_collection('losses', weight_loss)
    return var



def train_model(input_size_height = 24, input_size_width = 24, input_passageway_num = 8, model_path = Model_Path, batch_size = 128):
    """
    该函数用于创建训练模型
    Parameters
    ----------
        input_size_height: 输入图像的高度
        input_size_width: 输入图像的宽度
        input_passageway_num: 输入图像的通道数
        model_path: 模型保存路径
        batch_size: 每次迭代的样本数
    Returns
    -------
        logits: 预测的结果
        image_holder: 存储图像的数据结构
        label_holder: 存储标签的数据结构
    """
    out_label_num = input_size_height * input_size_width
    image_holder = tf.placeholder(tf.float32, [batch_size, input_size_height, input_size_width, input_passageway_num])
    label_holder = tf.placeholder(tf.int32, [batch_size, out_label_num])
    weight1 = variable_with_weight_loss(shape=[5, 5, input_passageway_num, 64], stddev = 5e-2, wl = 0)
    kernel1 = tf.nn.conv2d(image_holder, weight1, strides=[1, 1, 1, 1], padding='SAME')
    bias1 = tf.Variable(tf.constant(0.0, shape=[64]))
    conv1 = tf.nn.relu(tf.nn.bias_add(kernel1, bias1))
    pool1 = tf.nn.max_pool(conv1, ksize = [1, 3, 3, 1], strides = [1, 2, 2, 1], padding='SAME')
    norm1 = tf.nn.lrn(pool1, 4, bias = 1.0, alpha = 0.001 / 9.0, beta = 0.75)

    weight2 = variable_with_weight_loss(shape = [5, 5, 64, 64], stddev = 5e-2, wl=0)
    kernel2 = tf.nn.conv2d(norm1, weight2, strides = [1, 1, 1, 1], padding='SAME')
    bias2 = tf.Variable(tf.constant(0.1, shape = [64]))
    conv2 = tf.nn.relu(tf.nn.bias_add(kernel2, bias2))
    norm2 = tf.nn.lrn(conv2, 4, bias = 1.0, alpha = 0.001 / 9.0, beta = 0.75)
    pool2 = tf.nn.max_pool(norm2, ksize = [1, 3, 3, 1], strides = [1, 2, 2, 1], padding = 'SAME')

    reshape = tf.reshape(pool2, [batch_size, -1])
    dim = reshape.get_shape()[1].value
    weight3 = variable_with_weight_loss(shape=[dim, 384], stddev=0.04, wl=0.004)
    bias3 = tf.Variable(tf.constant(0.1, shape=[384]))
    local3 = tf.nn.relu(tf.matmul(reshape, weight3) + bias3)

    weight4 = variable_with_weight_loss(shape=[384, 192], stddev=0.04, wl=0.004)
    bias4 = tf.Variable(tf.constant(0.1, shape=[192]))
    local4 = tf.nn.relu(tf.matmul(local3, weight4) + bias4)


    weight5 = variable_with_weight_loss(shape=[192, out_label_num], stddev=1 / 192.0, wl=0.0)
    bias5 = tf.Variable(tf.constant(0.0, shape=[out_label_num]))
    logits = tf.matmul(local4, weight5) + bias5
    return logits, label_holder, image_holder



def log_loss(logits, labels):
    """
    还没看懂怎么算得train_loss
    """
    print ('logits=',np.shape(logits))
    print ('labels0=',np.shape(labels))
    labels = tf.cast(labels, tf.float32)
    print ('labels1=',np.shape(labels))
    # cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels,
    #                                                                name='cross_entropy_per_example')
    cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits = logits, labels = labels, name = 'cross_entropy_per_example')
    # tf.nn.()
    cross_entropy_mean = tf.reduce_mean(cross_entropy, name = 'cross_entropy')
    tf.add_to_collection('losses', cross_entropy_mean)
    return tf.add_n(tf.get_collection('losses'), name = 'total_loss')



def run_train(gpu_index = "0", model_path = Model_Path, iter_num = 10000, batch_size = 128, learning_rate = 0.001):
    """
    该函数用于训练、保存模型
    Parameters
    ----------
        gpu_index: 设置使用的gpu编号
        model_path: 模型保存路径
        iter_num: 总共迭代的次数
        batch_size: 每次迭代需要的样本数量
        learning_rate: 学习速率
    """
    name_list = shuffle_namelist(train_Path)
    logits, label_holder, image_holder = train_model()
    loss = log_loss(logits, label_holder)
    train_op = tf.train.AdamOptimizer(1e-3).minimize(loss)
    saver=tf.train.Saver()
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu_index
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction = 0.8)
    config = tf.ConfigProto(gpu_options = gpu_options)
    with tf.Session() as sess:
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        tf.global_variables_initializer().run()
        tf.train.start_queue_runners()
        start_index = 0
        for step in range(iter_num):
            start_time = time.time()
        # image_batch, label_batch = sess.run([images_train, labels_train])
            image_batch, label_batch, start_index = read_2_namelist(name_list, batch_size, start_index)
        # print (label_batch.shape)
            _, loss_value = sess.run([train_op, loss], feed_dict={image_holder: image_batch, label_holder: label_batch})
            duration = time.time() - start_time
            if step % 10 == 0:
                examples_per_sec = batch_size / duration
                sec_per_batch = float(duration)
                format_str = ('step %d,loss=%.2f(%1.f examples/sec;%.3f sec/batch)')
                print('\r' + format_str % (step, loss_value, examples_per_sec, sec_per_batch), end="3" )
            if step % 100 == 0:
                print()

        print ('training finish')
        save_path = saver.save(sess, model_path)

if __name__ == "__main__":
    run_train()
