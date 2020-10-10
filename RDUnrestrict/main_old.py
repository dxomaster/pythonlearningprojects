import json
import tkinter as tk
from tkinter import messagebox
import time
import pyperclip
import requests

API_TOKEN = "?auth_token=22DYD6YIYLDIVB2WCVRETOZZWTTZFI4IRELHJHUZXL6QEKVVLXEA"
BASE_URL = "https://api.real-debrid.com/rest/1.0/"
class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


def add_torrent(app):
    app.destroy()
    main_window = tk.Tk()
    torrent_url = tk.StringVar(main_window)
    torrent_url_input = tk.Entry(main_window, textvariable=torrent_url)
    torrent_url_input.grid(row=1, column=1)
    confirm_button = tk.Button(main_window, text="Enter",
                               command=lambda: torrent_handle(str(torrent_url.get()),
                                                              main_window))
    confirm_button.grid(row=2, column=1)
    main_window.mainloop()


def post_url(post_Data, url):
    url = BASE_URL + url + API_TOKEN
    response = json.loads(requests.post(url, data=post_Data, timeout=5).text)
    return response


def get_url(url):
    url = BASE_URL + url + API_TOKEN
    response = json.loads(requests.get(url, timeout=5).text)
    return response


def send_select_request(torrent_id, enable_dic, app): #TODO add instant available message
    app.destroy()
    #file_list = [] TODO Uncomment when reald-debrid fixes API
    #for item in enable_dic:
    #    if enable_dic[item].get() == 1:
    #       file_list.append(item)
    #postData = {'files': file_list} TODO ********************
    postData = {'files': [enable_dic.get()]}
    requests.post(BASE_URL + "torrents/selectFiles/" + torrent_id + API_TOKEN, data=postData, timeout=5)
    show_torrent_list()


def select_torrent_files(torrent_id, main_app=None):
    main_app.destroy()
    index = 0
    file_check_list = tk.Tk()
    scframe = VerticalScrolledFrame(file_check_list)
    scframe.pack()
    #enable_dic = {} TODO Uncomment when real-debrid fixes API
    enable_dic = tk.StringVar(file_check_list)
    response = get_torrent_info(torrent_id)
    while response['status'] != "waiting_files_selection":
        time.sleep(5)
        response = get_torrent_info(torrent_id)
    #for file in response['files']: TODO *****************************
    #    index += 1
    #    enable_dic[file['id']] = tk.IntVar()
    #    checkbox = tk.Checkbutton(file_check_list,
    #                              text="Name: " + file['path'] + ",Size: " + str(file['bytes'] / 1000000) + "MB",
    #                              variable=enable_dic[file['id']])
    #    checkbox.grid(row=index, column=0, sticky=tk.W)TODO **************************
    enable_dic.set("all")
    radio_button = tk.Radiobutton(scframe.interior,
                                  text="Select all files",
                                  variable=enable_dic, value="all")
    radio_button.grid(row=index,column=0)
    for file in response['files']:
        index +=1
        radio_button = tk.Radiobutton(scframe.interior,text="Name: " + file['path'] + ",Size: " + str(file['bytes'] / 1000000) + "MB",
                                      variable=enable_dic, value=str(file['id']))
        radio_button.grid(row=index, column=0, sticky=tk.W)
    confirm_button = tk.Button(scframe.interior, text="Continue",
                               command=lambda: send_select_request(torrent_id, enable_dic, file_check_list))
    confirm_button.grid(row=index + 1, column=0)
    file_check_list.mainloop()


def torrent_handle(torrent_url, main_window):
    postData = {'magnet': torrent_url}
    response = post_url(postData, "torrents/addMagnet")
    torrent_id = response['id']
    select_torrent_files(torrent_id, main_window)
    # postData = {'files': 2}
    # response = get_torrent_info(response['id'])
    # requests.post(BASE_URL + "torrents/selectFiles/" + response['id'] + API_TOKEN, data=postData, timeout=5)
    # print(response)
    # if int(response['progress']) < 100:
    #   torrent_download_url.set('Torrent is not cached, need to wait for download to finish :(')
    # else:
    #   main_gui()
    #  postData = {'link': response['links'][0]}
    # response = post_url(postData, "unrestrict/link/")
    # print(response)
    # torrent_download_url.set(response['download'])


def refresh_torrent_list(app):
    app.destroy()
    show_torrent_list()


