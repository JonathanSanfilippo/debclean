#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Jonathan Sanfilippo
# Program: debclean
# Date: Feb 11 2023 - Birmingham, United Kingdom. 
# Copyright (C) 2023 Jonathan Sanfilippo <jonathansanfilippo.uk@gmail.com>
#
#Licenses:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

 

import threading
import tkinter 
import platform
import customtkinter
import os
import subprocess
import getpass
import tkinter as tk
import psutil
from tkinter import *
from PIL import Image
import json
import shutil
import time
from tkinter import Scrollbar
import socket


#info
username = getpass.getuser()
hostname = socket.gethostname()

#root-(app)-dsm v1.00
app = customtkinter.CTk(className='Debian System Management') 
app.geometry(f"{1020}x{650}")
app.minsize(1020, 650)
app.maxsize(1020, 650)


def title_status():
    app.title(f"{username}@{hostname}")
    app.after(1000, title_status)
app.title(f"debclean - Debian System Management")  
app.after(1000, title_status)

#icons
icon = tkinter.PhotoImage(file="/home/" + username + "/.config/dsm/icons/app-icon.png")
app.iconphoto(False, icon)   


# Definire il percorso del file JSON 
file_path = "/home/" + username + "/.config/dsm/config/mode.json"

# Impostare il valore predefinito del modo di apparizione e del tema di colore
appearance_mode = "System"
color_theme = customtkinter.set_default_color_theme( "/home/" + username + "/.config/dsm/config/theme.json")

# Provare a caricare la scelta dell'utente dal file JSON
try:
    with open(file_path, "r") as file:
        choice = json.loads(file.read())
        appearance_mode = choice.get("appearance_mode", appearance_mode)
        color_theme = choice.get("color_theme", color_theme)
except FileNotFoundError:
    pass

# Impostare il modo di apparizione e il tema di colore
customtkinter.set_appearance_mode(appearance_mode)
#customtkinter.set_default_color_theme(color_theme)

appearance_mode_var = tkinter.StringVar(value=appearance_mode)
app.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(app,width=90,dropdown_hover_color=("#3b8ed0","#06c"), values=["Light", "Dark", "System"],
                                                              variable=appearance_mode_var,
                                                              command=lambda value: change_appearance_mode_event(value))
app.appearance_mode_optionemenu.place(x=40, y=610)

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)
    with open(file_path, "w") as file:
        choice = {"appearance_mode": new_appearance_mode, "color_theme": color_theme}
        json.dump(choice, file)

label = customtkinter.CTkLabel(master=app,text="Themes", width=50, height=15, text_color="#868686")
label.place(x=55, y=590)


#terminals
with open('/home/' + username + '/.config/dsm/config/terminals.json', 'r') as file:
    terminals_dict = json.load(file)
 
# Accedi alla lista di terminali
terminals = terminals_dict['terminals']

#license
label = customtkinter.CTkLabel(master=app,text="Copyright (C) 2023 Jonathan Sanfilippo - Licensed GPLv3", width=250, height=15, text_color="#868686")
label.place(x=365, y=620)

# Sidebar
app.sidebar_frame = customtkinter.CTkFrame(app, width=170, height=390, corner_radius=12)
app.sidebar_frame.place(x=20, y=10)

# panel right
app.panel_frame = customtkinter.CTkFrame(app, width=170, height=390, corner_radius=12)
app.panel_frame.place(x=825, y=10)


logo = customtkinter.CTkImage(light_image=Image.open("/home/" + username + "/.config/dsm/icons/app-logo.png"),
                                  dark_image=Image.open("/home/" + username + "/.config/dsm/icons/app-logo.png"),
                                  size=(100, 80))

label003 = customtkinter.CTkLabel(app, image=logo, text=" ", fg_color=('#dbdbdb','#2b2b2b') )
label003.place(x=56, y=279)
 


vr = os.popen('cat "/home/' + username + '/.config/dsm/version"').read()
text = "debclean v" + vr

# Create the label with the text from the file
app.label = customtkinter.CTkLabel(app, text=text, width=10, fg_color=('#dbdbdb','#2b2b2b'), text_color="#868686")
app.label.place(x=62, y=352)



#ProgressBar
progressbar = customtkinter.CTkProgressBar(app, width=250, height=5,progress_color="#55ff00")
progressbar.configure(mode="indeterminate",)
progressbar.place_forget()



