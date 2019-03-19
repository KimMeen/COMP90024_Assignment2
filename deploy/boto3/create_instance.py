#!/usr/bin/env python3.5
import boto3
import boto3config as config
import time
def connect_to_ec2():
    """
    Connect to EC2
    """
    ec2 = boto3.client(
    'ec2',
    aws_access_key_id=config.ACCESS_KEY,
    aws_secret_access_key=config.SECRET_KEY,
    region_name=config.DEFAULT_REGION,
    endpoint_url=config.EC2_ENDPOINT_URL,
    )

    return ec2

def get_images(ec2):
    """
    Get images' id
    """
    for image in ec2.describe_images(Filters=[
    {'Name': 'is-public', 'Values': ["True"]},
    {'Name': 'architecture', 'Values': ["x86_64"]},
    ])['Images']:
        print("Image Name:", image['Name'], "Image ID:", image['ImageId'])

def get_regions_zones(ec2):
    """
    Retrieves all regions/endpoints that work with EC2
    and Retrieves availability zones only for region of the ec2 object
    """
    response_regions= ec2.describe_regions()
    response_zones = ec2.describe_availability_zones()
    print('Regions:', response_regions['Regions'])
    print('Availability Zones:', response_zones['AvailabilityZones'])

def create_single_instance(ec2):
    instance = ec2.run_instances(
    ImageId=config.IMAGE_ID,
    InstanceType=config.INSTANCE_TYPE,
    Placement={
    'AvailabilityZone': config.PLACEMENT,
    },
    SecurityGroups=config.SECURITY_GROUPS,
    KeyName=config.KEY_NAME,
    MaxCount=1,
    MinCount=1,
    )
    return instance

def print_instance_info(ec2,instance):
    instance_id = instance['Instances'][0]['InstanceId']
    all_instances = ec2.describe_instances(
    InstanceIds=[
        instance_id,
    ],
    )

    print("-------- Instance Info --------")
    print("InstanceId:", all_instances['Reservations'][0]['Instances'][0]['InstanceId'])
    print("Private IP:", all_instances['Reservations'][0]['Instances'][0]['PrivateIpAddress'])
    print("Zone:", all_instances['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone'])
    print("Key Name:", all_instances['Reservations'][0]['Instances'][0]['KeyName'])

    print("------------- End -------------")

def main():
    ec2 = connect_to_ec2()
    print("Connected to Nectar")

    instance = create_single_instance(ec2)
    print("Created one instance")

    #wait until IP has been settled
    time.sleep(config.WAITING_TIME)
    print_instance_info(ec2, instance)

    # print(info)
    # get_images(ec2)
    # get_regions_zones(ec2)


if __name__ == "__main__":
    main()
