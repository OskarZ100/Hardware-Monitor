## READ ME
Welcome to my Hardware Monitor project, this was a project I made for fun that will display info about your
hardware, specifically your CPU, GPU, RAM and Storage. It is not a super complicated project but had fun
making it work and going through trial and error as you can see in the comments I left.

## REQUIREMENTS AND SETUP
- Windows
- Python

Install WMI and psutil and pywin32

```
pip install psutil WMI pywin32
```

These are super important as it relies on these libraries and dependencies 

Then once all installed head over to your terminal, cd to the location of the file and run 

```
py .\main.py
```

And the program should run 

## Demonstration of program 
<br>
After running the program you should get a prompt displaying the functions of the program <br>
<br>
<p align="center"><img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/45932c73-a777-420a-9bea-fdcf454efd20" /></p>
<br>
The only inputs the program will accept are

```
0,1,2,3,4,5,6, or 7
```

If you enter a non valid input the program will display, and prompt the menu again  

```
Input is a plain number no spaces try again and select a valid input
```

<br>
As shown, 
<br>
<p align="center"><img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/d0430c1b-7466-43a3-9bef-ae26ca614e95" /></p>
<br>

### (0) - Info About Project command
Displays basic like info about me and the project nothing fancy at all

### (1) - General Hardware Info 
Displays static general info about every component featured <br>
These are values grabbed at the exact time the function is called <br>
Updated live values only show up in the specific functions of each hardware component<br>
<br>
<p align="center"><img width="400" height="600" alt="image" src="https://github.com/user-attachments/assets/78b96b7d-6022-4df2-a7db-3ff8b068e1fc" /></p>
<br>
<br>
As you can see it is pretty bare bones, that is by design as I did not want to give too much detail on a general info command

#### QUICK INFO
At the end of every command (except if you enter a non valid command) it will prompt you to press enter clear the console and print
the menu again 
Like this <br>

```
 Press enter to go back to menu!
```

### (2) - CPU information
On entering this command it will display a set of basic static information about your CPU <br>
If for any reason the user has multiple CPUs it will support this <br>
It will also have a live data section that updates every 2 seconds utilizing threading<br>
Live data displays usage and speed I got the live updated data through psutil rather than WMI as it is less taxing<br>
WMI was still used in all update functions just to grab how many items are in the sets<br>

<p align="center"><img width="400" height="300" alt="cpuinfo" src="https://github.com/user-attachments/assets/05749a91-6c81-4e1d-8786-56ae830d9924" /></p>
<br>

### (3) - GPU information 
This command will display information about any GPUs on the system <br>
This only contains basic static data <br>
The reason for this I go more into depth on in the documentation section but it boils down to the way windows calculates this <br>

<p align="center"><img width="600" height="350" alt="image" src="https://github.com/user-attachments/assets/48356089-0a6c-499e-9f0a-443f5d908288" /></p>
<br>

### (4) - RAM information 

This will show you RAM information, follows same sort of blueprint like the CPU command <br>
shows static data on top with general live information in the live section <br>
I decided to just show the total usage with the live data as it is much neater in my opinion <br>

<p align="center"><img width="250" height="250" alt="raminfo" src="https://github.com/user-attachments/assets/8a8ac297-5931-4297-b69a-c3ba79bb129b" /></p>
<br>

### (5) - Storage information

Shows as you guessed, basic storage information with a live display that utilizes psutil <br>
In this project I found many ways to display free space, I had such such such an easier time using psutil <br>
WMI process for free space was one of the harder and annoying things to implement while psutil took me like 5 min
<br>
<p align="center"><img width="280" height="300" alt="image" src="https://github.com/user-attachments/assets/ab7e3ac7-68e6-415a-b96b-e3b486d74dc4" /></p>
<br>

### (6) - Clear console

Very straight forward command, just clear the console incase you somehow misinputed a ton of stuff <br>

<p align="center"><img width="250" height="250" alt="clearscreen" src="https://github.com/user-attachments/assets/eadbb9e8-31e8-469f-90c1-1ad63e0b826d" /></p>
<br>

