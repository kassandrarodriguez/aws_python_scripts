#!/usr/bin/env python3
import boto3
import pprint
import re
import sys
sys.path.append("../")
import ecslib

test = sys.argv[1]
client = boto3.client('ecs')

def print_the_results(results):
  for r in results:
        print(r['cluster'])
        print(r['service'])
        desired = str(r['desiredCount'])
        running = str(r['runningCount'])
        print(f"Desired Count: {desired}")
        print(f"Running Count: {running}")
        print(" ")

def main():
    
    if test == "desiredvsrunning" or test == "zero":
        clusters = ecslib.get_all_clusters()
        results = []   

        print ("We found {count} clusters in this account\n".format(count=len(clusters)))
        services = ecslib.get_all_services(clusters)
        
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
                n = re.search(r'service/(.*)', service)
                service_name = n[1]
                desiredCount = r['services'][0]['desiredCount']
                runningCount = r['services'][0]['runningCount']
                if test == "desiredvsrunning":
                    if desiredCount != runningCount:
                        results.append({'cluster': cluster_name, "service": service_name, "desiredCount": desiredCount, "runningCount": runningCount})
                if test == "zero":
                    if 'DECOM' not in cluster_name:
                        if desiredCount == 0:
                            results.append({'cluster': cluster_name, "service": service_name, "desiredCount": desiredCount, "runningCount": runningCount})
    
        print_the_results(results)
    else:
        print('Invalid Argument. Valid arguments: "desiredvsrunning" or "zero"')

main()
