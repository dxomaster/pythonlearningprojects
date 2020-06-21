import psutil
import os
# from mttkinter import mtTkinter as tk
from tkinter import *
# from tkinter import ttk
from resources.AnimatedGif import *
import stats
import threading


def update():  # stores psutil.net_io_counters into value and returns it
    # also sets global update_time to time.ctime()
    # noinspection PyGlobalUndefined
    global time_string
    os.system('cls')
    update_time = time.localtime()
    time_string = time.strftime("%H:%M:%S", update_time)
    value = psutil.net_io_counters()
    return value


def start_daemon(monitor_time, measure_unit):  # runs the main daemon for monitoring the bandwidth
    if measure_unit == 1:
        measure_convert = 1
        unit = "Bytes"
    elif measure_unit == 2:
        measure_convert = 1000
        unit = "KB"
    elif measure_unit == 3:
        measure_convert = 1000000
        unit = "MB"
    elif measure_unit == 4:
        measure_convert = 1000000000
        unit = "GB"
    first = True
    old_sent = update().bytes_sent
    old_recv = update().bytes_recv
    data_sent = {}
    data_recv = {}
    f = open("data_sent.data", "w")
    f2 = open("data_recv.data", "w")
    index = 0
    try:
        while True:
            index += 1
            print("Monitoring... , press CTRL + C to finish.")
            if not first:
                time.sleep(monitor_time)
            first = False
            value = update()
            recv = (float(value.bytes_recv) - old_recv) / measure_convert
            sent = (float(value.bytes_sent) - old_sent) / measure_convert
            old_recv = value.bytes_recv
            old_sent = value.bytes_sent
            print(time_string)
            data_sent[time_string] = sent
            data_recv[time_string] = recv
            print("Sent: " + str(sent) + unit)
            print("Received: " + str(recv) + unit)
            print("Script ran for: " + str(index) + " times")
    except KeyboardInterrupt:
        print("done monitoring.")
    f.write(str(data_sent))
    f2.write(str(data_recv))
    f.close()
    f2.close()


def daemon_gui(monitor_time, measure_unit, app):
    app.destroy()
    daemon_app = Tk()
    daemon_app.resizable(height=True, width=True)
    daemon_app.title("monitoring...")
    load = AnimatedGif(daemon_app, 'resources/loading.gif', 0.04)
    load.grid(row=1, column=1)

    monitor_label = tk.Label(daemon_app, text="Monitoring", font=("Arial", 22, "bold", "underline"))
    dynamic_monitor_label = tk.Label(daemon_app, font=("Arial", 8))
    dynamic_monitor_label.grid(row=1, column=1)
    monitor_label.grid(row=0, column=1)
    x = threading.Thread(target=run_process, args=(monitor_time, measure_unit, dynamic_monitor_label,load),
                        daemon=True)
    stop_button = tk.Button(daemon_app, text="Stop", command=lambda: stop_process(measure_unit, daemon_app))
    stop_button.grid(row=3, column=1)
    x.start()
    daemon_app.mainloop()


def data_handle(measure_unit, app):
    app.destroy()
    data_sent = stats.data_extract('sent')
    data_recv = stats.data_extract('recv')

    stats.plot_bar(data_sent, data_recv, measure_unit)


def stop_process(measure_unit, app):
    global run
    run = False
    app.after(2000, lambda: data_handle(measure_unit, app))


def run_process(monitor_time, measure_unit, dynamic_monitor_label,load):
    load.start()
    global run
    run = True
    first = True
    index = 0
    data_sent = {}
    data_recv = {}
    f = open("data_sent.data", "w")
    f2 = open("data_recv.data", "w")
    old_sent = update().bytes_sent
    old_recv = update().bytes_recv
    if measure_unit == 1:
        measure_convert = 1
        unit = "Bytes"
    elif measure_unit == 2:
        measure_convert = 1000
        unit = "KB"
    elif measure_unit == 3:
        measure_convert = 1000000
        unit = "MB"
    else:
        measure_convert = 1000000000
        unit = "GB"
    while run:
        index += 1
        if not first:
            time.sleep(monitor_time)
        first = False
        value = update()
        recv = (float(value.bytes_recv) - old_recv) / measure_convert
        sent = (float(value.bytes_sent) - old_sent) / measure_convert
        old_recv = value.bytes_recv
        old_sent = value.bytes_sent
        print(time_string)
        data_sent[time_string] = sent
        data_recv[time_string] = recv
        label_string = time_string + "\n" + "Sent:" + str(sent) + unit + "\n" + "Received: " + str(recv) + unit + "\n"
        label_string += "Script ran for: " + str(index) + " times"
        dynamic_monitor_label.config(text=label_string)
        print("Sent: " + str(sent) + unit)
        print("Received: " + str(recv) + unit)
        print("Script ran for: " + str(index) + " times")
    f.write(str(data_sent))
    f2.write(str(data_recv))
    f.close()
    f2.close()
