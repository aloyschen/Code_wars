# coding=utf-8
# 该脚本用于计算每五分钟的热门数据
# Author: gaochen3
# Date: 2017.12.14


import time
import click


def compute_time(file_data, start_time):
    """
    计算5分钟所有用户的停留时间，通过进入时间和退出时间计算
    Parameters
    ----------
        data_path: 数据文件路径
        start_time: 开始时间
    Return
    ------
        uid_staytime: 每个uid五分钟内的停留时间
    """
    last_uid, status = '', ''
    time_period = 300
    total_time, join_time, exit_time = 0, 0, 0
    uid_staytime = []
    for line in file_data:
        line = line.strip()
        data = line.split("\t")
        if len(data) != 4:
            continue
        if data[0] == 'NULL':
            continue
        time, uid, oper_type = int(data[0]), data[1], data[3]
        if time >= start_time and time <= int(start_time) + time_period:
            if last_uid != uid:
                if last_uid != '' and total_time > 0:
                    uid_staytime.append([last_uid, total_time])
                time, uid, oper_type = data[0], data[1], data[2]
                total_time = 0
                status = ''
                last_uid = uid
            if oper_type == 'join_room':
                join_time = time
                status = 'join_room'
            if oper_type == 'exit_room':
                exit_time = time
                if status == 'join_room':
                    total_time += int(exit_time) - int(join_time)
                status = 'exit_room'
    return uid_staytime



def compute_staytime(data_path, start_time, end_time):
    """
    计算一段时间内每隔五分钟的所有用户停留时间
    Parameters
    ----------
        start_time: 开始时间
        end_time: 结束时间
    Return
    ------
        None
    """
    file_data = open(data_path, encoding = 'utf-8').readlines()
    average_time = []
    while start_time < end_time:
        uid = []
        total_time = 0
        uid_time = compute_time(file_data, start_time)
        # print(uid_time)
        for element in uid_time:
            total_time += element[1]
            uid.append(element[0])
        time_local = time.localtime(start_time)
        print_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        average_time.append(total_time / len(set(uid)) / 60)
        print('start time: {0}, total stay time: {1}, average stay time: {2}'.format(print_time, total_time, total_time / len(set(uid)) / 60))
        start_time += 300
    median_time = get_median(average_time)
    print('median time: {0}'.format(median_time))


def compute_consumption(send_data_path, watch_data_path, start_time, end_time):
    """
    计算一段时间内每隔五分钟送礼的人数, 然后计算每五分钟的消费率(消费人数/累积观看人数)
    Parameters
    ----------
        start_time: 开始时间
        end_time: 结束时间
    Return
    ------
        None
    """
    file_data = open(send_data_path, encoding='utf-8').readlines()
    time_period = 300
    total_people = []
    total_watch_people = compute_watch_people(watch_data_path, start_time, end_time)
    while (start_time < end_time):
        send_uid = []
        for line in file_data:
            line = line.strip()
            data = line.split('\t')
            uid_time, uid = data[0], data[1]
            if uid_time == 'NULL':
                continue
            if int(uid_time) >= start_time and int(uid_time) <= start_time + time_period:
                send_uid.append(uid)
        time_local = time.localtime(start_time)
        print_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        print('Start time: {0} Total send gift people {1}'.format(print_time, len(set(send_uid))))
        total_people.append(len(set(send_uid)))
        start_time += time_period
    # print(len(total_people), '\t', len(total_watch_people))
    consumption = [send_people / watch_people for send_people in total_people
                   for watch_people in total_watch_people]
    median_people = get_median(consumption)
    print('median consumption: {0}'.format(median_people))

def compute_sendgift(send_data_path, start_time, end_time):
    """
    计算一段时间内每隔五分钟送礼的人数
    Parameters
    ----------
        start_time: 开始时间
        end_time: 结束时间
    Return
    ------
        None
    """
    file_data = open(send_data_path, encoding='utf-8').readlines()
    time_period = 300
    total_people = []
    while (start_time < end_time):
        send_uid = []
        for line in file_data:
            line = line.strip()
            data = line.split('\t')
            uid_time, uid = data[0], data[1]
            if uid_time == 'NULL':
                continue
            if int(uid_time) >= start_time and int(uid_time) <= start_time + time_period:
                send_uid.append(uid)
        time_local = time.localtime(start_time)
        print_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        print('Start time: {0} Total send gift people {1}'.format(print_time, len(set(send_uid))))
        total_people.append(len(set(send_uid)))
        start_time += time_period
    median_people = get_median(total_people)
    print('median consumption: {0}'.format(median_people))

