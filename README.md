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

#### Hardware (Main class)

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

This is to handle everything CPU
Helps with the in depth function in main and the general one
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

The dictionary setup is pretty basic I just setup all the keys I want
Then I loop through all the objects in information and store accordingly
Super simple

#### GPU subclass of hardware

Handles everything GPU!
Pretty much the exact same setup as CPU class
Just slight changes in the general info function obviously and with the dictionary setup there is one difference here

```
 if int(item.MaxRefreshRate) == 0:
   return_dict["RefreshRate"].append(str(item.MaxRefreshRate)+" GPU is not the display driving adaptor ATM")
 else:
   return_dict["RefreshRate"].append(str(item.MaxRefreshRate))
```

Ok as you can see this is a little different
I learned while doing the project that if you have more than one GPU there will be one display driving adaptor
In my case on laptop I have a dedicated GPU and internal GPU which ever is the display driving adaptor
So if it shows a 0 my program will assume and tell you which is the adaptor and not
Now if your GPU is just lets say completely cooked, it will not be the display driving adaptor so obviously will show that-
and status will let you know how it is doing, for anyone like well what if the GPU just blew up there u go

#### RAM subclass of hardware

Again handles everything RAM
Now this is the same exact setup as the CPU and GPU 
But there is a specific function it has which is getting its Capacity specifically in GB
WMI likes to give everything in bytes which is a pain so this handles getting Capacity and storing in an array
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

Super simple the reason I keep this in an array and don't think it needs updates is because-
I do not think the user will be switching out or downloading more RAM while program is running :)

#### Storage and LD2P classes 

This was probably the harder part of the project because I made it much harder than it needed to be by using WMI and not psutil
So psutil actually has a function you can use to get free space and I use it in main.py

```
my_storage.to_gb(psutil.disk_usage(psutilcombo).free)
```

As you can see you just pass in a logical drive, but it has to have a drive letter is the thing

Now for the storage class I decided to make a whole new class not a subclass of Hardware because it just didnt make sense to me 
There are so many different things between the two and Storage objects in WMI act very differently than the rest
It has a physical drive, logical disk, and partitions and all these get kind of messy when trying to figure certain things out
So I was just like lets make this easier to navigate and write than forcing compatibility 


## V2 Direction
