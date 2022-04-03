# Ricart-Agrawala-algorithm-DS

The Team contains **Elvin Mirzazada** and **Gular Samadova**

I used ps1(powershell) script instead of the shell script, because I use windows.

Starting the program: 

- **main.ps1 N** on the command prompt in windows
- **main.sh N** on the terminal in linux/ubuntu


The project has following functionality:

**list**: This command lists all the nodes and its states. For instance,
$ List
P1, DO-NOT-WANT
P2, DO-NOT-WANT
P3, DO-NOT-WANT
P4, DO-NOT-WANT
P5, DO-NOT-WANT
P6, DO-NOT-WANT
After t seconds, list command again
$ List
P1, HELD
P2, DO-NOT-WANT
P3, WANTED
P4, DO-NOT-WANT
P5, WANTED
P6, DO-NOT-WANT


**time-cs t**
This command sets the time to the critical section. It assigns a time-out for possessing the critical section
and the time-out is selected randomly from the interval (10, t). By default, each process can have the
critical section for 10 second. For instance, $ time-cs 20, sets the interval for time-out as [10, 20] – in
seconds.

**time-p t**
This command sets the time-out interval for all processes [5, t], meaning that each process takes its timeout randomly from the interval. This time is used by each process to move between states. For instance,
a process changes from DO-NOT-WANT to WANTED after a time-out, e.g., after 5 seconds. Notice here
that the process cannot go back to DO-NOT-WANT, and can only proceed to HELD once is authorized by 
