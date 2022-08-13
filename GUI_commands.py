"""Module containing functions that are use for button commands, checking url purposes, blocking website,
getting a list of block websites, etc"""

# Importing modules
from tkinter import *
from tkinter import messagebox
import webbrowser as wb
import requests
from math import ceil
from queue_DS import history_queue
from platform import system

# host path and ip address
host_path ='C:\Windows\System32\drivers\etc\hosts' if system() == "Windows" else "/etc/hosts"
#  a duplicate of the host file used during development, you may use this HOSTS2 file for testing purposes
#host_path = "HOSTS2"
ip_address = '127.0.0.1'

# this command class contains static methods that are used as buttons commands in the main GUI
class commands:
    # static method that is used as the button command for the block button to block websites
    @staticmethod
    def block_command(web_var, s_lbl, block_btn, GUI_cls, btm_frame):
        website = web_var.get()
        s_lbl["text"] = "Searching..."
        block_btn["state"] = "disabled"
        # the second version of the website link will be without the "www" if the user input website has it
        # if user did not input a website link with the "www", the second version will be the one with it
        if website.startswith("www."):
            second_link = website[4:]
        else:
            second_link = website
            website = f"www.{website}"
        # checking if the url are real before blocking the website
        if url_check(f"https://{website}") or url_check(f"https://{second_link}"):
            block_web(second_link, GUI_cls, btm_frame, web_var=web_var)
        else:
            messagebox.showerror(title="Website invalid!", message="Website input is not found")
        s_lbl["text"] = ""
        block_btn["state"] = "normal"

    # the static method used as the button command for the unblock button to unblock websites
    @staticmethod
    def unblock_command(web, GUI_cls, location):
        # filter out the web that the user want to unblock out of the list of block webs
        GUI_cls.blocked_webs = list(filter(lambda block_web: web not in block_web, GUI_cls.blocked_webs))
        # after filtering, we write the websites that are not the web that we want to block back into the host file
        with open(host_path, 'w') as host_file:
            for block_web in GUI_cls.blocked_webs:
                host_file.write(block_web)
        messagebox.showinfo(title="Website unblocked!", message="This website is now unblock!")
        # after unblock, we need to forget all of the bottom frames widgets so that we can change the bottom frame
        for widget in GUI_cls.btm_widgets_list:
            widget.place_forget()
        # changing the page amount and check if the current page is empty, if it is, it will go to the previous page
        GUI_cls.page_amt = ceil(len(GUI_cls.blocked_webs) / 5)
        if len(GUI_cls.blocked_webs[(GUI_cls.page_num - 1) * 5: GUI_cls.page_num * 5]) == 0:
            GUI_cls.page_num = GUI_cls.page_num - 1 if GUI_cls.page_num != 1 else GUI_cls.page_num
        GUI_cls.create_bottom_frame(location) # recreate the bottom frame

    # the static method used as the button command for the back button and forward button
    @staticmethod
    def switch(GUI_cls, location, reset_func, is_forward):
        # forgetting all of the bottom frames widgets so that we can change the bottom frame
        for widget in GUI_cls.btm_widgets_list:
            widget.place_forget()
        # to check if the button click is forward or back, if forward, the page_num increase by one, if back, the page_num decrease by one
        if is_forward:
            GUI_cls.page_num += 1
        else:
            GUI_cls.page_num -= 1
        reset_func(location) # recreate the bottom frame

    # the staticmethod used as the button command for the test website button
    @staticmethod
    def test_web(url):
        # check if the  first link is able to access the website, if not we use the link with the "www."
        if url_check(f"https://{url}"):
            wb.open_new(f"https://{url}")
        else:
            wb.open_new(f"https://www.{url}")

    # the staticmethod used as the the button command for the history button to access the past history of block websites
    @staticmethod
    def history(hist_btn, GUI_cls, btm_frame):
        # disabled button so user can't create multiple at once
        hist_btn["state"] = "disabled"
        # create new gui to show past block websites
        hist_root = Tk()
        hist_root.title("Block history")
        hist_root.resizable(0, 0)
        hist_root.geometry("380x268")
        hist_root.protocol("WM_DELETE_WINDOW", lambda: on_closing(hist_btn, hist_root))

        # x and y used for placing the buttons using the grid method
        x = 0
        y = 0
        # creating buttons for each block website in the history queue list, the amount buttons may be up to 20
        for blocked_web in GUI_cls.block_history.queue:
            block_web_btn = Button(hist_root, text=blocked_web, width=25,
                             bg="cyan", command=lambda blocked_web=blocked_web: block_web(blocked_web, GUI_cls, btm_frame,
                                                                                          protocol=lambda :on_closing(hist_btn, hist_root)))
            block_web_btn.grid(column=x, row=y)
            y += 1
            if y == 10: # if the column has already 10 buttons, we put the remaining buttons to the new row
                x += 1
                y = 0


# url_check function to check if the url is real or not 
def url_check(url):
    #Description
    """Boolean return - check to see if the site exists.
       This function takes a url as input and then it requests the site
       head - not the full html and then it checks the response to see if
       it's less than 400. If it is less than 400 it will return TRUE
       else it will return False.
    """
    try:
            site_ping = requests.head(url)
            if site_ping.status_code < 400:
                #  To view the return status code, type this   :   **print(site.ping.status_code)**
                return True
            else:
                return False
    except Exception:
        return False

# get_blocked_web function to create a list of current block websites by reading from the host file
def get_blocked_web():
    with open(host_path, "r") as file:
        # filter the contain of the file to only include the block website lines and filter out lines comments line or empty lines into the list
        block_list = list(filter(lambda line: False if "#" in line or line.startswith("\n") else True, file.readlines()))
    return block_list

# get_block_history to create a queue data structure of user history of block websites by reading from the history.txt file
def get_block_history():
    hist_list = history_queue()
    with open("history.txt", "r") as file:
        for line in file.readlines():
            # removing "\n" when putting the line into the queue
            if "\n" in line:
                hist_list.queue.append(line[:-1])
            else:
                hist_list.queue.append(line)
    return hist_list

# on_closing function used as protocol to turn the button state back to normal by the history GUI
def on_closing(btn, GUI):
    try:
        btn["state"] = "normal"
        GUI.destroy()
    except Exception as e: # if the main GUI is closed, this is used to allow the history GUI to close too
        GUI.destroy()

# block web function used by the block command staticmethod and as the history block web button command to block website
def block_web(second_link, GUI_cls, btm_frame, web_var=None, protocol=None):
    website = f"www.{second_link}"
    with open(host_path, 'r+') as host_file:
        file_content = host_file.read()
        # if website is already is already in the file, we just show the user a messagebox
        if website in file_content:
            messagebox.showinfo(title="Website is already blocked!",
                                message="The website you have input is already blocked.")
        else:
            # write to the host file and set the remove the website from the entry after adding
            host_file.write(ip_address + " " + website + " " + second_link + '\n')
            if web_var is not None:
                web_var.set("")
            messagebox.showinfo(title="Website blocked!", message="The website you have input is now blocked!")

            # add the website to the history list
            GUI_cls.block_history.modify(second_link)

            # after adding, we need to update the list of website shown in the GUI on the bottom frame
            for widget in GUI_cls.btm_widgets_list:
                widget.place_forget()
            GUI_cls.blocked_webs.append(f"{ip_address} {website} {second_link}\n")
            GUI_cls.page_amt = ceil(len(GUI_cls.blocked_webs) / 5)
            GUI_cls.create_bottom_frame(btm_frame) # recreate the bottom frame
        # protocol for the history block website to close the history gui
        if protocol is not None:
            protocol()