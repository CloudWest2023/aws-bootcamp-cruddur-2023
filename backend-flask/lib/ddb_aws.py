import boto3
import sys, os
from datetime import datetime, timedelta, timezone
import uuid

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..', '..'))
sys.path.append(parent_path)
from utils.bcolors import *


class ddbAWS:

    def client():
        printh("ddbAWS.client() ... creating connection to AWS server ...")
        
        aws_default_region = os.getenv("AWS_DEFAULT_REGION")
        dynamodbConnection = boto3.resource('dynamodb', region_name=aws_default_region)

        printh("    ... ddbAWS.client() created.")
        return dynamodbConnection
    

    def list_message_groups(ddbConn, current_user_uuid):

        printh("ddbAWS.list_message_groups() ...")

        curr_user_uuid = str(current_user_uuid)
        current_year = datetime.now().year
        table = ddbConn.Table('cruddur-messages')  # Ideally, we could prefix the table_name with `--stage` or `--prod` in more real dev process.

        response = table.query(
            KeyConditionExpression = {
                'user_uuid = :user_uuid',
            },
            ExpressionAttributeValues = {
                ':user_uuid': { 'S': curr_user_uuid }
            }
        )
        
        items = response['Items']

        printc(f"items:: {items}")

        results = []
        for item in items:
            last_sent_at = item['sk']['S']
            results.append({
                'uuid': item['message_group_uuid']['S'],
                'display_name': item['user_display_name']['S'],
                'handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': last_sent_at
            })

        printh("    ... ddbAWS.list_message_groups()")

        return results


    def list_messages(client, message_group_uuid):
        printh("ddbAWS.list_messages() ...")
        year = str(datetime.now().year)
        table_name = 'cruddur-messages'
        query_params = {
            'TableName': table_name,
            'KeyConditionExpression': 'pk = :pk',
            'ScanIndexForward': False,
            'Limit': 20,
            'ExpressionAttributeValues': {
                ':pk': { 'S': f"MSG#{message_group_uuid}" },
                'year': { 'S': year }
            }
        }

        response = client.query(**query_params)
        items = response['Items']
        
        results = []
        for item in items:
            created_at = item['sk']['S']
            results.append({
                'uuid': item['message_uuid']['S'],
                'display_name': item['user_display_name']['S'],
                'handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': created_at
            }
        )

        printh("    ... ddbAWS.list_messages()")

        return results


    # creates message_group and message
    def create_message_group(client, message,my_user_uuid, my_user_display_name, my_user_handle, other_user_uuid, other_user_display_name, other_user_handle):
        printh("ddbAWS.create_message_group() ...")
        
        table_name = 'cruddur-messages'
        
        message_group_uuid = str(uuid.uuid4())
        message_uuid = str(uuid.uuid4())
        now = datetime.now(timezone.utc).astimezone().isoformat()
        last_message_at = now
        created_at = now

        message_group = {
            'pk': {'S': f"GRP#{my_user_uuid}"},
            'sk': {'S': last_message_at},
            'message_group_uuid': {'S': message_group_uuid},
            'message': {'S': message},
            'user_uuid': {'S': other_user_uuid},
            'user_display_name': {'S': other_user_display_name},
            'user_handle':  {'S': other_user_handle}
        }

        message = {
            'pk':   {'S': f"MSG#{message_group_uuid}"},
            'sk':   {'S': created_at },
            'message': {'S': message},
            'message_uuid': {'S': message_uuid},
            'user_uuid': {'S': my_user_uuid},
            'user_display_name': {'S': my_user_display_name},
            'user_handle': {'S': my_user_handle}
        }

        items = {
        table_name: [
            {'Put': {'Item': message_group}},
            {'Put': {'Item': message}}
        ]
        }

        return {
            'message_group_uuid': message_group_uuid,
            'uuid': my_user_uuid,
            'display_name': my_user_display_name,
            'handle':  my_user_handle,
            'message': message,
            'created_at': created_at
        }

        try:
            # Begin the transaction
            with dynamodb_resource.meta.client.transact_write_items(RequestItems=items) as transaction:
                print('Transaction started.')
                # Commit the transaction
                response = transaction.commit()
                print('Transaction committed.')
                print(response)
        except ClientError as e:
            # Handle any errors
            print(e)

        printh("    ... ddbAWS.create_message_group()")


    def create_message(client,message_group_uuid, message, my_user_uuid, my_user_display_name, my_user_handle):
        printh("ddbAWS.create_message() ...")
        
        now = datetime.now(timezone.utc).astimezone().isoformat()
        created_at = now
        message_uuid = str(uuid.uuid4())

        record = {
            'pk':   {'S': f"MSG#{message_group_uuid}"},
            'sk':   {'S': created_at },
            'message': {'S': message},
            'message_uuid': {'S': message_uuid},
            'user_uuid': {'S': my_user_uuid},
            'user_display_name': {'S': my_user_display_name},
            'user_handle': {'S': my_user_handle}
        }
        # insert the record into the table
        table_name = 'cruddur-messages'
        response = client.put_item(
            TableName=table_name,
            Item=record
        )
        # print the response
        print(response)
        return {
            'message_group_uuid': message_group_uuid,
            'uuid': my_user_uuid,
            'display_name': my_user_display_name,
            'handle':  my_user_handle,
            'message': message,
            'created_at': created_at
        }

        printh("    ... ddbAWS.create_message()")