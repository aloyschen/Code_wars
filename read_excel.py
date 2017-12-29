import xlrd
import xlwt
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
# 设置中文显示字体
font = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc')

def read_excel(file_path):
    """
    读取excel文件中每行的第一列的uid
    :param file_path:
    :return:
    """
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    uid = []
    result = ''
    for row in range(table.nrows):
        row_value = table.row_values(row)
        row_data = str(row_value[0]).split(',')
        uid.append(row_data[0])
        # print(row_data)
        # print("uid: {}".format(row_data[0]))
    count = 0
    for element in uid:
        result += "'" + str(round(float(element))) +"',"
        count += 1
        if count % 10 == 0:
            result += "\n"
    print(result)


def write_excel(data_path, save_path):
    """

    :param data_path:
    :param save_path:
    :return:
    """
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("sheet1", cell_overwrite_ok = True)
    all_data = []
    cols, rows = 3, 0
    for line in open(data_path).readlines():
        line = line.strip()
        uid, data = line.split("\t")
        date, hour = data.split(" ")
        all_data.append([date, uid, hour])
    rows = len(all_data)
    print(rows)
    for row in range(rows):
        data_row = all_data[row]
        for col in range(cols):
            sheet.write(row, col, data_row[col])
    workbook.save(save_path)



def plot_pircture(data_path):
    """

    :param data_path:
    :param save_path:
    :return:
    """
    per_hour_people = {}
    per_hour_session = {}
    for hour in range(10):
        per_hour_people['0' + str(hour)] = []
        per_hour_session['0' + str(hour)] = []
    for hour in range(10, 24):
        per_hour_people[str(hour)] = []
        per_hour_session[str(hour)] = []
    print(per_hour_session)
    for line in open(data_path).readlines():
        line = line.strip()
        uid, data = line.split("\t")
        date, hour = data.split(" ")
        hour = hour.split(":")[0]
        per_hour_people[hour].append(uid)
    data = []
    for key in per_hour_people:
        data.append(len(set(per_hour_people[key])))
    print(data)
    plt.plot(list(per_hour_people.keys()), data, color = "red", linewidth = 2)
    print("{}:00".format(list(per_hour_people.keys())))
    plt.xticks(range(24), ("{}".format(element) for element in list(per_hour_people.keys())))
    plt.xlabel("时间(单位:小时)", fontproperties = font)
    plt.ylabel("人数(一个月内)", fontproperties = font)
    plt.title("主播人数分布曲线", fontproperties = font)
    plt.show()



if __name__ == '__main__':
    # read_excel('./test.xlsx')
    # write_excel('./zuid_starttime.txt', 'test.xlsx')
    plot_pircture('./zuid_starttime.txt')