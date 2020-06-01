import psutil  
import time
import math
import os
import daemon
import stats
ASCII_INTRO = """    ____                  __         _ __  __       __  ___            _ __            
   / __ )____ _____  ____/ /      __(_) /_/ /_     /  |/  /___  ____  (_) /_____  _____
  / __  / __ `/ __ \/ __  / | /| / / / __/ __ \   / /|_/ / __ \/ __ \/ / __/ __ \/ ___/
 / /_/ / /_/ / / / / /_/ /| |/ |/ / / /_/ / / /  / /  / / /_/ / / / / / /_/ /_/ / /    
/_____/\__,_/_/ /_/\__,_/ |__/|__/_/\__/_/ /_/  /_/  /_/\____/_/ /_/_/\__/\____/_/     
                                                                                       

"""
os.system('cls')
print(ASCII_INTRO)
time.sleep(1.5)
run = True
while run:
	while True:
		os.system('cls')
		try:
			monitor_time = int(input("Please specify your monitor timing (time between each scan, in whole secondes!)"))
			break
		except ValueError:
			continue
	while True:
		os.system('cls')
		try:
			print("Which unit of measurement would you like to use?")
			print("1.byte")
			print("2.MegaByte (MB)")
			print("3.GigaByte (GB)")
			measure_unit = int(input())
			if 1<=measure_unit<=3:	
				break
			else:
				continue
		except ValueError:
			print("Invalid input. Try again please.")
			continue
	daemon.start_daemon(monitor_time,measure_unit)		
	data_sent = stats.data_extract('sent')
	data_recv = stats.data_extract('recv')
	stats.plot_bar(data_sent,data_recv,measure_unit)
	os.system('cls')
	while True:
		restart = input("Run again? y/n")
		if restart == 'y':	
			break
		elif restart =='n':
			run = False
			os.system('cls')
			break
		else:
			print("Y/N only.")
			continue
print('Ciao!')
