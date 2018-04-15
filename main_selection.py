from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog

import os
import process_photo


def main():
    root = Tk()
    root.filename = tkFileDialog.askopenfilename(initialdir=".", title="Select photo",
                                                 filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    process_photo.add_photo(root.filename, 'NAME')


if __name__ == '__main__':
    main()
