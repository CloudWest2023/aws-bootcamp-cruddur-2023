from datetime import datetime, timedelta, timezone

import os, sys
current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..'))
sys.path.append(parent_path)
from lib.db import db
from lib.ddb import ddb
from utils.bcolors import *


class Messages:
  def run(message_group_uuid, cognito_user_id):
    printh("Messages.run() ...")
    model = {
      'errors': None,
      'data': None
    }

    sql = db.template('users', 'uuid_from_cognito_user_id')
    current_user_uuid = db.query_value(sql, { 
        'cognito_user_id': cognito_user_id 
    })

    print(f"UUID: {current_user_uuid}")


    data = ddb.list_messages(
      client=ddb.client(), 
      table_name=os.getenv("AWS_DYNAMODB_TABLE"),
      message_group_uuid=message_group_uuid
    )
    print(f"data: {data}")

    model['data'] = data
    return model