### (7) - End session
Again pretty self explanatory, ends process ez <br>
<p align="center"><img width="250" height="250" alt="end" src="https://github.com/user-attachments/assets/343c7236-bfe1-448b-a945-94145bc69d4c" /></p>
<br>

## Documentation

I want to kind of just go through some of the program here and stuff I did
It was a little messy but that is because I wanted to experiment and explore different ways of doing things so I can optimize everything for later versions

### Hardware.py classes

I decided to store my classes in a separate file and import into main to maintain a clean main environment
The classes could get pretty messy and long with certain functions

#### Hardware (BASE class)

This is the Superclass to a lot of the other classes you will see
I made this to be more efficient and clean, as you can see it doesn't really have anything crazy 

```
class Hardware:
    def __init__(self, h_list):
            self.amount = len(h_list) <-- This value does not look too important but comes in handy in a few subclass functions
            self.information = h_list <-- Just storing each actual hardware piece for what I am calling
            self.names = self.setup_names() <-- Getting names, this just makes future calls easier for me
    
    def setup_names(self): <-- Super simple function to get the names
        names = []
    
        for items in self.information:
            names.append(items.Name)
    
        return names

    def update_values(self,hardware_list): <-- Helps the update function, makes sure our values are not just snapshots taken at program runtime
            self.information = hardware_list
```

#### CPU subclass of hardware

This is to handle everything CPU \
Helps with the in depth function in main and the general one \
Again this will follow the same sort of trend as you see in the other classes but they all have slightly different versions of the same sort of function 

```
class CPU(Hardware):

    def __init__(self, h_list):
        super().__init__(h_list)
        self.cpu_info = self.dictionary_setup() <-- Sets up all the data we need for the in depth call

    def string_general_info(self): <-- All subclasses have this function, simple string and info return
        final_string = "" <-- I feel there are many ways to handle this maybe not most efficient but cleanest for me to follow
        

        if self.amount == 1:
            final_string += "CPU: " + self.names[0] + "\n"
            final_string += "\t USAGE: " + str(self.information[0].LoadPercentage) + "%\n\n" <-- Wanted to use WMI, psutil is faster if its just one though
        else: <-- Added this so if there is not more than one we dont gotta go thru the whole loop 
            count_of_cpus = 1
            for name in self.names:
                final_string += "CPU " + str(count_of_cpus) + ": " + name + "\n\n"
                final_string += "\t USAGE: " + str(self.information[count_of_cpus-1].LoadPercentage) + "%\n\n"
                count_of_cpus += 1

        return final_string
```

The dictionary setup is pretty basic I just setup all the keys I want \
Then I loop through all the objects in information and store accordingly \
Super simple

#### GPU subclass of hardware

Handles everything GPU! \
Pretty much the exact same setup as CPU class \
Just slight changes in the general info function obviously and with the dictionary setup there is one difference here 

```
 if int(item.MaxRefreshRate) == 0:
   return_dict["RefreshRate"].append(str(item.MaxRefreshRate)+" GPU is not the display driving adaptor ATM")
 else:
   return_dict["RefreshRate"].append(str(item.MaxRefreshRate))
```

Ok as you can see this is a little different \
I learned while doing the project that if you have more than one GPU there will be one display driving adaptor \
In my case on laptop I have a dedicated GPU and internal GPU which ever is the display driving adaptor \
So if it shows a 0 my program will assume and tell you which is the adaptor and not \
Now if your GPU is just lets say completely cooked, it will not be the display driving adaptor so obviously will show that \
and status will let you know how it is doing, for anyone like well what if the GPU just blew up there u go 

#### RAM subclass of hardware

Again handles everything RAM \
Now this is the same exact setup as the CPU and GPU \
But there is a specific function it has which is getting its Capacity specifically in GB \
WMI likes to give everything in bytes which is a pain so this handles getting Capacity and storing in an array \
So when we want to see the capacity we dont need to make a taxing WMI call but just a simple array call 

