import psutil
import time
import os


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
