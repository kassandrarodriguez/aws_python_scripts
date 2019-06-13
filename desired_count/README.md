# "desired_count_api.py"  
Is a script that has two functionalities. 

The first function is to check, through api, for desired vs running.  
If the desired count for a task is not the same as the running, it will output the clusters and the services that have this condition.  

To run:  
**"python3 desired_count_api.py desiredvsrunning"** 

The second function is to check if any service has a desired count of zero.  
This is possibly for anyone in DevOps that changed the desired amount of tasks to free up memory but forgot to make the changes back. Therefore, this script checks if desired == zero, except DECOMM.  

To run:  
**"python3 desired_count_api.py zero"** 
<br><br>
# "desired_count.py" 
Checks with arguments for desired vs running.  
With this script, a file with a list of clusters must be passed in as an argument. 
To run "desiredCount.py":  
You need to make a file with a list of clusters you will like to check  
You may name it, "listOfClusters.txt" 
<br><br>
Example of how the file should look like inside:  
cluster1  
cluster2  
cluster3
<br><br>
Then run:  
**"python3 desired_count.py listOfClusters.txt"**
