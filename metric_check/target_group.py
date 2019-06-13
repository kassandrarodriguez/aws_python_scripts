import boto3, pprint, re, sys, json, datetime
sys.path.append("../")
import ecslib

cloudwatch = boto3.client('cloudwatch')
client = boto3.client('ecs')

def main():

    my_dict = []
    metric_stat = []
    requests =[]
    token = ''
    while token is not None:
        if token == '':
            response = cloudwatch.list_metrics(
                Namespace='AWS/ApplicationELB',
                MetricName='RequestCountPerTarget',
            
            )
        else:
            response = cloudwatch.list_metrics(
                Namespace='AWS/ApplicationELB',
                MetricName='RequestCountPerTarget',
                nextToken=token
            
            )
        my_dict.append(response['Metrics'])
        token = response.get('nextToken', None)
    
    for element in my_dict[0]:
        response = cloudwatch.get_metric_statistics(
            # period = 1 min, checking in the 3 hours
                Period=60,
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=10800),
                EndTime=datetime.datetime.utcnow(),
                MetricName='RequestCountPerTarget',
                Namespace='AWS/ApplicationELB',
                Statistics=['Sum'],
                Dimensions=[{'Name':'TargetGroup', 'Value':element['Dimensions'][0]['Value']}])
        for r in response['Datapoints']:
            requests.append(r['Sum'])
        try:
            max_number =  max(requests)
        except ValueError:
            max_number = 0
            pass
        if max_number > 100:
            target_name = element['Dimensions'][0]['Value']
            metric_stat.append({'Max Requests': max_number, 'Target Group': target_name[12:22]})
            
        requests =[]
    df = ecslib.pd.DataFrame(metric_stat,columns=['Target Group',  'Max Requests']) 
    sorted_df = df.sort_values('Max Requests', ascending=False)
    print("RequestCountPerTarget: Max Requests over 100 in the last 3 hours\n")
    print(sorted_df)

main()