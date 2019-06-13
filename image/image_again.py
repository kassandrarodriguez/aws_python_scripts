import boto3, pprint, re, sys, json, codecs
sys.path.append("../")
import ecslib
import pandas as pd
import xlsxwriter
from botocore.exceptions import ClientError
import time


client = boto3.client('ecs')

a_list = sys.argv[1]
list_of_services = []
with codecs.open(a_list, "r",encoding='utf-8', errors='ignore') as f:
        for line in f:
            variable = line.strip() + '-WORKER1'
            list_of_services.append({'Service': variable})

clusters = ecslib.get_all_clusters()
services = ecslib.get_all_services_flushed(clusters)


for s in services:
    for a in list_of_services:
        if a['Service'] in s['Service']:
           a['Cluster'] =  s['Cluster']

           r = client.describe_services(
                cluster= a['Cluster'],
                services=[a['Service']]
            )


           taskd = r['services'][0]['taskDefinition']
           n= re.search(r'definition/(.*)', taskd)
           task_def_name = n[1]
           response = client.describe_task_definition(taskDefinition= task_def_name)
           entire_image = response['taskDefinition']['containerDefinitions'][0]['image']
           n = re.search(r'amazonaws.com/(.*)', entire_image)
           version = n[1]
           a['TaskDefinition'] = task_def_name
           a['Version'] = version

df = pd.DataFrame(list_of_services, columns=['Cluster', 'Service', 'Version'])
print(df)