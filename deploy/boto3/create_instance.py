#!/usr/bin/env python3.5
import boto3
import boto3config as config
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

def create_instances(ec2):
    instance = ec2.run_instances(
    ImageId=config.IMAGE_ID,
    InstanceType=config.INSTANCE_TYPE,
    Placement={
    'AvailabilityZone': config.PLACEMENT,
    },
    SecurityGroups=config.SECURITY_GROUPS,
    KeyName=config.KEY_NAME,
    MaxCount=config.MAX_COUNT,
    MinCount=config.MIN_COUNT,
    )
    return instance
def main():
    ec2 = connect_to_ec2()
    print("Connected to Nectar")
    instance = create_instances(ec2)
    print("Created instance")
    info = ec2.describe_instances()
    print(info)
    # get_images(ec2)
    # get_regions_zones(ec2)


if __name__ == "__main__":
    main()
