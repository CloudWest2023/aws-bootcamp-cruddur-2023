import uuid
from datetime import datetime, timedelta, timezone

from lib.db import db
from lib.ddb import ddb

# In this file, we have to get all the users in the conversation.
class CreateMessage:
  def run(mode, message, cognito_user_id, message_group_uuid=None, user_receiver_handle=None):
    model = {
      'errors': None,
      'data': None
    }
    
    if (mode == "update"):
      if message_group_uuid == None or len(message_group_uuid) < 1:
        model['errors'] = ['message_group_uuid_blank']

    if cognito_user_id == None or len(cognito_user_id) < 1:
      model['errors'] = ['cognito_user_id_blank']

    if (mode == "create"):
      if user_receiver_handle == None or len(user_receiver_handle) < 1:
        model['errors'] = ['user_receiver_handle_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['mesage_blank']
    elif len(message) > 1024:
      model['errors'] = ['mesasge_exceed_max_chars']
    
    if model['errors']:
      # return what we provided
      model['data'] = {
        'display_name': 'Mariachi in a Jar',
        'handle': user_sender_handle,
        'message': message
      }
    else: 
      sql = db.template('users', 'create_message_users')

      if user_receiver_handle == None:
        rev_handle = ''
      else:
        rev_handle = user_receiver_handle
      users = db.query_json_array(sql, {
        'cognito_user_id': cognito_user_id,
        'user_receiver_handle': rev_handle
      })
      print("USERS =-=-=-=-==")
      print(users)

      current_user = next((item for item in users if item['kind'] == 'sender'), None)
      other_user = next((item for item in users if item['kind'] == 'recv'), None)

      print("USERS=[current-user]==")
      print(current_user)
      print("USERS=[other-user]==")
      print(other_user)

      ddb_client = ddb.client()
      table_name = os.getenv("AWS_DYNAMODB_TABLE")

      if (mode == "update"):
        data = ddb.create_message(
          client=ddb_client,
          table_name=table_name,
          message_group_uuid=message_group_uuid,
          message=message,
          current_user_uuid=current_user['uuid'],
          current_user_display_name=current_user['display_name'],
          current_user_handle=current_user['handle']
        )
      elif (mode == "create"):
        data = ddb.create_message(
          client=ddb_client,
          table_name=table_name,
          message=message,
          current_user_uuid=current_user['uuid'],
          current_user_display_name=current_user['display_name'],
          current_user_handle=current_user['handle'],
          other_user_uuid=other_user['uuid'],
          other_user_display_name=other_user['display_name'],
          other_user_handle=other_user['handle']
        )

      model['data'] = data
    return model