def generate_download_link(selected_torrent):#check multiple file case
    response = get_torrent_info(selected_torrent)
    if response['status'] != 'downloaded':
        tk.messagebox.showerror("Download not finished", "Download hasn't finished yet, please wait.")
    else:
        tk.messagebox.showinfo("Copied!", "Download link copied to clipboard!")
        postData = {'link': response['links'][0]}
        response = post_url(postData, "unrestrict/link/")
        pyperclip.copy(response['download'])


def delete_torrent(torrent_id, app):
    response = get_torrent_info(torrent_id)
    result = tk.messagebox.askyesno("Really delete?", "Are you sure you want to delete " + response['filename'] + '?')
    if result:
        requests.delete(BASE_URL + "torrents/delete/" + str(torrent_id) + API_TOKEN)
        refresh_torrent_list(app)


def show_torrent_list():
    torrent_window = tk.Tk()
    torrent_dic = {}
    selected_torrent = tk.StringVar(torrent_window)
    response = get_url("torrents/")
    for item in response:
        torrent_dic[str(item['filename'])] = item['id']
    if len(torrent_dic) > 0:
        selected_torrent.set(list(torrent_dic.keys())[0])
    torrent_list = tk.OptionMenu(torrent_window, selected_torrent, *torrent_dic.keys())
    torrent_list.grid(row=1, column=0)
    details_text = tk.Text(torrent_window)
    show_torrent_details(details_text, str(torrent_dic[selected_torrent.get()]))
    details_text.grid(column=0, row=3)
    details_button = tk.Button(torrent_window, text="General details",
                               command=lambda: show_torrent_details(details_text,
                                                                    str(
                                                                        torrent_dic[
                                                                            selected_torrent.get()])))
    files_button = tk.Button(torrent_window, text="File Info", command=lambda: show_torrent_details(details_text,
                                                                                                    str(torrent_dic[
                                                                                                            selected_torrent.get()]),
                                                                                                    extended=True))
    add_torrent_button = tk.Button(torrent_window, text="Add torrent", command=lambda: add_torrent(torrent_window))
    refresh_button = tk.Button(torrent_window, text="Refresh", command=lambda: refresh_torrent_list(torrent_window))
    get_download_link = tk.Button(torrent_window, text="Download link",
                                  command=lambda: generate_download_link(torrent_dic[selected_torrent.get()]))
    get_download_link.grid(row=1, column=2)
    delete_torrent_button = tk.Button(torrent_window, text="Delete torrent",
                                      command=lambda: delete_torrent(torrent_dic[selected_torrent.get()],
                                                                     torrent_window))
    response = get_torrent_info(str(torrent_dic[selected_torrent.get()]))
    if response['status'] == "waiting_files_selection":
        select_files_button = tk.Button(torrent_window,text="Select files", command=lambda :select_torrent_files(str(torrent_dic[selected_torrent.get()]),torrent_window))
        select_files_button.grid(row=2,column=2)

    delete_torrent_button.grid(column=2, row=3)
    refresh_button.grid(row=1, column=3)
    add_torrent_button.grid(row=3, column=3)
    files_button.grid(row=4, column=2)
    details_button.grid(row=4, column=3)
    torrent_window.mainloop()


def get_torrent_info(torrent_id):
    return get_url("torrents/info/" + str(torrent_id))


def get_torrent_info_label(torrent_id, extended=False):
    response = get_torrent_info(torrent_id)
    if not extended:
        info = "Name: " + response['filename']
        info += "\n" + "Size: " + str(response['bytes'] / 1000000000) + "GB"
        info += "\nStatus: " + response['status']
        if response['status'] != 'downloaded':
            info += "\nProgress: " + str(response['progress']) + "%"
            if response['status'] == "downloading" or response['status'] == "compressing" or response[
                'status'] == "uploading":
                info += "\nSpeed: " + str(response['speed'] / 1000000) + " Mbps"
                if response['status'] == "downloading":
                    info += "\nSeeders: " + str(response['seeders'])
        else:
            info += "\nDate Finished: " + response['ended']
    else:
        info = "Files:"
        info += "\n************************"
        for file in response['files']:
            info += "\nPath: " + file['path']
            info += "\nSize: " + str(file['bytes'] / 1000000) + "MB"
            if file['selected'] == 0:
                info += "\nDownloaded: No"
            else:
                info += "\nDownloaded: Yes"
            info += "\n************************"
    return info


def show_torrent_details(torrent_details, torrent_id, extended=False):
    torrent_details.delete(1.0, tk.END)
    if not extended:
        info = get_torrent_info_label(torrent_id)
    else:
        info = get_torrent_info_label(torrent_id, extended=True)

    torrent_details.insert(1.0, info)


if __name__ == "__main__":
    show_torrent_list()
