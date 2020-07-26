import os
import os.path
import daemon
import stats
from tkinter import *
from tkinter import messagebox
from resources.AnimatedGif import *


def stop_running():
    result = messagebox.askyesno("Data save", "Do you wish to clear your data?")
    if result:
        try:
            os.remove("data_recv.data")
            os.remove("data_sent.data")
        except OSError:
            pass
    sys.exit()


def check_input(monitor_time, measure_unit, app):
    try:
        monitor_time = int(monitor_time.get())
        measure_unit = int(measure_unit.get())
    except ValueError:
        messagebox.showerror("", "Input Error")
    else:
        daemon.daemon_gui(monitor_time, measure_unit, app)


def run_wizard(app):  # TODO add a more asthetic way to choose monitor_time dropdown ?
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
    wizard_button = Button(wizard_app, text="Enter",
                           command=lambda: check_input(monitor_time, measure_unit, wizard_app))
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
It will then show you the results in a bar graph with your desired units of measurement.""",
                        font=("Arial", 10)).grid(columnspan=3)
    exit_button = Button(help_app, text="Close", font=("Arial", 8), command=help_app.destroy)
    exit_button.grid(row=3, column=1)
    help_app.mainloop()


def run_extraction(measure_unit, app=None, date_str=None):
    if isinstance(measure_unit, StringVar):
        measure_unit = int(measure_unit.get())
    if app is not None:
        app.destroy()
    data_sent = stats.data_extract('sent', measure_unit, date_str)
    data_recv = stats.data_extract('recv', measure_unit, date_str)
    stats.plot_bar(data_sent, data_recv, measure_unit)


def data_handle(app, measure_unit=0):
    app.destroy()
    date_arr = stats.check_multiple('sent')
    date_choose_app = Tk()
    date_chose = tk.StringVar(date_choose_app)
    date_chose.set(date_arr[0])
    date_list = tk.OptionMenu(date_choose_app, date_chose, *date_arr)
    date_list.grid(column=1, row=2)
    date_choose_label = Label(date_choose_app,
                              text="Multiple recordings detected, please choose a date to load",
                              font=("Arial", 10))
    date_choose_label.grid(column=1, row=1)
    if measure_unit == 0:
        measure_unit = StringVar(date_choose_app, "2")
        wizard_radio1 = Radiobutton(date_choose_app, variable=measure_unit, text="Bytes", value="1")
        wizard_radio1.grid(column=1, row=3, )
        wizard_radio2 = Radiobutton(date_choose_app, variable=measure_unit, text="KB", value="2")
        wizard_radio2.grid(column=1, row=4, )
        wizard_radio3 = Radiobutton(date_choose_app, variable=measure_unit, text="MB", value="3")
        wizard_radio3.grid(column=1, row=5, )
        wizard_radio4 = Radiobutton(date_choose_app, variable=measure_unit, text="GB", value="4")
        wizard_radio4.grid(column=1, row=6)
    confirm_button = Button(date_choose_app, text="Enter",
                            command=lambda: run_extraction(measure_unit, date_choose_app,
                                                           str(date_chose.get())))
    confirm_button.grid(column=1, row=7)
    date_choose_app.mainloop()


def existing_data(app):
    f = open("data_recv.data", "r")
    date_arr = stats.check_multiple('sent')
    date = ""
    for item in date_arr:
        date = date + "\n" + item
    result = messagebox.askyesno(None, "Existing data date: " + date + "\n Do you wish to continue?")
    if result:
        data_handle(app)
    else:
        pass


def main_gui():
    app_window = Tk()
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
    if os.path.isfile("data_sent.data"):
        old_data_button = Button(app_window, text="Use existing data", width=35, font=("Arial", 8),
                                 command=lambda: existing_data(app_window))
        old_data_button.grid(row=3, column=1)
        exit_button.grid(row=4, column=1)
    app_window.mainloop()


if __name__ == "__main__":
    main_gui()
else:
    pass
