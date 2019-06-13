# "task_def.py"  
Is a script that has two funtionalites.

One function is to monitor non-standard Task Definitions. Populates dictionaries of non-standard Task Definitions. 
whats considered a non-standard task definition can easily be changed if the infracture were to change.
Right now its set up to check if a certain amout of memory is being used per service. If its more than the norm, it would be considered non-standard.

To run:  
**"python3 task_def.py memory"**  

The second function is to ouput the different image versions of all task def and give a count for each.  
Example:  
Version3 100  
Version15 2000  
Version1 15  

Another function of this script is to check if the task defintions is the same as service.   
To run:  
**"python3 task_def.py task"**  

If the wrong arguments are passed, script will output the following:  
**"Invalid Argument. Valid arguments: 'memory' or 'task' "**
