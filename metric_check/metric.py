import boto3, pprint, re, sys, json, datetime
sys.path.append("../")
import ecslib

cloudwatch = boto3.client('cloudwatch')
client = boto3.client('ecs')


def main():

	try:
		percent = sys.argv[1]
		metric = sys.argv[2]
	except IndexError:
		pass
		print("Wrong parameters. Please insert parameters correctly")
		exit()
	metric_name = metric
					
	if metric_name == 'cpu':
		metric_name = 'CPUUtilization'
	else:
		metric_name = 'MemoryUtilization'
	results = []
	clusters = ecslib.get_all_clusters()
	services = ecslib.get_all_services_flushed(clusters)

	for s in services:
			# 86400 secs = 24 hours
			response = cloudwatch.get_metric_statistics(
					Period=300,
					StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=86400),
					EndTime=datetime.datetime.utcnow(),
					MetricName=metric_name,
					Namespace='AWS/ECS',
					Statistics=['Average'],
					Dimensions=[{'Name':'ClusterName', 'Value': s['Cluster']}, {'Name':'ServiceName', 'Value': s['Service']}])
			
			if response['Datapoints'] != []:
					average = response['Datapoints'][0]['Average'] 
					if average >= int(percent):
					# if average <= int(percent):
							if metric_name == 'CPUUtilization':
									results.append({'ECSCluster': s['Cluster'], "Service": s['Service'], "Average CPU Ultilization(Percent)": average})
									
							else:
									results.append({'ECSCluster': s['Cluster'], "Service": s['Service'], "Average Memory Ultilization(Percent)": average})

	print("Metrics for the last 24 hours, 5 min periods.\n")                            
	if metric_name == 'CPUUtilization':
			df = ecslib.pd.DataFrame(results,columns=['ECSCluster',  'Service',  'Average CPU Ultilization(Percent)']) 
			sorted_df = df.sort_values('Average CPU Ultilization(Percent)', ascending=False)
			print(sorted_df)
	else:
			df = ecslib.pd.DataFrame(results,columns=['ECSCluster',  'Service',  'Average Memory Ultilization(Percent)']) 
			sorted_df = df.sort_values('Average Memory Ultilization(Percent)', ascending=False)
			print(sorted_df)
main()