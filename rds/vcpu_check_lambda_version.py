import boto3
import datetime
import json
from botocore.exceptions import ClientError
from botocore.vendored import requests

ses = boto3.client('ses', region_name='us-east-1')
pricing = boto3.client('pricing')

def get_all_rds_instances(rds):
    marker = ''
    rds_response = []
    rds_dict = []
    while marker is not None:
        if marker == '':
            response = rds.describe_db_instances()
        else:
            response = rds.describe_db_instances(Marker = marker)
        rds_response += response['DBInstances']
        marker = response.get('Marker', None)
    for r in rds_response:
        rds_dict.append({'DBInstanceIdentifier': r['DBInstanceIdentifier'], 
        'DBInstanceClass': r['DBInstanceClass'], 'DBInstanceStatus': r['DBInstanceStatus'], 'DbiResourceId': r['DbiResourceId']})
    return rds_dict


def make_dbinstance_class_array(list_dict):
    instance_classes = dict()
    for a_dict in list_dict:
        if a_dict['DBInstanceClass'] not in instance_classes:
            instance_classes[a_dict['DBInstanceClass']] = 0
    return instance_classes


def get_vpc(array):
    for key, value in array.items():
        response = pricing.get_products(
            ServiceCode='AmazonRDS',
            Filters=[
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'instanceType',
                    'Value': key
                },
            ],

        )
        price_list = response['PriceList'][0]
        json_price_list = json.loads(price_list)
        array[key] = json_price_list['product']['attributes']['vcpu']


def put_vpc_in_rds_list(rds_dict, instances_classes):
    for a_dict in rds_dict:
        a_dict['vcpu'] = instances_classes.get(a_dict['DBInstanceClass'])


def get_max_value(a_list, pi):
    for a_dict in a_list:
        values = []
        max_value = 0
        result = []
        try:
            response = pi.get_resource_metrics(
                ServiceType='RDS',
                Identifier=a_dict['DbiResourceId'],
                MetricQueries=[
                    {
                        'Metric': 'db.load.avg',
                        'GroupBy': {
                            'Group': 'db.wait_event',
                            'Dimensions': [
                                'db.wait_event.name',
                            ],
                            'Limit': 10
                        },
                    },
                ],
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
                EndTime=datetime.datetime.utcnow(),
                PeriodInSeconds=60,
                MaxResults=20,)
        except ClientError:
            a_dict['MaxValue'] = 'PI is not enable'
            continue
        if len(response['MetricList']) > 1:
            for value in response['MetricList'][1]['DataPoints']:
                try:
                    values.append(value['Value'])
                except KeyError:
                    pass
            result = max(values)
            if result > max_value:
                max_value = result
        a_dict['MaxValue'] = round(max_value, 2)

def check_value_vs_vpc(rds_list):
    results = []
    for a_dict in rds_list:
        if a_dict['MaxValue'] != 'PI is not enable':
            if float(a_dict['MaxValue']) >= float(a_dict['vcpu']):
                results.append(a_dict)
    return results


def send_email(email_msg, email_subject):
    email_to = '{TO EMAIL GOE HERE}'
    email_source = '{SOURCE EMAIL GOES HERE}'
    email_source_arn = '{ARN GOES HERE}'
    ses.send_email(
    Destination={
        'ToAddresses': [email_to],
    },
    Message={
        'Body': {
            'Html': {
                'Charset': 'UTF-8',
                'Data': email_msg,
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': email_subject,
        },
    },
    Source=email_source,
    SourceArn=email_source_arn
    )
    print(f"\nInfo email sent to {email_to}!")


def relay_message(results):
    if results:
        email_subject = "AWS Lambda Info: check_current_activity_bar_rds_check"
        email_msg = "<html><h2>The following Databases have gone over the 'vCPU Given' in the past 20 minutes<h2>"
        email_msg += '<table border="1"cellpadding="10"><tr><th>DBInstanceIdentifier</th><th>DBInstanceClass</th><th>vcpu</th><th>MaxValue</th>'
        for r in results:
            email_msg += '<tr>'
            email_msg += '<td>'
            email_msg += str(r['DBInstanceIdentifier'])
            email_msg += '</td>'
            email_msg += '<td>'
            email_msg += str(r['DBInstanceClass'])
            email_msg += '</td>'
            email_msg += '<td>'
            email_msg += str(r['vcpu'])
            email_msg += '</td>'
            email_msg += '<td>'
            email_msg += str(r['MaxValue'])
            email_msg += '</td>'
            email_msg += '</tr>'
        email_msg += '</table></html>'
        send_email(email_msg, email_subject)


def lambda_handler(event, context):
    regions = ['us-east-1', 'ca-central-1', 'eu-west-2']
    for region in regions:
        rds = boto3.client('rds', region_name=region)
        pi = boto3.client('pi', region_name=region)
        rds_dict = get_all_rds_instances(rds)
        instance_classes = make_dbinstance_class_array(rds_dict)
        get_vpc(instance_classes)
        put_vpc_in_rds_list(rds_dict, instance_classes)
        get_max_value(rds_dict, pi)
        results = check_value_vs_vpc(rds_dict)
        relay_message(results)
        print("Region " + region + " is completed")



lambda_handler('test', 'test')
