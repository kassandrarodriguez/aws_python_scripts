# "metric_check.py"  
This script checks metrics over the period of 24 hours of all services in US East.  
The indiviual running the script would pass a percentage of memory usage.   
The script will ouput all services that uses the percentage passed in or higher.  
Therefore, if the indiviual running the script pass 200 as a parameter, the script will output all services that had used a percentage of 200 or more in Memory usage in the last 24 hrs.   
This output will be displayed in a pandas dataframe for easy readibility.


Run the following:  
**"python3 metric_check.py (PERCENTAGE HERE)"**  

Example:  
**"python3 metric_check.py 200"**
