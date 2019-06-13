import boto3, pprint, re, sys

arg = sys.argv[1]
client = boto3.client('ecs')
file = open(arg, "r")
lines = file.readlines()


def main():
    listOfServices = []
    for line in lines:
        services = client.list_services(
        cluster =line.strip(),
        maxResults = 100
    )
        listOfServices = (services['serviceArns'])
        array =[listOfServices[i:i+10] for i in range(0, len(listOfServices), 10)]
        for i in array:
            counts = client.describe_services(
                cluster = line.strip(),
                services = i
                )
            # print(line.strip())
            for count in counts['services']:
                if 'kipu-logservers-pair' not in count['serviceName']:
                    if count['desiredCount'] != count['runningCount']:
                        
                        print(count['serviceName'], count['desiredCount'], count['runningCount'])
       
main()
