#!/usr/bin/env python3
import boto3, pprint, re, sys, json
sys.path.append("../")
import ecslib

choice = sys.argv[1]
client = boto3.client('ecs')

def describe_task_def_mem(results, selection):
    task_diff_results = []
    for re in results:
        try:
            response = client.describe_task_definition(taskDefinition= re['TaskDefinition'])
            mem = response['taskDefinition']['containerDefinitions'][0]['memoryReservation']
            cpu = response['taskDefinition']['containerDefinitions'][0]['cpu']
        except KeyError:
            pass
        else:
            re['SoftMemory'] = mem
            re['CPU'] = cpu
            if selection == 'memory':
                if 'WORKER' in re['TaskDefinition']:
                    if mem != 750:
                        task_diff_results.append(re)
                elif 'WEB' in re['TaskDefinition']:
                    if mem > 1024:
                        task_diff_results.append(re)
            else:
                if cpu != 100:
                     task_diff_results.append(re)

    return(task_diff_results)

def describe_container_type(results):
    container_diff = []
    for re in results:
        response = client.describe_task_definition(taskDefinition= re['TaskDefinition'])
        container_type = response['taskDefinition']['containerDefinitions'][0]['environment'][0]['value']
        if container_type != 'server' and container_type != 'worker1cron' and container_type != 'worker2':
            re['Container_Type'] = container_type
            container_diff.append(re)
             
    return container_diff

def check_task_def(results):
    problem_list = []
    for result in results:
        if result['Service'] not in result['TaskDefinition']:
            problem_list.append(result)
    if problem_list != []:
        pprint.pprint(problem_list)
    else:
        print("Everything is as should")

def main():

    if choice == 'memory' or choice == 'task' or choice == 'type' or choice == 'cpu':
        clusters = ecslib.get_all_clusters()
        services = ecslib.get_all_services(clusters)
        tasks_defs = ecslib.get_all_taskdef(services)
     
        if choice == 'memory' or choice == 'cpu':
            task_diff_results = describe_task_def_mem(tasks_defs, choice)
            df = ecslib.pd.DataFrame(task_diff_results, columns=['ECSCluster', 'Service', 'TaskDefinition', 'CPU', 'SoftMemory'])
            print(df)
        elif choice == 'type':
            container_types = describe_container_type(tasks_defs)
            df = ecslib.pd.DataFrame(container_types, columns=['ECSCluster', 'Service', 'TaskDefinition', 'Container_Type'])
            print(df)
        else:
            check_task_def(tasks_defs)
    else:
        print("Invalid Argument. Valid arguments: 'memory' or 'task' or 'type'")
                
main()

