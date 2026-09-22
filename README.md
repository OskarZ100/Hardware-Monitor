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
After running the program you should get a prompt displaying the functions of the program 
<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/45932c73-a777-420a-9bea-fdcf454efd20" />
The only inputs the program will accept are
```
0,1,2,3,4,5,6, or 7
```
If you enter a non valid input the program will display, and prompt the menu again  
```
Input is a plain number no spaces try again and select a valid input
```
As shown, 
<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/d0430c1b-7466-43a3-9bef-ae26ca614e95" />
### (0) - Info About Project command
Displays basic like info about me and the project nothing fancy at all
### (1) - General Hardware Info 
Displays static general info about every component featured 
These are values grabbed at the exact time the function is called 
Updated live values only show up in the specific functions of each hardware component
<img width="682" height="657" alt="image" src="https://github.com/user-attachments/assets/78b96b7d-6022-4df2-a7db-3ff8b068e1fc" />
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
<img width="250" height="250" alt="cpuinfo" src="https://github.com/user-attachments/assets/05749a91-6c81-4e1d-8786-56ae830d9924" />
<br>
### (3) - GPU information 
This command will display information about any GPUs on the system <br>
This only contains basic static data <br>
The reason for this I go more into depth on in the documentation section but it boils down to the way windows calculates this <br>
<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/48356089-0a6c-499e-9f0a-443f5d908288" />
<br>
### (4) - RAM information 
This will show you RAM information, follows same sort of blueprint like the CPU command <br>
shows static data on top with general live information in the live section <br>
I decided to just show the total usage with the live data as it is much neater in my opinion <br>
<img width="250" height="250" alt="raminfo" src="https://github.com/user-attachments/assets/8a8ac297-5931-4297-b69a-c3ba79bb129b" />
<br>
### (5) - Storage information
Shows as you guessed, basic storage information with a live display that utilizes psutil <br>
In this project I found many ways to display free space, I had such such such an easier time using psutil <br>
WMI process for free space was one of the harder and annoying things to implement while psutil took me like 5 min <br>
<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/ab7e3ac7-68e6-415a-b96b-e3b486d74dc4" />
<br>
### (6) - Clear console
Very straight forward command, just clear the console incase you somehow misinputed a ton of stuff <br>
<img width="250" height="250" alt="clearscreen" src="https://github.com/user-attachments/assets/eadbb9e8-31e8-469f-90c1-1ad63e0b826d" />
<br>
### (7) - End session
Again pretty self explanatory, ends process ez <br>
<img width="250" height="250" alt="end" src="https://github.com/user-attachments/assets/343c7236-bfe1-448b-a945-94145bc69d4c" />
<br>

## Documentation
## V2 Direction
