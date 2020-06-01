import psutil
import time
import os
def update(): #stores psutil.net_io_counters into value and returns it
              #also sets global update_time to time.ctime()
	global time_string
	os.system('cls')
	update_time = time.localtime()
	time_string = time.strftime("%H:%M:%S", update_time)
	value = psutil.net_io_counters()
	return value
def start_daemon(): #runs the main daemon for monitoring the bandwith	
	first = True
	old_sent = update().bytes_sent
	old_recv = update().bytes_recv
	monitor_time = int(input("Please insert monitor time (in secondes)"))
	data_sent = {}
	data_recv = {}
	f = open("data_sent.data", "w")
	f2 = open("data_recv.data","w")
	index = 0
	try:
		while True:
			index +=1
			print("Monitoring...")
			if not first:
				time.sleep(monitor_time)
			first = False
			value = update()
			recv = (float(value.bytes_recv) - old_recv) /1000
			sent = (float(value.bytes_sent) - old_sent) /1000
			old_recv = value.bytes_recv
			old_sent = value.bytes_sent
			print(time_string)
			data_sent[time_string] = sent
			data_recv[time_string] = recv
			print("Sent: " + str(sent) +"MB")
			print("Recieved: "+ str(recv) + "MB")
			print("Script ran for: " + str(index) + " times")
			
			
			
	except KeyboardInterrupt:
		print("done monitoring.")
	f.write(str(data_sent))
	f2.write(str(data_recv))
	f.close()
	f2.close()

