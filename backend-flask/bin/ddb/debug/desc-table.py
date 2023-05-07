import boto3
import os, sys

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..', '..'))
sys.path.append(parent_path)
from utils.bcolors import *

printh("desc-table ...")

aws_default_region = os.getenv('AWS_DEFAULT_REGION')
ddbConn = boto3.resource('dynamodb', region_name=aws_default_region)
printh(f"        Connected to AWS DynamoDB: {ddbConn}")

response = ddbConn.describe_table(
    TableName='cruddur-messages'
)