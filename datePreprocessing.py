# coding:utf-8
# 该脚本用于数据预处理
# Author: gaochen3
# Date: 2017.12.22

import pandas as pd
from sklearn import preprocessing


def ReadData(data_path):
    """
    将数据读取进pandas的dataframe中, 并去除样本中包含null的值
    Parameters
    ----------
        data_path: 数据文件路径
    Returns
    -------
        data: 存储所有样本的数据
    """
    columns_name = ['label', 'uid', "zuid", "minute", "u_age", "u_gender",
                "u_prov_id", "u_city_id", "z_age", "z_gender", "z_user_type_id", "z_vuser_type_id",
                "z_prov_id", "z_city_id", "z_filtered_atten_num", "z_filtered_fans_num",
                "z_filtered_recip_num", "watch_num", "gift_amount", "like_num", "watch_time",
                "comment_num", "u_tagscore", "z_tagscore"]
    data = pd.read_csv(data_path, header = None, sep = '\t', names = columns_name)
    data = data.dropna(how = 'all')
    # print(data['u_prov_id'].value_counts())
    # scaler = preprocessing.StandardScaler(with_mean = True, with_std = True).fit(data['minute'].values.reshape(-1, 1))
    # test = scaler.transform(data['minute'].values.reshape(-1, 1))
    # print('转换前：\n {} \n 转化后：\n {}'.format(data['minute'].values.reshape(-1, 1), test))
    return data


def CrossFeatures(data):
    """
    增加主播和用户的交叉特征
    :param data:
    :return:
    """

def DataPreprocessing(data):
    """
    对数据进行预处理，包括一下几个步骤：
    1、根据用户和主播的城市、性别信息增加交叉特征；
    2、计算用户和主播标签相同数目；
    3、对连续数据进行归一化处理；
    4、对类别特征进行onehot编码：
    连续特征使用GBDT模型组合，然后和经过ont_hot编码的类别特征一起通过LR模型进行处理
    Parameters
    ----------
        data: 包含所有样本数据的dataframe
    Returns
    -------

    """

if __name__ == "__main__":
    ReadData('/Users/gaochen3/sina_study/java_study/train.txt')
