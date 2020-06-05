import psutil
import time
import math
import os
import os.path
import daemon
import stats

ASCII_INTRO = """    ____                  __         _ __  __       __  ___            _ __            
   / __ )____ _____  ____/ /      __(_) /_/ /_     /  |/  /___  ____  (_) /_____  _____
  / __  / __ `/ __ \/ __  / | /| / / / __/ __ \   / /|_/ / __ \/ __ \/ / __/ __ \/ ___/
 / /_/ / /_/ / / / / /_/ /| |/ |/ / / /_/ / / /  / /  / / /_/ / / / / / /_/ /_/ / /    
/_____/\__,_/_/ /_/\__,_/ |__/|__/_/\__/_/ /_/  /_/  /_/\____/_/ /_/_/\__/\____/_/     
                                                                                       

"""


def run_program():
    while True:
        os.system('cls')
        print(ASCII_INTRO)
        try:
            monitor_time = int(input("Please specify your intervals (time between each scan, in whole secondes!)"))
            break
        except ValueError:
            continue
    while True:
        os.system('cls')
        print(ASCII_INTRO)
        try:
            print("Which unit of measurement would you like to use?")
            print("1.byte")
            print("2.KiloByte (KB)")
            print("3.MegaByte (MB)")
            print("4.GigaByte (GB)")
            measure_unit = int(input())
            if 1 <= measure_unit <= 4:
                break
            else:
                continue
        except ValueError:
            continue
    daemon.start_daemon(monitor_time, measure_unit)
    data_sent = stats.data_extract('sent')
    data_recv = stats.data_extract('recv')
    stats.plot_bar(data_sent, data_recv, measure_unit)
    os.system('cls')


def main():
    print(ASCII_INTRO)
    time.sleep(1.6)
    data_exist = False
    while True:
        if os.path.exists('data_sent.data'):
            data_exist = True
        os.system('cls')
        print(ASCII_INTRO)
        print("Menu:")
        print("1.Start monitoring")
        print("2.Help")
        print("3.Exit")
        try:
            choice = int(input())
        except ValueError:
            continue
        if choice == 3:
            try:
                os.remove("data_recv.data")
                os.remove("data_sent.data")
            except OSError:
                pass
            print('Ciao!')
            break
        elif choice == 1:
            run = True
        elif choice == 2:
            os.system('cls')
            print(ASCII_INTRO)
            print("Help")
            print("______")
            print("""Bandwidth monitor is an application which monitors your sent and received packets in intervals of 
    your choosing. It will then show you the results in a graph using your desired units of measurement.""")
            input("Press any key to continue...")
            continue
        else:
            continue

        if run:
            run_program()


if __name__ == "__main__":
    main()
else:
    pass
