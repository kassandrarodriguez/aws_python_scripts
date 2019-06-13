import boto3, pprint, re, sys, json
sys.path.append("../")
import ecslib
from botocore.exceptions import ClientError

class colors: 
    warning='\033[31m'
    success='\033[32m'
    good='\033[94m'

client = boto3.client('s3')
array_of_buckets = []
list_of_buckets = sys.argv[1]

def main():

    #extracting from file the bucket names
    my_file = open(list_of_buckets, "r")
    lines = my_file.readlines()
    for line in lines:
        array_of_buckets.append(line.strip())

    # Looping through all buckets that was given in file
    for bucket in array_of_buckets:
        name_tag= 0
        #Checking to see if bucket has NAME Tag, if no error has occur. It is bc tags exist already
        try:
            response = client.get_bucket_tagging(
                Bucket=bucket
            )
            for x in response['TagSet']:
                if x['Key'] == 'NAME':
                    name_tag = 1
            if name_tag != 1:
                print(colors.success + bucket + " already has tags but does not have NAME tag, adding NAME tag....")
                a_list = response['TagSet']
                a_list.append( {
                            'Key': 'NAME',
                            'Value': bucket
                        })
                another_response = client.put_bucket_tagging(
                Bucket=bucket,
                Tagging={
                    'TagSet': a_list
                }
            )
            else:
                print(colors.good + bucket + " already has NAME TAG....")
        #If an exception occurs, its either because bucket has no tags or the bucket does not exist
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchTagSet':
                print(colors.success + bucket + " has no tags, adding NAME tags....")
                r = client.put_bucket_tagging(
                Bucket=bucket,
                Tagging={
                    'TagSet': [
                        {
                            'Key': 'NAME',
                            'Value': bucket
                        },
                    ]
                })
            elif e.response['Error']['Code'] == 'NoSuchBucket':
                print(colors.warning + bucket + " does not exist in this account.....")
            pass

main()