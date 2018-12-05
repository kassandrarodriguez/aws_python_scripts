#!/usr/bin/env python3
import boto3, pprint, re, sys

test = sys.argv[1]
client = boto3.client('ecs')

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
    
def print_the_results(results):
  for r in results:
        print(r['cluster'])
        print(r['service'])
        print("Desired Count: " + str(r['desiredCount']))
        print("Running Count: " + str(r['runningCount']))
        print(" ")

def main():
    
    if test == "desiredvsrunning" or test == "zero":
        clusters = get_all_clusters()
        results = []   

        print ("We found {count} clusters in this account\n".format(count=len(clusters)))
        services = get_all_services(clusters)
        
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
                # print("Getting data for cluster:" + cluster_name)
                desiredCount = r['services'][0]['desiredCount']
                runningCount = r['services'][0]['runningCount']
                if test == "desiredvsrunning":
                    if desiredCount != runningCount:
                        results.append({'cluster': cluster_name, "service": service, "desiredCount": desiredCount, "runningCount": runningCount})
                if test == "zero":
                        if desiredCount == 0:
                            results.append({'cluster': cluster_name, "service": service, "desiredCount": desiredCount, "runningCount": runningCount})
    
        print_the_results(results)

    else:
        print('Invalid Argument. Valid arguments: "desiredvsrunning" or "zero"')
           
main()
