import psutil  
import time
import math
import os
import daemon
import stats


daemon.start_daemon()
data_sent = stats.data_extract('sent')
data_recv = stats.data_extract('recv')
stats.plot_bar(data_sent,data_recv)
os.system('cls')