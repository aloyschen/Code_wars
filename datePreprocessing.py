# coding:utf-8
# 该脚本用于数据预处理
# Author: gaochen3
# Date: 2017.12.22

import pandas as pd
from sklearn import preprocessing


def read_data(data_path):
    """
    将数据读取进pandas的dataframe中
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
    print(data['u_prov_id'].value_counts())
    # scaler = preprocessing.StandardScaler(with_mean = True, with_std = True).fit(data['minute'].values.reshape(-1, 1))
    # test = scaler.transform(data['minute'].values.reshape(-1, 1))
    # print('转换前：\n {} \n 转化后：\n {}'.format(data['minute'].values.reshape(-1, 1), test))
    return data


if __name__ == "__main__":
    read_data('/Users/gaochen3/sina_study/java_study/train.txt')