```
    def __init__(self, h_list):
        super().__init__(h_list)
        self.dict = self.dict_setup()
        self.gb_capacity = self.get_capacity() < --- Makes the call

    def get_capacity(self):
        ram_capacity = [] <--- Set up our array 
        for item in self.information: <--- Go through each stick
            ram_capacity.append(int(item.Capacity) / (1024 ** 3)) <--- Convert and send through

        return ram_capacity
```

Super simple the reason I keep this in an array and don't think it needs updates is because \
I do not think the user will be switching out or downloading more RAM while program is running :) 

#### Storage and LD2P classes 

This was probably the harder part of the project because I made it much harder than it needed to be by using WMI and not psutil \
So psutil actually has a function you can use to get free space and I use it in main.py 

```
my_storage.to_gb(psutil.disk_usage(psutilcombo).free)
```

As you can see you just pass in a logical drive, but it has to have a drive letter is the thing 

---

Now for the storage class I decided to make a whole new class not a subclass of Hardware because it just didnt make sense to me \
There are so many different things between the two and Storage objects in WMI act very differently than the rest \
It has a physical drive, logical disk, and partitions and all these get kind of messy when trying to figure certain things out \
So I was just like lets make this easier to navigate and write than forcing compatibility 

So here is kind of the basic setup of the class 

```
class Storage:

    def to_gb (self,num): <--- Super helpful function as I convert A LOT in here
        return ((int(num)) / (1000 ** 3)) <--- GB not GiB

    def __init__(self, hard_list, logic_list):
        self.raltion = wmi.WMI().Win32_LogicalDiskToPartition() <-- Useful partitions here
        self.physical_hardware = hard_list <-- Physical drive
        self.logical_hardware = logic_list <-- Logical disk
        self.important_relations = self.important_setup() <-- The super annoying function for setting up partitions
        self.valued_partition_count = self.valued_partition_ctSetup() <-- Things we use to calculate values
```

There is a lot of setup in this class as you can see \
The to_gb function actually comes in clutch in a lot of functions here and in main \
So the "raltion" I misspelt relation but wanted to keep it, is helping with the setup specifically important setup function \
logical and physical hardware setups are pretty straight forward nothing crazy here 

---

Now this function was something that I was happy when I made but hated making

```
    def important_setup(self):
        relation = self.raltion
        
        mapper = {}
        for x in relation:
            vol_name = str(x.Dependent.VolumeName)
            temp_obj_holder = LD2P_object(str(x.Dependent.DeviceID),str(x.Dependent.Size),str(x.Dependent.FreeSpace))
        
            if mapper.get(vol_name) is None:
                mapper[vol_name] = []
        
            mapper[vol_name].append(temp_obj_holder)

        return mapper
```

I learned how to spell relation here \
I also wanted to map out the the specific volume name to the partitions \
So when I go to display data to the user its not just showing random partitions but neat and nice, like the correct volume what disk and all that \
As you can see I use a dictionary again here, really big fan of those sometimes there are better options to use but these are more comfortable for me and V1 \
Also as you can see we use what is called a Dependent which is honestly an INSANLY helpful object, like it gives you a full list of basically anything and everything you need with a logical disk, also it will give you the partition you need and actually want instead of the random ones nobody cares about \
So when I found that out I was very happy and you can tell by the comments in the actual code 

---

Now LD2P real quick was a super basic class I made 

```
class LD2P_object:

    def __init__(self,Device_id,Capacity,Freespace):
        self.Device_id = Device_id
        self.capacity = Capacity
        self.freespace = Freespace
```

The whole purpose of LD2P is Logical drive 2 partition \
It helps out the setup by making it more readable and less sort of cross over-ish \
So when I add it to the dictionary all the info you could possibly want from our massive Dependent object from WMI is compressed into what we actually want, and nice and neat instead of having to go through the whole call again 

---

Now the valued partition function 

```
    def valued_partition_ctSetup(self):
        arr_map = [0] * len(self.physical_hardware)
        
        setup_count = 0
        for item in self.important_relations:
            for part in item[1]:
                arr_map[setup_count] += 1
            setup_count += 1

        return arr_map
```

