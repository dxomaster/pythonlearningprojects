import psutil
from tkinter import *
from resources.AnimatedGif import *
import threading
import main


def update():  # stores psutil.net_io_counters into value and returns it
    # also sets global update_time to time.ctime()
    # noinspection PyGlobalUndefined
    global time_string
    update_time = time.localtime()
    time_string = time.strftime("%H:%M:%S", update_time)
    value = psutil.net_io_counters()
    return value


def daemon_gui(monitor_time, measure_unit, app):
    app.destroy()
    daemon_app = Tk()
    daemon_app.resizable(height=False, width=False)
    daemon_app.title("monitoring...")
    monitor_label = tk.Label(daemon_app, text="Monitoring", font=("Arial", 22, "bold", "underline"))
    dynamic_monitor_label = tk.Label(daemon_app, font=("Arial", 8))
    dynamic_monitor_label.grid(row=2, column=1)
    monitor_label.grid(row=0, column=1)
    x = threading.Thread(target=run_process, args=(monitor_time, measure_unit, dynamic_monitor_label, daemon_app),
                         daemon=True)
    stop_button = tk.Button(daemon_app, text="Stop", command=lambda: stop_process(dynamic_monitor_label))
    stop_button.grid(row=3, column=1)
    x.start()
    daemon_app.mainloop()


def stop_process(dynamic_monitor_label):
    global run
    run = False
    dynamic_monitor_label.config(text="Finishing last monitor check, hang tight...")


def run_process(monitor_time, measure_unit, dynamic_monitor_label,
                app):
    load = AnimatedGif(app, 'resources/loading.gif', 0.04)
    load.grid(row=1, column=1)
    load.start_thread()
    global run
    run = True
    first = True
    index = 0
    data_sent = {}
    data_recv = {}
    f = open("data_sent.data", "a")
    f2 = open("data_recv.data", "a")
    old_sent = update().bytes_sent
    old_recv = update().bytes_recv
    if measure_unit == 1:
        unit = "Bytes"
    elif measure_unit == 2:
        unit = "KB"
    elif measure_unit == 3:
        unit = "MB"
    else:
        unit = "GB"
    while run:
        index += 1
        if not first:
            time.sleep(monitor_time)
        else:
            first = False
            time_signature = time.strftime("%e/%m/%Y %H:%M:%S", time.localtime())
            f.write("#" + time_signature + "\n")
            f2.write("#" + time_signature + "\n")
        value = update()
        recv = (float(value.bytes_recv) - old_recv)
        sent = (float(value.bytes_sent) - old_sent)
        old_recv = value.bytes_recv
        old_sent = value.bytes_sent
        f.write(str(sent) + "*" + str(time_string) + "\n")
        f2.write(str(recv) + "*" + str(time_string) + "\n")
        data_sent[time_string] = sent
        data_recv[time_string] = recv
        label_string = time_string + "\n" + "Sent:" + str(sent) + unit + "\n" + "Received: " + str(recv) + unit + "\n"
        label_string += "Script ran for: " + str(index) + " times"
        dynamic_monitor_label.config(text=label_string)
    load.stop_thread()
    f.close()
    f2.close()
    app.after(1, lambda: main.data_handle(app, measure_unit))