def compute_clickpv(data_path, start_time, end_time):
    """
    计算一段时间内的点击率
    Parameters
    ----------
        start_time: 开始时间
        end_time: 结束时间
    Return
    ------
        None
    """
    file_data = open(data_path, encoding='utf-8').readlines()
    time_period = 300
    total_click = []
    while (start_time < end_time):
        show_num = 0
        click_num = 0
        send_uid = []
        for line in file_data:
            line = line.strip()
            data = line.split('\t')
            uid_time, action = data[0], data[1]
            if uid_time == 'NULL':
                continue
            if int(uid_time) >= start_time and int(uid_time) <= start_time + time_period:
                if action == '26':
                    show_num += 1
                elif action == '1481':
                    click_num += 1
        time_local = time.localtime(start_time)
        print_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        if click_num == 0:
            total_click.append(0)
        elif show_num == 0:
            total_click.append(0)
        else:
            print('Start time: {0} click_num: {1} show_num: {2} clickPV {3}'.format(print_time, click_num, show_num, click_num / show_num))
            total_click.append(click_num / show_num)
        start_time += time_period
    median_people = get_median(total_click)
    print('median click PV: {0}'.format(median_people))


def compute_watch_people(data_path, start_time, end_time):
    """
    计算一段时间内每隔五分钟的观看人数
    Parameters
    ----------
        start_time: 开始时间
        end_time: 结束时间
    Return
    ------
        每五分钟的总观看人数
    """
    file_data = open(data_path, encoding='utf-8').readlines()
    time_period = 300
    total_watch_people = []
    while (start_time < end_time):
        watch_uid = []
        for line in file_data:
            line = line.strip()
            data = line.split('\t')
            if len(data) != 4:
                continue
            uid_time, uid = data[0], data[1]
            if uid_time == 'NULL':
                continue
            if int(uid_time) >= start_time and int(uid_time) <= start_time + time_period:
                watch_uid.append(uid)
        time_local = time.localtime(start_time)
        print_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        print('Start time: {0} Total watch people number {1}'.format(print_time, len(set(watch_uid))))
        total_watch_people.append(len(set(watch_uid)))
        start_time += time_period
    print(len(total_watch_people))
    return total_watch_people


def compute_giftamount(data_path, start_time, end_time):
    """
    计算一段时间内每隔五分钟的消费金额
    Parameters
    ----------
        start_time: 开始时间
        end_time: 结束时间
    Return
    ------
        None
    """
    file_data = open(data_path, encoding='utf-8').readlines()
    time_period = 300
    total_amount = []
    while (start_time < end_time):
        total_gift = 0
        for line in file_data:
            line = line.strip()
            data = line.split('\t')
            if len(data) != 3:
                continue
            uid_time, gift_amount = data[0], data[2]
            if int(uid_time) >= start_time and int(uid_time) <= start_time + time_period:
                total_gift += int(gift_amount)
        time_local = time.localtime(start_time)
        print_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        print('Start time: {0} Total gift amount: {1}'.format(print_time, total_gift))
        total_amount.append(total_gift)
        start_time += time_period
    median_gift = get_median(total_amount)
    print('median gift amount: {0}'.format(median_gift))

def get_median(data):
    """
    针对奇数和偶数的列表情况获取中位数
    Parameters
    ----------
        data: 包含数据的列表
    Return
    ------
        列表中数据的中位数
    """
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2


@click.command()
@click.option('-d', '--data', help = "互动行为数据文件路径", prompt = True)
@click.option('-w', '--watch_data', help = "观看时间数据文件路径", prompt = True)
@click.option('-p', '--option', help = "StayTime -> 计算停留时间, "
                                       "SendGiftPeople -> 计算送礼人数, "
                                       "CommentRate -> 计算评论率"
                                       "FollowRate -> 计算关注率"
                                       "GiftAmount -> 计算礼物金额"
                                       "ClickPV -> 计算点击率"
                                       "Consumption -> 计算消费率", type = click.Choice(['StayTime', 'SendGiftPeople', 'CommentRate', 'FollowRate', 'GiftAmount', 'ClickPV', 'Consumption']), prompt = True)
@click.option('-s', '--start', help = "start time 开始时间戳", prompt = True)
@click.option('-e', '--end', help = "end time 结束时间戳", prompt = True)
def compute(option, data, start, end, watch_data=''):
    """
    通过不同的命令行参数执行不同的函数
    Parameters
    ----------
        data: 文件存储路径
        option: 根据不同的输入参数计算对应的数据
        start: 开始时间
        end: 结束时间
    Returns
    -------
        None
    """
    if option == "StayTime":
        compute_staytime(data, int(start), int(end))
    elif option == "SendGiftPeople":
        compute_sendgift(data, int(start), int(end))
    elif option in ['CommentRate', 'FollowRate', 'Consumption']:
        compute_consumption(data, watch_data, int(start), int(end))
    elif option == "ClickPV":
        compute_clickpv(data, int(start), int(end))
    elif option == "GiftAmount":
        compute_giftamount(data, int(start), int(end))


if __name__ == '__main__':
    compute()
    compute_clickpv('./uid_click_20.txt', 1513080000, 1513087200)