This function is more for us to tell how many important partitions do we have per physical drive \
Again all of this is for the simple task of displaying data and how much free space we have \
Pretty sure an Enum could have been used here, but I didn't use it, honestly in my opinion would have made it more confusing to read 

---

Now here is the free space return function 

```
    def free_space_return(self,num):
        final_string = ""

        for i in range(0, self.valued_partition_count[num]):
            final_string += "\t    Drive Letter: " + str(list(self.important_relations.values())[num][i].Device_id) + "\n"
            final_string += "\t\t Capacity of Drive: " +str(self.to_gb(int(list(self.important_relations.values())[num][i].capacity))) + " GB\n"
            final_string += "\t\t Free space of Drive: " +str(self.to_gb(int(list(self.important_relations.values())[num][i].freespace))) + " GB\n"

        return final_string
```

It just goes through all the valued partitions of the drive we are on, then will show you the drive letter and the free space \
Sounded simple, was not \
Again pretty sure if I used a psutil approach it would have been a LOT easier but for V1 wanted to explore many different ways of doing things, as it is my first time using WMI and psutil

---

Also for the to string function, I added a try/except in case the capacity was empty for whatever reason 

```
            try:
                Capacity = str(round(((int(item.Size)) / (1000 ** 3)), 2))
            except(TypeError, ValueError):
                Capacity = "NONE"
```

In case there is true it will just show NONE, simple 

### main.py 

Now time for the main file where everything comes together \
Nothing too crazy here main focus was trying to keep it readable, and organized \
A lot of the variables are self explanatory but I will attempt to explain the ones that might be on the fence

---

```
arch_map = ["x86","MIPS","Alpha","PowerPC","","ARM","Itanium","","","x64"]
```

So as you can see above arch_map seems like an array with a bunch of random values \
This array actually comes in helpful when returning CPU architecture \
For some reason WMI when you want the architecture type for the processor it returns some random number and it doesn't even go in order \
So I just looked up and mapped out what each number mapped out to 

---

Here is the super simple main script 

```
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
```

Very simple and self explanatory, only reason I include it is to explain a few things \
The thread we use at the start is to keep values of hardware updated, it itself is also pretty simple \
Each class has an update function attached to it that just resets and calls WMI again \
For V2 I think I might ditch that idea, although it probably wont it definitely is not efficient and could maybe do some bottlenecking \
Or performance spiking at the least \
The update function just runs infinitely until program closes via daemon 

---

```
def update():
    pythoncom.CoInitialize() 
    while True:
        my_cpu.update_values(wmi.WMI().Win32_Processor())
        my_gpu.update_values(wmi.WMI().Win32_VideoController())
        my_storage.update_values(wmi.WMI().Win32_DiskDrive(),wmi.WMI().Win32_LogicalDisk())
        time.sleep(5)
```

Again pretty simple, Call CoInitialize() so it can actually call and use WMI \
I do not close it because the only way the loop can stop is through the program terminating so no point really

Many of the display functions in this part of the program follow a very similar method 

---

```
def display_ram_info():
    for x in range(my_ram.amount):
        print("\t\t--- STICK #" + str(x) + " ---")
        print("\tCapacity: " + str(my_ram.gb_capacity[x]) + " GB")
        print("\tManufacturor: " + my_ram.dict["man"][x])
        print("\tSpeed: " + my_ram.dict["speed"][x] + " MHz")
        print("\tForm Factor: " + my_ram.dict["formfact"][x])
        print()

    print("\t\t-- LIVE DISPLAY --")
    user_stop = threading.Event()
    temp_live_display = "\tTotal Usage: " + str(psutil.virtual_memory().percent) + "%\n"
    temp_live_display += "\tSwap usage: " + str(psutil.swap_memory().percent) + "% \n"
    print(temp_live_display)
    threading.Thread(target=ram_live_update,args=(user_stop,),daemon=True).start()

    input()
    user_stop.set()
    os.system("cls")
```

