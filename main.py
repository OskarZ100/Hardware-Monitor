# Need these to actually pull info
import wmi
import psutil
import sys
import os

# For update function
import threading
import time
import pythoncom

# My classes 
from hardware import CPU, GPU, RAM, Storage



#     -Variable declaration-

#   WMI variables
cpu_list = wmi.WMI().Win32_Processor()
gpu_list = wmi.WMI().Win32_VideoController()
ram_list = wmi.WMI().Win32_PhysicalMemory()
drive_list = wmi.WMI().Win32_DiskDrive()
disk_list = wmi.WMI().Win32_LogicalDisk()

#   Static computer vars
my_cpu = CPU(cpu_list)
my_gpu = GPU(gpu_list)
my_ram = RAM(ram_list)

my_storage = Storage(drive_list, disk_list)

#   Loop control
running_script = True

# Architect is mapped in code for soem reason 
arch_map = ["x86","MIPS","Alpha","PowerPC","","ARM","Itanium","","","x64"]

#       -Function Def-

#Menu selection and redirection
def direct_user(user_input):
    match user_input:
        case "0":
            display_project_info()
        case "1":
            display_general_hardware_info()
        case "2":
            display_cpu_info()
        case "3":
            display_gpu_info()
        case "4":
            display_ram_info()
        case "5":
            display_storage_info()
        case "6":
            os.system("cls")
            return
        case "7":
            sys.exit("Ending Session")
        case _:
            print("\nInput is a plain number no spaces try again and select a valid input\n")
            return

# Display info about the project and me
def display_project_info():
    print("\n\n" \
    "\t\t -Project Information-\n" \
    "Hello, welcome to my hardware monitor my name is Oskaras Zincenko\n" \
    "As of writing this i am a student at CSU a member of the USCG and-\n" \
    "I also currently work at best buy, i host a channel where i am going-\n" \
    "to document my dev progress, i really enjoy learning about hardware.\n" \
    "Although this V1 of the project is basic i plan to make a GUI out of-\n" \
    "this and then want to possibly do something fancy for V3.\n" \
    "it is currently 9/9/2026 my goals are\n" \
    "gain hardware setup and experience\n" \
    "cooler projects but like interesting ones not copy paste snooze fest\n" \
    "get internship or co-op\n\n" \
    "press enter to go back to menu!\n")
    input()
    os.system("cls")
    return

# Display a general summary of the users hardware and specs
def display_general_hardware_info():
    print("\t\t -General Hardware Info-\n" \
    + my_cpu.string_general_info() +
    my_gpu.string_general_info() + \
    my_ram.string_general_info() + \
    my_storage.string_general_info()) 
    #ADD WARNINGS LIKE MAYBE stuff where its like ok this is weirdly high or overused at bottom
    print("\n\n\n Press enter to go back to menu!\n")
    input()
    os.system("cls")
    return

# Display CPU info
def display_cpu_info():
    # Base setups
    # Idea is to have a static string that displays like the info that dont change
    # Then a live updating thing to show usage and stats like that

    # Space and resource consuming but i want it to look neat
    space = " "
    if len(my_cpu.names) > 1:
        space = "/"
    static_string = "\n\t\t |--CPU Extended Look--|\n"
    static_string += "\t----------------------------------------\n"

    quick_dict = my_cpu.cpu_info

    for x in range(0, len(my_cpu.names)):
        static_string += "CPU#" + str(x+1) + "\n"
        static_string += "Name: " + my_cpu.names[x] + "\n"
        static_string += "\tManufacturor: " + quick_dict["Manufactor"][x] + "\tArchitecture: " + arch_map[int(quick_dict["Architect"][x])] + "\n"
        static_string += "\tCores: " + str(quick_dict["PhysCore"][x]) + "\tThreads: " + str(quick_dict["LogCore"][x]) + "\n"
        static_string += "\tMax Clock Speed: " + str(quick_dict["MaxClock"][x]) + " MHz\n"
        static_string += "\tL2 Cache: " + str(quick_dict["L2"][x]) + " MB" + "\tL3 Cache: " + str(quick_dict["L3"][x]) + " MB\n"
        static_string += "\t----------------------------------------"
    print(static_string)
    #print("\033[2A")  move it up like 2 but technically only one line for u 
    #print("\033[2K")  then clear it 
    # prob a move clear loop going on would work 

    print("\t\t - LIVE DATA -\n")

    # LIVE DATA DISPALY 

    # Need a thread event to wait for input properly
    user_stop = threading.Event()

    temp_live_display = "\tSpeed: " + str(psutil.cpu_freq().current) + "\n"
    temp_live_display += "\tOverall usage: " + str(psutil.cpu_percent()) + "% \n"
    print(temp_live_display)
    threading.Thread(target=cpu_live_update,args=(user_stop,),daemon=True).start()

    input()
    user_stop.set()
    os.system("cls")
    return
     
def cpu_live_update(stop):
    pythoncom.CoInitialize()
    running = True
    while not stop.is_set():
        print("\033[4A", end="")
        print("\033[2K")
        temp_live_display = "\tSpeed: " + str(psutil.cpu_freq().current) + "\n"
        temp_live_display += "\tOverall usage: " + str(psutil.cpu_percent()) + "% \n"
        temp_live_display += "\tPRESS ENTER TO STOP"
        print(temp_live_display)
        time.sleep(2)




# Display GPU info 
def display_gpu_info():
    return

# Display RAM info 
def display_ram_info():
    return 

# Display Storage info
def display_storage_info():
    return

# Update function to maintain updated values
def update():
    pythoncom.CoInitialize() #WIM auto handles like the setup in main thread but need to have COM access in this thread so this fixes that
    while True:
        my_cpu.update_values(wmi.WMI().Win32_Processor())
        my_gpu.update_values(wmi.WMI().Win32_VideoController())
        my_storage.update_values(wmi.WMI().Win32_DiskDrive(),wmi.WMI().Win32_LogicalDisk())
        time.sleep(5)

#           -Script Startup-
def main():
    threading.Thread(target=update, daemon=True).start()
    print("Welcome to the Hardware Monitor V1 by Oskaras Zincenko")
    print("Select an option from the menu to begin\n")

    #           -Loop for menu-
    while running_script:
        print("\t\t---- MENU ----\n" \
            "0. Info about project\n" \
            "1. General Hardware info\n" \
            "2. CPU info\n" \
            "3. GPU info\n" \
            "4. RAM info\n" \
            "5. Storage info\n" \
            "6. clear screen\n" \
            "7. exit\n" \
            "\t\t--------------")

        user_input = input()
        direct_user(user_input)

if __name__ == "__main__":
    main()



#P_core_count = psutil.cpu_count(logical=False)
#thread_count = psutil.cpu_count()

#print("--- CPU Information ---")
#print("Physical Core Count: " + str(P_core_count))
#print("Number of Threads: " + str(thread_count))

