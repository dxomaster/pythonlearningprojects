import ast
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


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
    x = np.arange(len(data_sent))  # the label locations
    width = 0.35
    names = list(data_sent.keys())
    values = list(data_sent.values())
    rects1 = ax.bar(x - width / 2, values, width, label='Sent')
    values = list(data_recv.values())
    rects2 = ax.bar(x + width / 2, values, width, label='Received')
    ax.set_ylabel('Data (in ' + unit + ')')
    ax.set_title('Data usage by time')
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.legend()
    auto_label(rects1, ax)
    auto_label(rects2, ax)
    fig.tight_layout()
    plt.show()


def auto_label(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def data_extract(data_type):
    if data_type == "sent":
        f = open("data_sent.data", "r")

    else:
        f = open("data_recv.data", "r")
    data_str = str(f.read())
    data = ast.literal_eval(data_str)
    return data