Take RAM for example, it has a static section that remains unchanged when called and displays data we can get from the dictionary we set up with all our classes \
This is the same for the CPU and GPU too and even Storage has its own little version \
The live display feature now \
I set up a thread for each of the live displays for all hardware \
The event is setup so whenever the user wants to move on it will close that thread and clear the console and reprint the menu \
This is done to keep the console free of clutter \
I use psutil for the live display as again it is far more efficient than having to update and call WMI over and over 

---

```
def ram_live_update(stop):
    while not stop.is_set():
        clear_line(3)
        temp_live_display = "\tTotal Usage: " + str(psutil.virtual_memory().percent) + "%\n"
        temp_live_display += "\tSwap Usage: " + str(psutil.swap_memory().percent) + "% \n"
        temp_live_display += "\tPRESS ENTER TO STOP"
        print(temp_live_display)
        time.sleep(2)
```

This is the update function \
Again pretty much the same thing for GPU and storage \
Do not need CoInitialize here as no WMI usage \
But pretty simple exits on any input given by user

---

```
def clear_line(amnt):
    for x in range(0,amnt):
        print("\033[1A\033[2K", end="")
```

This I have not really done before but it will move up and clear the line that cursor is on \
Nothing actually too crazy \
Didn't want to have to clear and repaste the static and live together just the live part so I made this

One interesting road block that I will further try to tackle in V2, was the lack of info given for the GPU \
For some reason WMI and psutil do not really have much to give in this field \
I wanted to do some calculations and figure out what counters windows uses to give out a GPU usage percentage \
But I couldn't find anything at all, and when you try to call each individual driver through WMI, it will return the messiest clump of different drivers you have ever seen and apparently there is a specific way windows uses counters to calculate the total usage but I was not able to figure it out and implement it here \
Definitely something to look into further in V2 maybe through an alternative library \
Did not want to use a whole lot of libraries for this so didn't go about that 

---

```
def update_storage(stop):
    pythoncom.CoInitialize()
    while not stop.is_set():
        clear_line((4*len(my_storage.logical_hardware))+1)
        for i in my_storage.logical_hardware:
            if not i.DeviceID == None:
                devid = i.DeviceID
                psutilcombo = str(devid + "\\")
                print("\tDrive Letter: " + devid)
                print("\tCapacity: " + str(round(my_storage.to_gb(psutil.disk_usage(psutilcombo).total),2))+ " GB")
                print("\tFree Space: " + str(round(my_storage.to_gb(psutil.disk_usage(psutilcombo).free),2)) + " GB")
                print("\tPercentage: " + str(psutil.disk_usage(psutilcombo).percent) + "%")
                

        print("\tPRESS ENTER TO STOP")
        time.sleep(10)
    pythoncom.CoUninitialize()
```

Now I want to show this \
This is the storage update it is slightly different than the rest in that I actually utilize WMI so I will run a CoInit and UnInit to prevent memory leaks \
I also update this far less frequently as it is not constantly changing like the CPU and RAM \
Now this is also where I show just how much easier it is to use psutil rather than WMI to grab free space and such \
I'm sure there might be a few issues with what if the drive has no letter and all that but again just trying things out \
Here that should not pose a huge issue though and I made sure to catch it just in case \
The clear line also looks a little messy but this was the formula I figured out through trial and error with the prints 

---

## V2 Direction

For V2 as I have said I want to implement a GUI, make it a lot neater and cleaner \
With V1 I have experimented a lot found a ton of new things I never knew that will 100% help me out \
I think I will try to find a library in order to complete the GPU information so we can actually have a live display \
And I will also do my best to optimize the program, as in less WMI calls only when needed and make the main live update calls through psutil \
I think I will continue the project in python, but there is a slight chance I may consider C++ depending on what advantages it may hold \
Over all I would consider this project a success as it did what I wanted it to, I learned many different ways to do things and different ways to utilize psutil and WMI \
Contact : oskaraszincenko500@gmail.com
<p align="center"><img style="border-radius: 50%;" width="200" height="134" alt="image" src="https://github.com/user-attachments/assets/4c13845f-de59-4698-873b-611cf3d6a326" /></p>

