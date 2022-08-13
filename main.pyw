""" The main module where the program will be run. To make the running of this program easier, user may place
every file used in this program to the system32 ( on windows) directory. User may also rename this main.pyw file
to something else so that user can easily identify the main file to run this program in the cmd prompt.
To run this program, user must run as administrator with the cmd and do "python (this file name)" so that this
program is able to access and change the content of the user host file"""

# importing modules
from tkinter import *
import website_GUI
from website_GUI import GUI

# the main function to run the whole program
def main():
    # creating GUI
    root = Tk()
    # GUI title, size, etc
    root.title("Website blocker")
    root.geometry(f"{website_GUI.width}x{website_GUI.height}")
    root.resizable(0, 0)
    root.iconbitmap("blocker.ico")
    root.protocol("WM_DELETE_WINDOW", lambda: GUI.main_closing(root))

    # creating 3 frames, the title frame, blocking frame and a list/unblocking frame
    # top frame for GUI title
    top_frame = Frame(root, bg="green", width=website_GUI.width, height=website_GUI.prct(20, website_GUI.height))
    top_frame.place(x=0, y=0)

    # middle frame for entering website and blocking
    middle_frame = Frame(root, bg="#D3D3D3", width=website_GUI.width, height=website_GUI.prct(30, website_GUI.height))
    middle_frame.place(x=0, y=website_GUI.prct(20, website_GUI.height))

    # bottom frame to show a list of block website and unblock options
    bottom_frame = Frame(root, bg="white", width=website_GUI.width, height=website_GUI.prct(50, website_GUI.height))
    bottom_frame.place(x=0, y=website_GUI.prct(50, website_GUI.height))

    # title label
    title_lbl = Label(top_frame, text="Website Blocker", fg="cyan", font=("Verdana Bold", 30), bg="green").place(
        x=website_GUI.prct(22, website_GUI.width), y=website_GUI.prct(5, website_GUI.height))

    # creating label, button and entry for middle frame
    GUI.create_middle_frame(middle_frame, bottom_frame)

    # creating label and buttons for bottom frame
    GUI.create_bottom_frame(bottom_frame)

    # running GUI
    mainloop()

if __name__ == '__main__':
    main()

