# "scale_in.py"  
Is a script that checks all clusters if they have scale-in protection. Outputs all the clusters that does. 
This is script was made because very often clusters get their hosts replaced and sometimes a devOps member would leave the scale-in protection left on the EC2 instances. This is could be dangerous. So this is the reason the script was made. 

To run:  
**"python3 scale_in.py"**  

Example of output:  
The following Clusters have scale in-protection:  
Cluster1  
Cluster2  


If no cluster have scale-in protection left on. The following message will appear:  
**No scale-in proctection on any auto-scaling group**
