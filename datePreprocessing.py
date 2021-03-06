# coding:utf-8
# 该脚本用于数据预处理
# Author: gaochen3
# Date: 2017.12.22

import pandas as pd
import numpy as np
import warnings
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from IPython.display import display, HTML

NumericalFeatures = ["minute", "u_age", "z_age", "z_filtered_atten_num", "z_filtered_fans_num", "z_filtered_recip_num", "watch_num", "gift_amount", "like_num", "watch_time", "comment_num", "same_tag_num"]
CategoricalFeatures = ["u_gender", "u_prov_id",  "u_city_id", "z_gender", "z_user_type_id", "z_vuser_type_id","z_prov_id", "z_city_id", "u_z_prov_id", "u_z_city_id", "u_z_gender"]


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
    return data


def CrossFeatures(data):
    """
    增加主播和用户的交叉特征, 若省份ID相同则为1，若城市ID相同则为1，若性别相同则为1；
    计算主播和用户标签列表中相同的数目
    Parameters
    ----------
        data: 包含样本数据的dataframe
    Return
        result: 增加交叉特征之后的dataframe
    """
    data['u_z_prov_id'] = np.where(data['u_prov_id'] == data['z_prov_id'], 1, 0)
    data['u_z_city_id'] = np.where(data['u_city_id'] == data['z_city_id'], 1, 0)
    data['u_z_gender'] = np.where(data['u_gender'] == data['z_gender'], 1, 0)
    data['same_tag_num'] = [set(x[0].split(',')) & set(x[1].split(',')) for x in data[['u_tagscore', 'z_tagscore']].values]
    data['same_tag_num'] = data['same_tag_num'].str.len()
    data = data.drop(columns = ['u_tagscore', 'z_tagscore'])
    return data


def DataStandardScale(data):
    """
    对连续型特征进行标准化处理
    Parameters
    ----------
        data: 需要处理的样本数据
    Returns
    -------
        data: 经过标准化处理之后的数据
    """
    for ColumnName in NumericalFeatures:
        scaler = preprocessing.StandardScaler(with_mean = True, with_std = True).fit(data[ColumnName].values.reshape(-1, 1).astype(float))
        data[ColumnName + "_scaled"] = scaler.transform(data[ColumnName].values.reshape(-1, 1).astype(float))
        data = data.drop(columns = ColumnName)
    return data


def DataOneHotEncoder(data):
    """
    类别特征进行OneHot编码，不经过GBDT模型，直接和GBDT组合特征一起经过LR模型;
    先获取到每个类别特征包含的类别数目，然后进行转换为数字编码，再进行onehot编码
    Parameters
    ----------
        data: 样本特征数据
    Returns
    -------
        data: 经过OneHot编码处理之后的样本数据
    """
    for ColumnName in CategoricalFeatures:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            label_encoder = LabelEncoder()
            integer_encoded = label_encoder.fit_transform(data[ColumnName].values.reshape(-1, 1))
            onehot_encoder = OneHotEncoder(sparse = False)
            integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
            data[ColumnName + '_onehot'] = list(onehot_encoder.fit_transform(integer_encoded))
            data = data.drop(columns = ColumnName)


def DataPreprocessing(data_path):
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
    print("开始读取数据")
    data = ReadData(data_path)
    print("开始计算交叉特征")
    data = CrossFeatures(data)
    print("开始对特征进行标准化")
    data = DataStandardScale(data)
    print("开始对特征进行onehot编码")
    data = DataOneHotEncoder(data)
    # print(data)

if __name__ == "__main__":
    DataPreprocessing('/Users/gaochen3/sina_study/java_study/train.txt')