# coding='utf-8'
# 该脚本用于预测土地变化区域，生成提交结果
# Author: gaochen
# Date: 2017.10.09

import tensorflow as tf
import numpy as np
from PIL import Image
import tifffile as tiff
import time
import os

FILE_2015 = '../data/quickbird2015.tif'
FILE_2017 = '../data/quickbird2017.tif'


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
    var = tf.Variable(tf.truncated_normal(shape, stddev=stddev))
    if wl is not None:
        weight_loss = tf.multiply(tf.nn.l2_loss(var), wl, name='weight_loss')
        tf.add_to_collection('losses', weight_loss)
    return var



def scale_percentile(matrix):
    """
    该函数是对图像进行标准化处理
    parameters
    ----------
        matrix: 图像中一个区域的矩阵，通道为蓝，绿，红，近地
    Returns
    -------
        matrix: 经过标准化处理之后的图像数据
    """
    w, h, d = matrix.shape
    # 先将数据reshape成一行数据
    matrix = np.reshape(matrix, [w * h, d]).astype(np.float64)
    # 通过百分位数获取数据的最大值和最小值进行标准化处理
    mins = np.percentile(matrix, 1, axis = 0)
    maxs = np.percentile(matrix, 99, axis = 0) - mins
    matrix = (matrix - mins[None, :]) / maxs[None, :]
    # 再将数据reshape成图像的大小
    matrix = np.reshape(matrix, [w, h, d])
    matrix = matrix.clip(0, 1)
    return matrix



def predict_model(batch_size = 1, input_size_height = 24, input_size_width = 24, input_passageway_num = 8):
    """
    该函数是构建预测模型
    Parameters
    ----------
        batch_size: 每次迭代样本数目
        input_size_height: 输入图像高度
        input_size_width: 输入图像宽度
        input_passageway_num: 输入图像通道数
    Returns
    -------
        predict: 预测模型的最终sigmod函数
        image_holder: 存储图像大小的数据结构
    """
    out_label_num = input_size_height * input_size_width
    image_holder = tf.placeholder(tf.float32, [batch_size, input_size_height, input_size_width, input_passageway_num])
    weight1 = variable_with_weight_loss(shape=[5, 5, input_passageway_num, 64], stddev=5e-2, wl=0)
    kernel1 = tf.nn.conv2d(image_holder, weight1, strides=[1, 1, 1, 1], padding='SAME')
    bias1 = tf.Variable(tf.constant(0.0, shape=[64]))
    conv1 = tf.nn.relu(tf.nn.bias_add(kernel1, bias1))
    pool1 = tf.nn.max_pool(conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
    norm1 = tf.nn.lrn(pool1, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75)

    weight2 = variable_with_weight_loss(shape=[5, 5, 64, 64], stddev=5e-2, wl=0)
    kernel2 = tf.nn.conv2d(norm1, weight2, strides=[1, 1, 1, 1], padding='SAME')
    bias2 = tf.Variable(tf.constant(0.1, shape=[64]))
    conv2 = tf.nn.relu(tf.nn.bias_add(kernel2, bias2))
    norm2 = tf.nn.lrn(conv2, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75)
    pool2 = tf.nn.max_pool(norm2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')

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
    # logits = tf.nn.relu(tf.matmul(local4, weight5) + bias5)
    logits = tf.matmul(local4, weight5) + bias5
    predict = tf.nn.sigmoid(logits)
    return predict, image_holder



def predict_final(each_weight = 24, each_width = 24, weight_step = 2, width_step = 2, gpu_index = "0"):
    """
    该函数是预测2015和2017图像拼接在一起的24*24的图像的结果，
    然后将结果拼接成一个矩阵，存储为tif格式
    Parameters
    ----------
        each_weight: 每个预测图像的高度
        each_width: 每个预测图像的宽度
        weight_step: 沿高度方向滑动步长
        width_step: 沿宽度方向滑动步长
        gpu_index: 使用gpu的编号
    """
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu_index
    im_2015 = tiff.imread(FILE_2015).transpose([1, 2, 0])
    im_2017 = tiff.imread(FILE_2017).transpose([1, 2, 0])
    a, b, c = im_2015.shape
    image_array = np.zeros((a, b))
    predict, image_holder = predict_model()
    print('each_pic_size =', each_weight * each_width, '=', each_weight, '*', each_width)
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction = 0.8)
    with tf.Session(config = tf.ConfigProto(gpu_options = gpu_options)) as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver()
        model_path = 'model0.ckpt'
        threshold = 0.5
        saver.restore(sess, model_path)
        init_time = time.time()
        num = 0
        print ('all=',int(((a - each_weight) / weight_step))*int((b - each_width) / width_step))
        last_time = time.time()
        for i in range(int(((a - each_weight) / weight_step))):
            for j in range(int((b - each_width) / width_step)):
                hs = i * weight_step
                he = hs + each_weight
                ws = j * width_step
                we = ws + each_width
                test_2015 = scale_percentile(im_2015[hs:he, ws:we, :])
                test_2017 = scale_percentile(im_2017[hs:he, ws:we, :])
                test_input = np.array([np.concatenate((test_2015, test_2017), axis = 2)])
                result = sess.run(predict, feed_dict = {image_holder: test_input}).flatten().reshape(24,24)
                image_array[hs:he, ws:we] += result
                num += 1
                if num % 1000 == 0:
                    this_time = time.time()
                    print (num,this_time-last_time,(this_time-init_time)*1000/num)
                    last_time=this_time
        image_array[image_array >= threshold] = 1
        image_array[image_array < threshold] = 0
        image_array = image_array.astype('uint8')
        img_out = Image.fromarray(image_array)
        img_out.save('result.tiff')
    # print((time.time() - init_time))
    # print('result=', type(result), result.shape)
    # result = result.flatten()
    # print(result.shape)
    # print(result[:10])
    # result = result.reshape(24, 24)
    # print(result.shape)
    # print('result =', result[:3, :3])


if __name__ == "__main__":
    predict_final()
