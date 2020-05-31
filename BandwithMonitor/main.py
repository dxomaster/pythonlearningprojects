import psutil  
import time
import math
import os
import matplotlib.pyplot as plt  
import ast
import daemon


try:
	daemon.daemon()
except KeyboardInterrupt:
	os.system('cls')
	print("done monitoring.")
time.sleep(5)