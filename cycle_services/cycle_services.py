import boto3
import pprint
import sys
sys.path.append("../")
import ecslib
import re

file_input = sys.argv[1]
services = []
session = boto3.session.Session(region_name='us-east-1')

client = session.client('ecs')

with open(file_input, "r") as services_list:
    inputted_services = services_list.read().splitlines()

all_clusters = ecslib.get_all_clusters()

for cluster in all_clusters:
    token = ''
    while token is not None:
        if token == '':
            response = client.list_services(cluster=cluster, maxResults=100)
        else:
            response = client.list_services(cluster=cluster, maxResults=100, nextToken=token)
            
        for service in response['serviceArns']:
            for element in inputted_services:
                if element in service:
                    m = re.search(r'cluster/(.*)', cluster)
                    cluster_name = m[1]
                    n = re.search(r'service/(.*)', service)
                    service_name = n[1]
                    services.append({"cluster": cluster_name, "service": service_name})
        token = response.get('nextToken', None)

for service in services:
    response = client.update_service(
        cluster = service['cluster'],
        service= service['service'],
        forceNewDeployment=True,
    )
    print("Cycled: " + service['service'])
    print('On Cluster: ' + service['cluster'])