"""This module contains the GUI class and everything used for the GUI. The GUI class contains instance
variable like a list of block websites or history list of block websites, stringvars for the bottom frame usages
and the page number. The class GUI also contains staticmethod to create the widgets of the middle frame, bottom frame
unblock and test button as well as the protocol for when user close the GUI
"""

# importing modules
from tkinter import *
from GUI_commands import commands as cm
from GUI_commands import get_blocked_web as gb_web
from GUI_commands import get_block_history as gb_hist
from threading import Thread
from math import ceil

# width and height variable
width = 600
height = 500

# function percent to calculate the percentage of width or height for placement or measuing size purposes
def prct(percent, length):
    return (percent * length) // 100

class GUI:
    # Instance variable
    # variable that will hold a stringvar when the middle frame and bottom frame are created
    web_var = None
    select_web = None
    page_num = 1
    blocked_webs = gb_web() # the list of block websites
    block_history = gb_hist() # the list of past block websites
    y_place = 6 # set the y coordinate percentage for the first block website radio button
    page_amt = ceil(len(blocked_webs) / 5) # a page will contain 5 block website and the amount of block website will determine the page amount
    btm_widgets_list = None # the instance variable that will hold every widgets that needs to change when resetting the bottom frame

    # static method to create all of the widgets of the middle frame and place it on the middle frame
    @staticmethod
    def create_middle_frame(location, btm_frame):
        # creating label, button and entry
        enter_web_lbl = Label(location, text="Enter Website (No Query):", font="Times 10", bg="#D3D3D3").place(
            x=prct(40, width), y=prct(2, height))
        search_lbl = Label(location, font=("Verdana Bold", 12), bg="#D3D3D3")
        search_lbl.place(x=prct(20, width), y=prct(22, height)) # need to write a line with .place
        block_btn = Button(location, text="Block", font=("Verdana Bold", 8),
                           command=lambda: Thread(target=cm.block_command, daemon=True,
                                                  args=(GUI.web_var, search_lbl, block_btn, GUI, btm_frame)).start())
        block_btn.place(x=prct(46, width), y=prct(22, height))

        # string var for url entry
        GUI.web_var = StringVar(value="www.google.com")
        url_entry = Entry(location, textvariable=GUI.web_var, width=80, font="arial 8")
        url_entry.place(x=50, y=40, height=40)

    # static method to create all of the widgets of the bottom frame and place it on the bottom frame
    @staticmethod
    def create_bottom_frame(location):
        # creating and resetting the widget list
        GUI.btm_widgets_list = list()

        list_lbl = Label(location, text="List of block websites", font=("Verdana Bold", 10), bg="white").place(
            x=prct(38, width), y=prct(1, height)
        )
        page_lbl = Label(location, text=f"Page {GUI.page_num}", bg="white")
        page_lbl.place(x=prct(20, width), y=prct(40,height))

        #buttons
        back_btn = Button(location, text="<<", command=lambda:cm.switch(GUI, location, GUI.create_bottom_frame, False))
        forward_btn = Button(location, text=">>", command=lambda: cm.switch(GUI, location, GUI.create_bottom_frame, True))
        his_btn = Button(location, text="History", width=10, command=lambda: cm.history(his_btn, GUI, location))

        # check the page number, if its first, the back_btn is disabled, if the page num is the page amount, the forward_btn is disabled
        if GUI.page_num == 1:
            back_btn["state"] = "disabled"
        if GUI.page_num == GUI.page_amt:
            forward_btn["state"] = "disabled"

        # after placing them, we need to put the page label, back and forward button to the widget list so they can reset themselves
        # alongside with the other widgets
        GUI.btm_widgets_list.append(back_btn)
        GUI.btm_widgets_list.append(forward_btn)
        GUI.btm_widgets_list.append(page_lbl)

        # placing them
        back_btn.place(x=prct(10, width), y=prct(40, height))
        forward_btn.place(x=prct(32, width), y=prct(40, height))
        his_btn.place(x=prct(80, width), y=prct(40, height))

        # string var
        GUI.select_web = StringVar(value="None")
        block_weblist = list(map(lambda web: web[web.index("w"):-1].split()[1], GUI.blocked_webs[(GUI.page_num - 1) * 5 : GUI.page_num * 5]))
        GUI.y_place = 6 # setting or resetting the y_place to 6
        # placing up to 5 radio buttons to the bottom frame
        for b_web in block_weblist:
            web_rbtn = Radiobutton(location, text=b_web, value=b_web,
                                   variable=GUI.select_web, indicator=0, font=("Arial", 10),
                                   width=30, background ="light blue", selectcolor="light green",
                                   command= lambda: GUI.set_unblocktest(location, GUI.select_web.get(), GUI.btm_widgets_list))
            web_rbtn.place(x=prct(30, width), y=prct(GUI.y_place, height))
            GUI.btm_widgets_list.append(web_rbtn)
            GUI.y_place += 5

    # static method that will be used by the block website radio buttons commands. Basically, if the user click on any of the block website
    # radio button, a pair of test button to test if the website is properly block and unblock button to unblock the website will pop up on the bottom frame
    # for the users to use them
    @staticmethod
    def set_unblocktest(location, url, btn_list):
        # creating test_btn to test if the website is properly block or not and unblock button to unblock the website
        test_btn = Button(location, text="Test website", command=lambda:cm.test_web(url))
        unblock_btn = Button(location, text="Unblock", command=lambda:cm.unblock_command(url, GUI, location))
        test_btn.place(x=prct(60, width), y=prct(40, height))
        unblock_btn.place(x=prct(45, width), y=prct(40, height))
        # adding the two buttons to the widgets list that needs to be reset when the page is change or when a website is block/unblock
        btn_list.append(test_btn)
        btn_list.append(unblock_btn)

    # staticmethod that is used for the protocol when the user close the main GUI
    # the main purpose is to write the new history list of block websites into the history.txt file
    @staticmethod
    def main_closing(main_GUI):
        with open("history.txt", "w") as file:
            for web in GUI.block_history.queue:
                file.write(web)
                file.write("\n")
        main_GUI.destroy()

