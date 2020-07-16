import boto3
import pprint
import re
import sys
sys.path.append("../")
import ecslib

cloudwatch = boto3.client('cloudwatch')
elb = boto3.client('elbv2')

def get_elbv2_load_balancers():
    marker = ''
    lb_response = []
    load_balancers = []
    while marker is not None:
        if marker == '':
            response = elb.describe_load_balancers()
        else:
            response = elb.describe_load_balancers(Marker = marker)
        lb_response += response['LoadBalancers']
        marker = response.get('NextMarker', None)
    for r in lb_response:
        load_balancers.append({'LoadBalancerArn': r['LoadBalancerArn']})
    return load_balancers

def main():      
    load_bals = get_elbv2_load_balancers()
    lb_response = []
    for lb in load_bals:
        marker = ''
        while marker is not None:
            if marker == '':
                response = response = elb.describe_listeners(LoadBalancerArn=lb['LoadBalancerArn']
                )
            else:
                response = elb.describe_listeners(LoadBalancerArn=lb['LoadBalancerArn'],
                    Marker = marker)
            try:
                lb_response.append({'TargetGroupArn': response['Listeners'][0]['DefaultActions'][0]['TargetGroupArn'], 'Listener': response['Listeners'][0]['ListenerArn'], 'Worked': 'First time'})
            except:
                lb_response.append({'TargetGroupArn': response['Listeners'][1]['DefaultActions'][0]['TargetGroupArn'], 'Listener': response['Listeners'][1]['ListenerArn'], 'Worked': 'secound time'})
            marker = response.get('NextMarker', None)

    for response in lb_response: 
        r = elb.describe_target_health(
        TargetGroupArn=response['TargetGroupArn'])
        if r['TargetHealthDescriptions'] == []:
            print(response['TargetGroupArn'])


main()
