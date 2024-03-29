import matplotlib.pyplot as plt
import numpy as np
import main


def plot_bar(data_sent, data_recv, measure_unit):
    if measure_unit == 1:
        unit = "Bytes"
    elif measure_unit == 2:
        unit = "KB"
    elif measure_unit == 3:
        unit = "MB"
    else:
        unit = "GB"
    fig, ax = plt.subplots()
    names = list(data_sent.keys())
    x = np.arange(len(names))  # the label locations
    width = 0.35
    values = list(data_sent.values())
    rects1 = ax.bar(x - width / 2, values, label='Sent', width=width)
    values = list(data_recv.values())
    rects2 = ax.bar(x + width / 2, values, label='Received', width=width)
    ax.set_ylabel('Data (in ' + unit + ')')
    ax.set_title('Data usage by time')
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.legend()
    auto_label(rects1, ax)
    auto_label(rects2, ax)
    fig.tight_layout()
    plt.show()
    main.main_gui()


def auto_label(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def check_multiple(data_type):
    dates_arr = []
    if data_type == "sent":
        f = open("data_sent.data", "r")

    else:
        f = open("data_recv.data", "r")
    for line in f:
        if line[0] == "#":
            dates_arr.append(line.replace("#", ""))
    return dates_arr


def data_extract(data_type, measure_unit, date_str):
    dict = {}
    if date_str is None:
        extract = True
    else:
      extract = False
    if data_type == "sent":
        f = open("data_sent.data", "r")

    else:
        f = open("data_recv.data", "r")
    if measure_unit == 1:
        measure_convert = 1
    elif measure_unit == 2:
        measure_convert = 1000
    elif measure_unit == 3:
        measure_convert = 1000000
    else:
        measure_convert = 1000000000
    for line in f:
        if line[0] == "#" and date_str is not None:
            if line.replace("#", "") == date_str:
                extract = True
            else:
                extract = False
        if extract and line[0] != "#":
            (val, key) = line.strip("\n").split("*")
            val = float(val) / measure_convert
            dict[key] = val

    return dict
