import boto3
import os
from botocore.vendored import requests


url = 'http://www.deanza.edu/schedule/listings.html?dept=CIS&t=S2019'
sns_client = boto3.client('sns')


def notify(msg):
    sns_client.publish(
        PhoneNumber=os.environ['PHONE_NUMBER'],
        Message=msg
    )


def check_url(url):
    url_file = requests.get(url)
    url_file = url_file.text.splitlines()
    check_class_status(url_file, '42519', 'Data Abstraction and Structures')
    check_class_status(
            url_file, '46057',
            'Introduction to x86 Processor Assembly Language and Computer '
            + 'Architecture')


def check_class_status(url_file, class_number, class_name):
    full_class_msg = f'{class_name} is full'
    opened_class_msg = f'{class_name} has opened up'
    sign_up_msg = f'Sign up now for {class_name}'

    for line in url_file:
        if f'{class_number}' in line:
            items = line.split()
            for item in items:
                if 'Open' in item:
                    print(opened_class_msg)
                    notify(opened_class_msg)
                elif 'WL' in item:
                    print(sign_up_msg)
                    notify(sign_up_msg)
                elif 'Full' in item:
                    print(full_class_msg)
            #        notify(full_class_msg)


def lambda_handler(event, context):
    check_url(url)

