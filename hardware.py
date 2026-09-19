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

    def __init__(self, h_list):
        super().__init__(h_list)
        self.cpu_info = self.dictionary_setup()

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

    # This will be the place we will store most our info for the advanced info
    # We do this so we do not need to constantly call the WMI and all in that function
    # Just ask from the class should be faster
    def dictionary_setup(self):
        # The main reason i am using a dict is to support multiple CPUs if for any reason there is some 
        dictionary = {}

        dictionary["Manufactor"] = []
        dictionary["Architect"] = []
        dictionary["PhysCore"] = []
        dictionary["LogCore"] = []
        dictionary["MaxClock"] = []
        dictionary["L2"] = []
        dictionary["L3"] = []

        for item in self.information:
        # Manufactor
            dictionary["Manufactor"].append(str(item.Manufacturer))
        # Architecture
            dictionary["Architect"].append(str(item.Architecture))
        # Physical Core
            dictionary["PhysCore"].append(str(item.NumberOfCores))
        # Logical Core
            dictionary["LogCore"].append(str(item.NumberOfLogicalProcessors))
        # Max Clock Speeds
            dictionary["MaxClock"].append(str(item.MaxClockSpeed))
        # L2 caches
            dictionary["L2"].append(str(int(item.L2CacheSize)/1024))
        # L3 caches
            dictionary["L3"].append(str(int(item.L3CacheSize)/1024))
        return dictionary

# Follow the same structure as the CPU class basically
class GPU(Hardware):

    def __init__(self, h_list):
        super().__init__(h_list)
        self.gpu_info = self.dict_setup()

    def dict_setup(self):
        return_dict = {}

        return_dict["Manufact"] = []
        return_dict["VideoProc"] = []
        return_dict["RefreshRate"] = []
        return_dict["Status"] = []
        return_dict["DeviceId"] = []

        for item in self.information:
            return_dict["Manufact"].append(str(item.AdapterCompatibility))
            return_dict["VideoProc"].append(str(item.VideoProcessor))
            if int(item.MaxRefreshRate) == 0:
                return_dict["RefreshRate"].append(str(item.MaxRefreshRate)+" GPU is not the display driving adaptor ATM")
            else:
                return_dict["RefreshRate"].append(str(item.MaxRefreshRate))
            return_dict["Status"].append(str(item.Status))
            return_dict["DeviceId"].append(str(item.DeviceID))

        return return_dict

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
            final_string += "\t STICK " + str(count_for_ram) + ":\n\t\t CAPACITY: " + str(self.gb_capacity[count_for_ram-1]) + " GB\n\n"
            count_for_ram += 1
        return final_string


# LogicalDisk to partition object helper with the class below
class LD2P_object:

    def __init__(self,Device_id,Capacity,Freespace):
        self.Device_id = Device_id
        self.capacity = Capacity
        self.freespace = Freespace


class Storage:

    def to_gb (self,num):
        return ((int(num)) / (1000 ** 3))

    def __init__(self, hard_list, logic_list):
        self.raltion = wmi.WMI().Win32_LogicalDiskToPartition()
        self.physical_hardware = hard_list
        self.logical_hardware = logic_list
        self.important_relations = self.important_setup()
        self.valued_partition_count = self.valued_partition_ctSetup()
        


    def string_general_info(self):
        final_string = "STORAGE: \n"
        Capacity = ""

        
        count = 1
        for item in self.physical_hardware:
            # Some systems may return NONE for the item.Size so i will use a try catch to help out 
            # This is the same with MediaType and InterfaceType but those can use a simple str wrap as we are not calculating anything
            try:
                Capacity = str(round(((int(item.Size)) / (1000 ** 3)), 2))
            except(TypeError, ValueError):
                Capacity = "NONE"

            final_string += "\t Drive "+ str(count) + " :" + item.Model + "\n"
            final_string += "\t\t Capacity: " + Capacity  + " GB\n"
            final_string += self.free_space_return(count-1)
            final_string += "\t\t Media Type: " + str(item.MediaType) + "\n"
            final_string += "\t\t Interface: " + str(item.InterfaceType) + "\n\n"
            count += 1
        return final_string

    # We need the update values function for storage unlike RAM
    def update_values(self,hard_list,logic_list):
        self.physical_hardware = hard_list
        self.logical_hardware = logic_list
        self.raltion = wmi.WMI().Win32_LogicalDiskToPartition()

    def important_setup(self):
        # Just found this extremly useful object, did not see it before gives so much good info and solves big partition problem
        # Dependent is key here
        relation = self.raltion
        
        # Set up a dictionary for easy acess to important partitions
        # Will map it out with ID:(this will be like OS and stuff so each logical disk gets matched to appropriate physical disk)
        # Then each of these will containt a list of objects with info towards the free space per partiton
        # This may make the editor a little packed but as this is first project with WMI i will optimize in V2
        mapper = {}
        for x in relation:
            vol_name = str(x.Dependent.VolumeName)
            temp_obj_holder = LD2P_object(str(x.Dependent.DeviceID),str(x.Dependent.Size),str(x.Dependent.FreeSpace))
        
            # Quick Key check for the dict
            if mapper.get(vol_name) is None:
                mapper[vol_name] = []
        
            # Add to the dict
            mapper[vol_name].append(temp_obj_holder)

        return mapper

    def valued_partition_ctSetup(self):
        arr_map = [0] * len(self.physical_hardware)
        
        setup_count = 0
        for item in self.important_relations:
            for part in item[1]:
                arr_map[setup_count] += 1
            setup_count += 1

        return arr_map

    def free_space_return(self,num):
        final_string = ""

        # This was the most messy function to write so far will clean up the whole process in V2
        # Really happy i was able to get it running had me stumped definitly a little messy tried to clean it up where i could
        for i in range(0, self.valued_partition_count[num]):
            final_string += "\t    Drive Letter: " + str(list(self.important_relations.values())[num][i].Device_id) + "\n"
            final_string += "\t\t Capacity of Drive: " +str(self.to_gb(int(list(self.important_relations.values())[num][i].capacity))) + " GB\n"
            final_string += "\t\t Free space of Drive: " +str(self.to_gb(int(list(self.important_relations.values())[num][i].freespace))) + " GB\n\n"



        return final_string



