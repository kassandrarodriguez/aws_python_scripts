# "s3_tags.py.py"  
 Goes through a list of bucket names in S3 and tags them with "KAST_NAME" and the value.    
 If "KAST_NAME" tag already exists, it will skip it.  
 
 
Make a file with the list of buckets you want to tag: 

Example:  
40404  
56790  
89030  
12919  
<br><br>
Run the following:  
**"python3 s3_tags.py (FILENAME HERE)"**  

