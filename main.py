import wmi
import psutil
import sys
import os


#     -Variable declaration-
#   Loop control
running_script = True

#       -Function Def-

#Menu selection and redirection
def direct_user(user_input):
    match user_input:
        case "1":
            display_project_info()
        case "2":
            display_general_hardware_info()
        case "3":
            display_cpu_info()
        case "4":
            display_gpu_info()
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
    return

# Display a general summary of the users hardware and specs
def display_general_hardware_info():
    return

# Display CPU info
def display_cpu_info():
    return 

# Display GPU info 
def display_gpu_info():
    return

# Display Storage info
def display_storage_info():
    return


#           -Script Startup-
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




#P_core_count = psutil.cpu_count(logical=False)
#thread_count = psutil.cpu_count()

#print("--- CPU Information ---")
#print("Physical Core Count: " + str(P_core_count))
#print("Number of Threads: " + str(thread_count))

