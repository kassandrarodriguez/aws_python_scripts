import boto3, pprint, re, sys, json
sys.path.append("../")
import ecslib
import pandas as pd
import xlsxwriter
from botocore.exceptions import ClientError
import time

client = boto3.client('ecs')

def make_version_dict(image_results):
    uniq_version_list = []
    all_versions_list = []
    new_dict = []
    for result in image_results:
        if 'WORKER1' in result['Service']:
            all_versions_list.append(result['Version'])
            new_dict.append(result)
            if result['Version'] not in uniq_version_list:
                uniq_version_list.append(result['Version'])
    return new_dict, all_versions_list, uniq_version_list

def get_versions_count(new_dict, version_dict):
    this_dict = []
    for version in version_dict:
        this_dict.append({ 'Version': version, 'Count': new_dict.count(version)})
    return this_dict

def make_excel(the_input):
    df = pd.DataFrame(the_input,columns=['ECSCluster', 'Service', 'TaskDefinition', 'Version'])
    writer = pd.ExcelWriter('images.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

def main():
    choice = None
    try:
        choice = sys.argv[1]
    except IndexError:
        pass
    clusters = ecslib.get_all_clusters()
    print("Getting Services...")
    services = ecslib.get_all_services(clusters)
    print("Getting Tasks defs...")

    done = False
    while not done:
        try:
            tasks_defs = ecslib.get_all_taskdef(services)
            done = True
        except ClientError as ex:
            print(ex)
            print("Will sleep for 3 mins and try again...")
            time.sleep(180)

    if choice == "count":
        print("Making Version dictionary...")
        full_dict, all_versions_list, uniq_version_list  = make_version_dict(tasks_defs)
        print("Counting Versions...")
        version_count = get_versions_count(all_versions_list, uniq_version_list)
        df = pd.DataFrame(version_count, columns=['Version', 'Count'])
        df_sorted = df.sort_values('Count', ascending=False)
        print(df_sorted)
        make_excel(full_dict)
    else:
        print("Making excel spreadsheet...")
        make_excel(tasks_defs)
    
main()