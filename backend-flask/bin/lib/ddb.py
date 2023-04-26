import boto3
import os, sys
import uuid
from datetime import datetime, timedelta, timezone

class DDB:
	def client():
		endpoint_url = os.getenv("AWS_ENDPOINT_URL")
		if endpoint_url:
			attrs = { 'endpoint_url': endpoint_url }
		else: 
			attrs = {}
		dynamodb = boto3.client('dynamodb', **attrs)
		return dynamodb


	def list_message_groups(client, current_user_uuid):
		table_name = 'cruddur-messages' # Ideally, we could prefix the table_name with `--stage` or `--prod` in more real dev process.
		query_params = {
			'TableName': table_name,
			'KeyConditionExpression': 'pk = :pk',
			'ScanIndexForward': False,
			'Limit': 20,
			'ExpressionAttributeValues': { 
				':pk': { 'S': f'GRP#{current_user_uuid}' }
			}
		}		
		print('query-params----------------------------')
		print(query_params)
		print('client----------------------------------')
		print(client)

		results = []
		for item in items:
			last_sent_at = item['sk']['S']
			results.append({
				'uuid': item['mesasge_group_uuid']['S'],
				'display_name': item['user_display_name']['S'],
				'handle': item['user_handle']['S'],
				'message': item['message']['S'],
				'created_at': last_sent_at				
			})
		return results