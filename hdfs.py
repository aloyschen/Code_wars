# coding:utf-8
# 该脚本用户hadoop集群文件大小监控
# Author: gaochen3
# Date: 2018.01.19

import subprocess

hdfs_file_path = '/user_ext/weibo_multimedia_live/'

def run_cmd(args_list):
    """
    执行Linux的shell命令
    Parameters
    ----------
        args_list: shell命令列表
    Returns
    -------
        s_return: 返回代码
        s_output: std输出
        s_err: std错误输出
    """
    # import subprocess
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return = proc.returncode
    return s_return, s_output, s_err


def hdfs_all_file():
    """
    该函数是显示hdfs上所有文件的大小
    """
    (ret, out, err) = run_cmd(['hdfs', 'dfs', '-du', '-h', hdfs_file_path])
    lines = str(out).split('\\n')
    print(lines[0].split('\t'))


if __name__ == '__main__':
    hdfs_all_file()
