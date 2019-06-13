#!/usr/bin/env python3
import boto3, re, sys

client = boto3.client('autoscaling')
ec2_client = boto3.client('ec2')

def get_instance_list():
    token = ''
    instance_list = []
    while token is not None:
        if token == '':
            response = ec2_client.describe_instances(MaxResults=123)
            reservation  = response['Reservations']
            for r in reservation:
                for e in r['Instances']:
                    instance_list.append(e['InstanceId'])
        else:
            response = ec2_client.describe_instances(NextToken=token)
            reservation  = response['Reservations']
            for r in reservation:
                for e in r['Instances']:
                    instance_list.append(e['InstanceId'])
        token = response.get('NextToken', None)
    return(instance_list)

def remove(duplicate):
    new_list = []
    for instance in duplicate:
        if instance not in new_list:
            new_list.append(instance)
    return new_list
        
def main():
    the_list = get_instance_list()
    len_of_list = len(the_list)
    end_count = 50
    beginning_count = 0
    temp_dict= []
    my_list = []

    while end_count < len_of_list + 50:
        id_list = the_list[beginning_count:end_count]
        response = client.describe_auto_scaling_instances(InstanceIds=id_list,)
        temp_dict.append(response)
        beginning_count = end_count
        end_count += 50
    
    for element in temp_dict:
        for e in element['AutoScalingInstances']:
            if e['ProtectedFromScaleIn'] == True:
                my_list.append(e['AutoScalingGroupName'])

    if my_list == []:
        print("No scale-in protection on any auto-scaling group")
    else:
        new_list= remove(my_list)
        print("The following Clusters have scale in-protection:")

        for element in new_list:
            print(element)
    
main()

