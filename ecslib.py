import boto3, re
import pandas as pd
client = boto3.client('ecs')

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.width', None)


def get_all_clusters():
    token = ''
    clusterList = []
    while token is not None:
        if token == '':
            response = client.list_clusters(
            maxResults = 100
            )
        else:
            response = client.list_clusters(
            nextToken = token
            )
        clusterList += response['clusterArns']
        token = response.get('nextToken', None)
    return clusterList

def get_all_services(clusters):
    services = []
    for c in clusters:
        token = ''
        while token is not None:
            if token == '':
                response = client.list_services(cluster=c, maxResults=100)
            else:
                response = client.list_services(cluster=c, maxResults=100, nextToken=token)
            for s in response['serviceArns']:
                services.append({"cluster": c, "service": s})
            token = response.get('nextToken', None)
    return services


def get_all_services_flushed(clusters):
    services = []
    for c in clusters:
        token = ''
        while token is not None:
            if token == '':
                response = client.list_services(cluster=c, maxResults=100)
            else:
                response = client.list_services(cluster=c, maxResults=100, nextToken=token)
            for s in response['serviceArns']:
                m = re.search(r'cluster/(.*)', c)
                cluster_name = m[1]
                n = re.search(r'service/(.*)', s)
                service_name = n[1]
                services.append({"Cluster": cluster_name, "Service": service_name})
            token = response.get('nextToken', None)
    return services

def get_all_taskdef(services):
    tasks_defs = []  
    for s in services:
        service = s['service']
        cluster = s['cluster']
    
        if 'kipu-logservers-pair' not in service:
            r = client.describe_services(
                cluster=cluster,
                services=[service]
            )
            m = re.search(r'cluster/(.*)', cluster)
            cluster_name = m[1]
            taskd = r['services'][0]['taskDefinition']
            n= re.search(r'definition/(.*)', taskd)
            task_def_name = n[1]
            o = re.search(r'service/(.*)', service)
            service_name = o[1]
            response = client.describe_task_definition(taskDefinition= task_def_name)
            entire_image = response['taskDefinition']['containerDefinitions'][0]['image']
            n = re.search(r'amazonaws.com/(.*)', entire_image)
            version = n[1]
            tasks_defs.append({'ECSCluster': cluster_name, "Service": service_name, "TaskDefinition": task_def_name, "Version": version})  
    return tasks_defs