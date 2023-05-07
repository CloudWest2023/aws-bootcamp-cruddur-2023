from datetime import datetime, timedelta, timezone

import os, sys
current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..'))
sys.path.append(parent_path)
# from lib.db import db
# from lib.ddb_aws import ddbAWS as ddb
from lib.ddb import ddb
from lib.db import db
from utils.bcolors import *


class MessageGroups:
  def run(cognito_user_id):

    printh("MessageGroups.run ...")

    model = {
      'errors': None,
      'data': None
    }

    sql = db.template('users', 'uuid_from_cognito_user_id')
    current_user_uuid = db.query_value(sql, { 
        'cognito_user_id': cognito_user_id 
    })

    printh(f"uuid data type: {type(current_user_uuid)}")
    print(f"UUID: {current_user_uuid}")

    ddb_client = ddb.client()
    data = ddb.list_message_groups(ddb_client, current_user_uuid)
    printc(f"   list_message_groups: {data}")

    model['data'] = data

    printh("   ... MessageGroups.run")

    return model