import wmi
import psutil


# Variable declaration 
P_core_count = psutil.cpu_count(logical=False)
L_core_count = psutil.cpu_count()

print("--- CPU Information ---")
print("Physical Core Count: " + str(P_core_count))
print("Number of Threads: " + str(L_core_count))

