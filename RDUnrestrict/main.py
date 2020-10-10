import json
import tkinter as tk
from tkinter import messagebox
import time
import pyperclip
import requests
from vsf import VerticalScrolledFrame
from tkinter import scrolledtext
from collections import OrderedDict

API_TOKEN = 'AUTHTOKEN'
BASE_URL = 'https://api.real-debrid.com/rest/1.0/'


# noinspection PyAttributeOutsideInit
class TorrentListWindow:
    def __init__(self):
        pass

    def refresh_window(self):
        self.parent.destroy()
        self.start_window()

    def start_window(self):
        self.parent = tk.Tk()
        self.torrent_dic = {}
        self.selected_torrent = tk.StringVar(self.parent)
        response = get_url("torrents/")
        for item in response:
            self.torrent_dic[str(item['filename'])] = item['id']
        if len(self.torrent_dic) > 0:
            self.selected_torrent.set(list(self.torrent_dic.keys())[0])
        torrent_list = tk.OptionMenu(self.parent, self.selected_torrent, *self.torrent_dic.keys())
        torrent_list.grid(row=1, column=0)
        self.details_text = scrolledtext.ScrolledText(self.parent)
        self.show_torrent_details()
        self.details_text.grid(column=0, row=3)
        details_button = tk.Button(self.parent, text="General details",
                                   command=self.show_torrent_details)
        files_button = tk.Button(self.parent, text="File Info", command=lambda: self.show_torrent_details(True))
        add_torrent_button = tk.Button(self.parent, text="Add torrent", command=self.add_torrent)
        refresh_button = tk.Button(self.parent, text="Refresh", command=self.refresh_window)
        get_download_link = tk.Button(self.parent, text="Download link",
                                      command=self.generate_download_link)
        get_download_link.grid(row=1, column=2)
        delete_torrent_button = tk.Button(self.parent, text="Delete torrent",
                                          command=self.delete_torrent)
        stream_torrent_button = tk.Button(self.parent, text="Stream torrent",
                                          command=self.stream_torrent)
        stream_torrent_button.grid(row=1,column=4)
        response = get_torrent_info(str(self.torrent_dic[self.selected_torrent.get()]))
        if response['status'] == "waiting_files_selection":
            select_files_button = tk.Button(self.parent, text="Select files",
                                            command=self.man_select_torrent_files)  # fix
            select_files_button.grid(row=2, column=2)

        delete_torrent_button.grid(column=2, row=3)
        refresh_button.grid(row=1, column=3)
        add_torrent_button.grid(row=3, column=3)
        files_button.grid(row=4, column=2)
        details_button.grid(row=4, column=3)
        self.parent.mainloop()

    def man_select_torrent_files(self):
        select_file_window = SelectFileWindow(self)
        self.parent.destroy()
        self.man = True
        select_file_window.select_torrent_files()

    def show_torrent_details(self, extended=False):
        self.details_text.delete(1.0, tk.END)
        if not extended:
            info = get_torrent_info_label((self.torrent_dic[self.selected_torrent.get()]))
        else:
            info = get_torrent_info_label((self.torrent_dic[self.selected_torrent.get()]), extended=True)
        self.details_text.insert(1.0, info)

    def add_torrent(self):
        self.parent.destroy()
        self.add_torrent_window = tk.Tk()
        self.torrent_url = tk.StringVar(self.add_torrent_window)
        select_file_window = SelectFileWindow(self)
        self.man = False
        torrent_url_input = tk.Entry(self.add_torrent_window, textvariable=self.torrent_url)
        torrent_url_input.grid(row=1, column=1)
        confirm_button = tk.Button(self.add_torrent_window, text="Enter",
                                   command=select_file_window.select_torrent_files)
        confirm_button.grid(row=2, column=1)
        self.add_torrent_window.mainloop()

    def generate_download_link(self):
        response = get_torrent_info(self.torrent_dic[self.selected_torrent.get()])
        if response['status'] != 'downloaded':
            tk.messagebox.showerror("Download not finished", "Download hasn't finished yet, please wait.")
        else:
            if len(response['links']) == 1:  # checking if length of file list is 1
                post_data = {'link': response['links'][0]}
                response = post_url(post_data, "unrestrict/link/")
                pyperclip.copy(response['download'])
                tk.messagebox.showinfo("Copied", "Download link copied to clipboard!")
            else:  # multiple file case, add all ?
                dic = {}
                index = 0
                for item in response['files']:
                    if item['selected'] == 1:
                        dic[item['path']] = response['links'][index]
                        index += 1
                index = 1
                self.file_check_list = tk.Tk()
                scframe = VerticalScrolledFrame(self.file_check_list)
                scframe.pack()
                self.selected_file = tk.StringVar(self.file_check_list)
                ls = [item['path'] for item in response['files'] if item['selected'] == 1]
                ls.sort()  # display alphabitcally
                self.selected_file.set(dic[ls[0]])
                for file in ls:
                    index += 1
                    radio_button = tk.Radiobutton(scframe.interior, text="Name: " + file, variable=self.selected_file,
                                                  value=dic[file])
                    radio_button.grid(row=index, column=0, sticky=tk.W)
                confirm_button = tk.Button(scframe.interior, text="Continue",
                                           command=self.multiple_file_download_link)
                confirm_button.grid(row=1, column=0)
                self.file_check_list.mainloop()

    def multiple_file_download_link(self):
        self.file_check_list.destroy()
        post_data = {'link': str(self.selected_file.get())}
        response = post_url(post_data, "unrestrict/link/")
        pyperclip.copy(response['download'])
        tk.messagebox.showinfo("Copied", "Download link copied to clipboard!")

    def multiple_file_stream_link(self):
        self.file_check_list.destroy()
        post_data = {'link': str(self.selected_file.get())}
        response = post_url(post_data, "unrestrict/link/")
        if response['streamable'] == 1:
            pyperclip.copy("https://real-debrid.com/streaming-" + response['id'])
            tk.messagebox.showinfo("Copied", "Stream link copied to clipboard!")
        else:
            tk.messagebox.showerror("Error", "File is not streamable.")

    def delete_torrent(self):
        response = get_torrent_info(self.torrent_dic[self.selected_torrent.get()])
        result = tk.messagebox.askyesno("Really delete?",
                                        "Are you sure you want to delete " + response['filename'] + '?')
        if result:
            requests.delete(
                BASE_URL + "torrents/delete/" + str(self.torrent_dic[self.selected_torrent.get()]) + API_TOKEN)
            self.refresh_window()

    def stream_torrent(self):

        response = get_torrent_info(self.torrent_dic[self.selected_torrent.get()])
        if response['status'] != 'downloaded':
            tk.messagebox.showerror("Download not finished", "Download hasn't finished yet, please wait.")
        else:
            if len(response['links']) == 1:  # checking if length of file list is 1
                post_data = {'link': response['links'][0]}
                response = post_url(post_data, "unrestrict/link/")
                if response['streamable'] == 1:
                    pyperclip.copy("https://real-debrid.com/streaming-" + response['id'])
                    tk.messagebox.showinfo("Copied", "Stream link copied to clipboard!")
                else:
                    tk.messagebox.showerror("Error","File is not streamable.")
            else:  # multiple file case, add all ?
                dic = {}
                index = 0
                for item in response['files']:
                    if item['selected'] == 1:
                        dic[item['path']] = response['links'][index]
                        index += 1
                index = 1
                self.file_check_list = tk.Tk()
                scframe = VerticalScrolledFrame(self.file_check_list)
                scframe.pack()
                self.selected_file = tk.StringVar(self.file_check_list)
                ls = [item['path'] for item in response['files'] if item['selected'] == 1]
                ls.sort()  # display alphabitcally
                self.selected_file.set(dic[ls[0]])
                for file in ls:
                    index += 1
                    radio_button = tk.Radiobutton(scframe.interior, text="Name: " + file, variable=self.selected_file,
                                                  value=dic[file])
                    radio_button.grid(row=index, column=0, sticky=tk.W)
                confirm_button = tk.Button(scframe.interior, text="Continue",
                                           command=self.multiple_file_stream_link)
                confirm_button.grid(row=1, column=0)
                self.file_check_list.mainloop()