class MyTabView(customtkinter.CTkTabview):
    def __init__(app, master, **kwargs):
        super().__init__(master, **kwargs)
         
        filename = "/home/" + username + "/.config/dsm/data/processes.json"
        if not os.path.exists(filename):
               with open(filename, "w") as f:
                    pass 
        
        
        filename = "/home/" + username + "/.config/dsm/data/processes.json"
        with open(filename) as f:
                 num_lines = sum(1 for line in f)
           
        
        # create tabs
        app.add(" Console ")
        app.add(f" Processes ({num_lines})")
        app.add(" dpkg Log ")
        
        
        # Console
        app.text = ""
        def update_textbox():
            filename = "/home/" + username + "/.config/dsm/data/console.json"
            if not os.path.exists(filename):
               with open(filename, "w") as f:
                    pass
            global textbox
            with open("/home/" + username + "/.config/dsm/data/console.json", "r") as file:
                 new_text = file.read()
            if new_text != app.text:
               textbox.configure(state="normal")  # configure textbox to be editable
               textbox.delete("0.0", "end")  # clear textbox
               textbox.insert("0.0", new_text)  # insert updated text
               textbox.configure(state="disabled")  # configure textbox to be read-only
               app.text = new_text
            app.after(1000, update_textbox)
        
        global textbox
        textbox = customtkinter.CTkTextbox(master=app.tab(" Console "), width=600, height=316, font=('source code pro',14), corner_radius=12)
        textbox.place(x=0, y=0)
        textbox.configure(state="disabled") # configure textbox to be read-only
        app.after(1000, update_textbox)

        
        def write_processes_to_file():
            # Recupera la lista dei processi in esecuzione
            processes = list(psutil.process_iter())
            # Ordina i processi in base al consumo di CPU
            processes.sort(key=lambda process: process.memory_percent(), reverse=True)
            # Apri il file in modalità di scrittura
            with open("/home/" + username + "/.config/dsm/data/processes.json", "w") as file:
            # Per ogni processo in esecuzione
               for process in processes:
                try:
                   # Recupera informazioni sul processo
                   process_info = process.as_dict(attrs=["pid", "name", "status"])
                   # Recupera informazioni sul consumo di CPU e RAM del processo
                   cpu_percent = process.cpu_percent()
                   memory_info = process.memory_info().rss / 1024 / 1024
                   # Scrivi le informazioni sul processo nel file
                   file.write(f"{process_info['name']} {process_info['pid']}: - CPU: {cpu_percent}%, RAM: {memory_info:.2f} MB\n")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                   pass
            app.after(10000,write_processes_to_file)      
        
        app.after(1000,write_processes_to_file)        
        
         # Processes
        app.text2 = ""
        def update_textbox2():
            global textbox2
            with open("/home/" + username + "/.config/dsm/data/processes.json", "r") as file:
                 new_text = file.read()
            if new_text != app.text2:
               textbox2.configure(state="normal")  # configure textbox to be editable
               textbox2.delete("0.0", "end")  # clear textbox
               textbox2.insert("0.0", new_text)  # insert updated text
               textbox2.configure(state="disabled")  # configure textbox to be read-only
               app.text2 = new_text
            app.after(1000, update_textbox2)
        
        global textbox2
        textbox2 = customtkinter.CTkTextbox(master=app.tab(f" Processes ({num_lines})"), width=600, height=316, font=('source code pro',14), corner_radius=12)
        textbox2.place(x=0, y=0)
        textbox2.configure(state="disabled") # configure textbox to be read-only
        app.after(1000, update_textbox2)  
            
            
         # SysLog
       # os.system("cp -r /var/log/syslog.log /home/" + username + "/.config/dsm/data/syslog.log ")
        
        def copy_last_100_lines_of_file(src, dst):
            with open(src, "r") as src_file:
                 lines = src_file.readlines()
            with open(dst, "w") as dst_file:
                 dst_file.writelines(lines[-1000:])

        def copy_syslog_to_home():
            username = os.getlogin()
            filename = "/home/" + username + "/.config/dsm/data/manager.log"
            if not os.path.exists(filename):
                with open(filename, "w") as f:
                 pass
            src = "/var/log/dpkg.log"
            dst = "/home/" + username + "/.config/dsm/data/manager.log"
            copy_last_100_lines_of_file(src, dst)
            app.after(1000, copy_syslog_to_home)

        
        app.after(1000, copy_syslog_to_home)
        
        app.text3 = ""
        def update_textbox3():
            global textbox3
            with open("/home/" + username + "/.config/dsm/data/manager.log", "r") as file:
                 new_text = file.read()
            if new_text != app.text3:
               textbox3.configure(state="normal")  # configure textbox to be editable
               textbox3.delete("0.0", "end")  # clear textbox
               textbox3.insert("0.0", new_text)  # insert updated text
               textbox3.configure(state="disabled")  # configure textbox to be read-only
               app.text3 = new_text
            app.after(1000, update_textbox3)
        
        global textbox3
        textbox3 = customtkinter.CTkTextbox(master=app.tab(" dpkg Log "), width=600, height=316, font=('source code pro',14), corner_radius=12)
        textbox3.place(x=0, y=0)
        textbox3.configure(state="disabled") # configure textbox to be read-only
        app.after(1000, update_textbox3)      



