#!/usr/bin/env python3
# Author: LyfeOnEdge
# Purpose: Make a gui for nsw2ff8.py
# Original Script by AnalogMan https://github.com/AnalogMan151/nsw2ff8

import sys, os
import tkinter as tk

import style
from gui.widgets import basePlugin, basePage, button
from gui.widgets import scrollingWidgets

LABELWIDTH = 125
ABOUT = "~FF8 NSW Save Tool~\nOriginal Script by AnalogMan\n\nInjects or extracts FF8 save data to Switch save file."
OPTIONS = ["Inject", "Extract"]
OPTIONMAP = {
    "Inject" : "-i",
    "Extract": "-e",
}

class Page(basePage.BasePage):
    def __init__(self, app, container, plugin):
        basePage.BasePage.__init__(self, app, container, "Switch ~ FF8SaveTool")
        self.plugin = plugin
        
        self.about_label = tk.Label(self, text = ABOUT, background = style.secondary_color, font = style.smalltext, foreground = style.primary_text_color)
        self.about_label.place(relwidth = 1, x = style.offset, width = - 2 * style.offset, rely = 0.5, height = 90, y = - 180)

        self.save_entry_label = tk.Label(self, text = "FF8 Save file -", foreground = "white", background = style.secondary_color)
        self.save_entry_label.place(x = style.offset, width = LABELWIDTH, rely = 0.5, height = 20, y = - 70)
        self.save_entry_box = tk.Entry(self, foreground = "white", background = style.primary_color, justify = "center", font = style.mediumtext)
        self.save_entry_box.place(relwidth = 1, x = 2 * style.offset + LABELWIDTH, width = - (3 * style.offset + LABELWIDTH), rely = 0.5, height = 20, y = - 70)

        self.switch_save_entry_label = tk.Label(self, text = "Switch Save file -", foreground = "white", background = style.secondary_color)
        self.switch_save_entry_label.place(x = style.offset, width = LABELWIDTH, rely = 0.5, height = 20, y = - 40)
        self.switch_save_entry_box = tk.Entry(self, foreground = "white", background = style.primary_color, justify = "center", font = style.mediumtext)
        self.switch_save_entry_box.place(relwidth = 1, x = 2 * style.offset + LABELWIDTH, width = - (3 * style.offset + LABELWIDTH), rely = 0.5, height = 20, y = - 40)

        self.selected_option_label = tk.Label(self, text = "Mode -", foreground = "white", background = style.secondary_color)
        self.selected_option_label.place(x = style.offset, width = LABELWIDTH, rely = 0.5, height = 20, y = - 10 )
        self.selected_option = tk.StringVar()
        self.selected_option.set(OPTIONS[0])
        self.selected_option_dropdown = tk.OptionMenu(self,self.selected_option,*OPTIONS)
        self.selected_option_dropdown.configure(foreground = "white")
        self.selected_option_dropdown.configure(background = style.primary_color)
        self.selected_option_dropdown.configure(highlightthickness = 0)
        self.selected_option_dropdown.configure(borderwidth = 0)
        self.selected_option_dropdown.place(relwidth = 1, x = 2 * style.offset + LABELWIDTH, width = - (3 * style.offset + LABELWIDTH), rely = 0.5, height = 20, y = - 10)

        self.run_button = button.Button(self, text_string = "run script", background = style.primary_color, callback = self.run)
        self.run_button.place(relwidth = 1, x = style.offset, width = - 2 * style.offset, rely = 0.5, height = 20, y = 20)

        self.console_label = tk.Label(self, text = "CONSOLE:", foreground = "white", background = style.secondary_color)
        self.console_label.place(relwidth = 1, x = - 0.5 * LABELWIDTH, width = LABELWIDTH, rely = 0.5, height = 20, y = 40 + style.offset)

        self.console = scrollingWidgets.ScrolledText(self, background = "black", foreground = "white")
        self.console.place(relwidth = 1, width = - (2 * style.offset), relheight = 0.5, height = - (2 * style.offset + 60), rely = 0.5, y = 60 + style.offset, x = + style.offset)

    def Print(self, string):
        self.console.insert("end", string)
        self.console.yview_pickplace("end")
        self.plugin.out(string)

    def run(self):
        main(OPTIONMAP[self.selected_option.get()], self.save_entry_box.get(), self.switch_save_entry_box.get(), self.Print)
 
class Plugin(basePlugin.BasePlugin):
    def __init__(self, app, container):
        self.app = app
        self.container = container
        basePlugin.BasePlugin.__init__(self, app, "FF8SaveTool", container)

    def get_pages(self):
        return[Page(self.app, self.container, self)]

    def exit(self):
        pass

def main(arg, nsw_file, ff8_file, sout):
    inject = False
    extract = False
    if arg == "-i":
        inject = True
    if arg == "-e":
        extract = True

    # Check if required files exist
    if os.path.isfile(nsw_file) == False:
        sout('Switch save cannot be found\n\n')
        return 1

    if extract == True:
        try: 
            with open(nsw_file, 'rb') as nsw:
                save_len = int.from_bytes(nsw.read(4), byteorder='little')
                ff8_data = nsw.read(save_len)
            with open(ff8_file, 'wb') as ff8:
                ff8.write(ff8_data)
            sout('FF8 save file extracted successfully.\n\n')
        except Exception as e:
            sout(f'Save could not be extracted. - {e}\n\n')
    
    if inject == True:
        if os.path.isfile(ff8_file) == False:
            sout('FF8 save cannot be found\n\n')
            return 1
        try:
            with open(ff8_file, 'rb') as ff8:
                ff8_data = ff8.read()
            with open(nsw_file, 'rb+') as nsw:
                nsw.write((len(ff8_data)).to_bytes(4, byteorder='little'))
                nsw.write(ff8_data)
            sout('FF8 save file injected successfully.\n\n')
        except Exception as e:
            sout(f'Save could not be injected. - {e}\n\n')

def setup(app, container):
    return Plugin(app, container)