# noinspection PyAttributeOutsideInit
class SelectFileWindow:
    def __init__(self, master):
        self.master = master

    def select_torrent_files(self):
        if not self.master.man:
            self.master.add_torrent_window.destroy()
            post_data = {'magnet': self.master.torrent_url.get()}
            response = post_url(post_data, "torrents/addMagnet")
            self.torrent_id = response['id']
        else:
            self.torrent_id = str(self.master.torrent_dic[self.master.selected_torrent.get()])
        index = 0
        self.file_check_list = tk.Tk()
        scframe = VerticalScrolledFrame(self.file_check_list)
        scframe.pack()
        self.enable_dic = tk.StringVar(self.file_check_list)
        response = get_torrent_info(self.torrent_id)
        while response['status'] != "waiting_files_selection":
            time.sleep(2)
            response = get_torrent_info(self.torrent_id)
        self.enable_dic.set("all")
        radio_button = tk.Radiobutton(scframe.interior,
                                      text="Select all files",
                                      variable=self.enable_dic, value="all")
        radio_button.grid(row=index, column=0)
        for file in response['files']:
            index += 1
            radio_button = tk.Radiobutton(scframe.interior, text="Name: " + file['path'] + ",Size: " + str(
                file['bytes'] / 1000000) + "MB",
                                          variable=self.enable_dic, value=str(file['id']))
            radio_button.grid(row=index, column=0, sticky=tk.W)
        confirm_button = tk.Button(scframe.interior, text="Continue",
                                   command=self.send_select_request)
        confirm_button.grid(row=index + 1, column=0)
        self.file_check_list.mainloop()

    def send_select_request(self):
        self.file_check_list.destroy()
        post_data = {'files': [self.enable_dic.get()]}
        requests.post(BASE_URL + "torrents/selectFiles/" + self.torrent_id + API_TOKEN, data=post_data, timeout=5)
        self.master.start_window()


def post_url(post_data, url):
    url = BASE_URL + url + API_TOKEN
    response = json.loads(requests.post(url, data=post_data, timeout=5).text)
    return response


def get_url(url):
    url = BASE_URL + url + API_TOKEN
    response = json.loads(requests.get(url, timeout=5).text)
    return response


def get_torrent_info(torrent_id):
    return get_url("torrents/info/" + str(torrent_id))


def get_torrent_info_label(torrent_id, extended=False):
    response = get_torrent_info(torrent_id)
    if not extended:
        info = "Name: " + response['filename']
        info += "\n" + "Size: " + str(response['bytes'] / 1000000000) + "GB"
        info += "\nStatus: " + response['status']
        if response['status'] != 'downloaded':
            info += "\nProgress: " + str(float(response['progress'])) + "%"
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
    window = TorrentListWindow()
    window.start_window()
