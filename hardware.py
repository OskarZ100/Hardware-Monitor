import wmi
import psutil
import sys
import os
#       -Classes setup-
# A lot of repetition happening so made subclasses 
class Hardware:
    def __init__(self, h_list):
            self.amount = len(h_list)
            self.information = h_list
            self.names = self.setup_names()
    
    def setup_names(self):
        names = []
    
        for items in self.information:
            names.append(items.Name)
    
        return names

    def update_values(self,hardware_list):
            self.information = hardware_list


class CPU(Hardware):


    # Returns a basic summary of CPU info to display to user in Gen info func
    def string_general_info(self):
        final_string = ""

        if self.amount == 1:
            final_string += "CPU: " + self.names[0] + "\n"
            final_string += "\t USAGE: " + str(self.information[0].LoadPercentage) + "%\n\n"
        else:
            count_of_cpus = 1
            for name in self.names:
                final_string += "CPU " + str(count_of_cpus) + ": " + name + "\n\n"
                final_string += "\t USAGE: " + str(self.information[count_of_cpus-1].LoadPercentage) + "%\n\n"
                count_of_cpus += 1

        return final_string

# Follow the same structure as the CPU class basically
class GPU(Hardware):

    def string_general_info(self):
        final_string = ""

        if self.amount == 1:
            final_string += "GPU: " + self.names[0] + "\n"
            final_string += "\t STATUS: " + str(self.information[0].Status) + "\n\n"
        else:
            count_for_gpus = 1
            for name in self.names:
                final_string += "GPU " + str(count_for_gpus) + ": " + name + "\n\n"
                final_string += "\t STATUS: " + str(self.information[count_for_gpus-1].Status) + "\n\n"
                count_for_gpus += 1

        return final_string

class RAM(Hardware):

    def __init__(self, h_list):
        super().__init__(h_list)

        self.gb_capacity = self.get_capacity()

    def get_capacity(self):
        ram_capacity = []
        for item in self.information:
            ram_capacity.append(int(item.Capacity) / (1024 ** 3))

        return ram_capacity

    def string_general_info(self):
        final_string = "RAM: \n OVERALL USAGE: " + str(psutil.virtual_memory().percent) + "%\n"

        count_for_ram = 1
        for item in self.information:
            final_string += "\t STICK " + str(count_for_ram) + ":\n\t\t CAPACITY: " + str(self.gb_capacity[count_for_ram-1]) + "\n\n"
            count_for_ram += 1
        return final_string