#cpu-disk-ram-swap-boot
def update_values():
    disk_usage = psutil.disk_usage("/").percent
    disk_progress.set(value=disk_usage/100)
    disk_label.configure(text="Disk  {:.2f}%".format(disk_usage))

    ram_usage = psutil.virtual_memory().percent
    ram_progress.set(value=ram_usage/100)
    ram_label.configure(text="RAM  {:.2f}%".format(ram_usage))

    swap_usage = psutil.swap_memory().percent
    swap_progress.set(value=swap_usage/100)
    swap_label.configure(text="Swap  {:.2f}%".format(swap_usage))
    
    cpu_usage = psutil.cpu_percent()
    cpu_progress.set(value=cpu_usage/100)
    cpu_label.configure(text="CPU  {:.2f}%".format(cpu_usage))
 
    boot_partition_usage = psutil.disk_usage("/boot").percent
    boot_partition_progress.set(value=boot_partition_usage/100)
    boot_partition_label.configure(text="Boot {:.2f}%".format(boot_partition_usage))

    app.after(1000, update_values)


app.after(1000, update_values)

cpu_label = customtkinter.CTkLabel(app, text="CPU" , fg_color=('#dbdbdb','#2b2b2b'))
cpu_label.place(x=845, y=237)

cpu_progress = customtkinter.CTkProgressBar(app, height=5, width=130, progress_color="red")
cpu_progress.place(x=845, y=260)

disk_label = customtkinter.CTkLabel(app, text="Disk ", fg_color=('#dbdbdb','#2b2b2b'))
disk_label.place(x=845, y=267)

disk_progress = customtkinter.CTkProgressBar(app, height=5, width=130, progress_color="#0f94d2")
disk_progress.place(x=845, y=290)

ram_label = customtkinter.CTkLabel(app, text="RAM ", fg_color=('#dbdbdb','#2b2b2b'))
ram_label.place(x=845, y=297)

ram_progress = customtkinter.CTkProgressBar(app, height=5,width=130, progress_color="orange")
ram_progress.place(x=845, y=320)

swap_label = customtkinter.CTkLabel(app, text="Swap ", fg_color=('#dbdbdb','#2b2b2b'))
swap_label.place(x=845, y=327)

swap_progress = customtkinter.CTkProgressBar(app, height=5,width=130, progress_color="magenta")
swap_progress.place(x=845, y=350)

boot_partition_label = customtkinter.CTkLabel(app, text="Boot ", fg_color=('#dbdbdb','#2b2b2b'))
boot_partition_label.place(x=845, y=357)

boot_partition_progress = customtkinter.CTkProgressBar(app, height=5,width=130, progress_color="#55ff00")
boot_partition_progress.place(x=845, y=380)

def count_installed_packages():
    output = subprocess.run(['pikaur', '-Q'], stdout=subprocess.PIPE)
    packages = output.stdout.decode('utf-8').split('\n')
    return len(packages)


def update_kernel_info():
    kernel = platform.release()
    kernel_label.configure(text="Kernel: {}".format(kernel))
    kernel_label.after(1000, update_kernel_info)
    
kernel_label = customtkinter.CTkLabel(app, text="Kernel: ...", fg_color=('#dbdbdb','#2b2b2b'))
kernel_label.place(x=845, y=165)
app.after(1000, update_kernel_info)

def update_mirrorlist_info():
    mirrorlist = subprocess.run(['bash', '-c', 'mirrorlist=$(cat /etc/pacman.d/mirrorlist | wc -l ); diff=$( expr $mirrorlist - 10); echo $diff'], capture_output=True, text=True)
    diff = int(mirrorlist.stdout.strip())
    mirrorlist_label.configure(text="Server Mirrors: {}".format(diff))
    mirrorlist_label.after(1000, update_mirrorlist_info)

mirrorlist_label = customtkinter.CTkLabel(app, text="Server Mirrors: ...", fg_color=('#dbdbdb','#2b2b2b'))
mirrorlist_label.place(x=845, y=185)
app.after(1000, update_mirrorlist_info)

def update_packages_info():
    packages = count_installed_packages()
    label.configure(text="Packages: {}".format(packages))
    label.after(1000, update_packages_info)

label = customtkinter.CTkLabel(app,fg_color=('#dbdbdb','#2b2b2b'),text="Packages: {}".format(count_installed_packages()))
label.place(x=845, y=205)
app.after(1000, update_packages_info)





app.tab_view = MyTabView(master=app, width=610, height=365,)
app.tab_view.place(x=203, y=35)



app.mainloop()