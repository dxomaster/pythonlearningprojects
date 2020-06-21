import os
import os.path
import daemon
import stats
from tkinter import *
from tkinter import messagebox
from resources.AnimatedGif import *
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
        run_program()


def stop_running():
    try:
        os.remove("data_recv.data")
        os.remove("data_sent.data")
    except OSError:
        pass
    sys.exit()


def check_input(monitor_time, measure_unit,app):
    try:
        monitor_time = int(monitor_time.get())
        measure_unit = int(measure_unit.get())
    except ValueError:
        messagebox.showerror("", "Input Error")
    else:
        daemon.daemon_gui(monitor_time, measure_unit,app)



def run_wizard(app):
    app.destroy()
    wizard_app = Tk()
    monitor_time = StringVar(wizard_app)
    measure_unit = StringVar(wizard_app, "1")
    wizard_app.title("Daemon setup")
    wizard_app.resizable(width=False, height=False)
    wizard_label = Label(wizard_app, text="Wizard", justify="left", font=("Arial", 22, "bold", "underline"))
    wizard_label.grid(column=0)
    wizard_label2 = Label(wizard_app, justify="left", text="""Please specify your intervals (time between each scan, 
in whole secondes!)""", font=("Arial", 8))
    wizard_label2.grid(column=0)
    wizard_input = Entry(wizard_app, textvariable=monitor_time)
    wizard_input.grid(column=0, row=2, sticky=W)
    wizard_radio1 = Radiobutton(wizard_app, variable=measure_unit, text="Bytes", value="1")
    wizard_radio1.grid(column=0, row=3, sticky=W)
    wizard_radio2 = Radiobutton(wizard_app, variable=measure_unit, text="KB", value="2")
    wizard_radio2.grid(column=0, row=4, sticky=W)
    wizard_radio3 = Radiobutton(wizard_app, variable=measure_unit, text="MB", value="3")
    wizard_radio3.grid(column=0, row=5, sticky=W)
    wizard_radio4 = Radiobutton(wizard_app, variable=measure_unit, text="GB", value="4")
    wizard_radio4.grid(column=0, row=6, sticky=W)
    wizard_button = Button(wizard_app, text="Enter", command=lambda: check_input(monitor_time, measure_unit,wizard_app))
    wizard_button.grid(column=1, row=4)
    wizard_app.mainloop()


def help_window():
    help_app = Tk()
    help_app.title("Help")
    help_app.resizable(width=False, height=False)
    help_label = Label(help_app, text="Help", font=("Arial", 22, "bold", "underline"))
    help_label.grid(column=1)
    help2_label = Label(help_app, justify="left", text="""Bandwidth monitor is an application which monitors your sent 
and received packets at intervals of your choosing.
It will then show you the results in a graph using your desired units of measurement.""",
                        font=("Arial", 10)).grid(columnspan=3)
    exit_button = Button(help_app, text="Close", font=("Arial", 8), command=help_app.destroy)
    exit_button.grid(row=3, column=1)
    help_app.mainloop()


def main_gui():

    app_window = Tk()
  # loading = AnimatedGif(app_window, 'resources/loading.gif', 0.04)
   # loading.grid(row=0, column=0)
    #loading.start()
    app_window.resizable(width=False, height=False)
    app_window.title("BandwidthMonitor")
    menu_label = Label(app_window, text="Menu", font=("Arial", 22, "bold", "underline"))
    menu_label.grid(column=1)
    run_button = Button(app_window, text="Run", width=35, command=lambda: run_wizard(app_window), font=("Arial", 8))
    run_button.grid(row=1, column=1)
    help_button = Button(app_window, text="Help", justify="center", width=35, font=("Arial", 8), command=help_window)
    help_button.grid(row=2, column=1)
    exit_button = Button(app_window, text="Exit", width=35, font=("Arial", 8), command=lambda: stop_running())
    exit_button.grid(row=3, column=1)
    app_window.mainloop()


if __name__ == "__main__":
    main_gui()
else:
    pass
