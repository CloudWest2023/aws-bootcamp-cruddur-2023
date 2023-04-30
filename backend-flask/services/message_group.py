from datetime import datetime, timedelta, timezone

from lib.db import DB # this is necessary to find the handle from the uuid.
from lib.ddb import DDB

class MessageGroup:
  def run(cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }

    sql = DB.template("", "users", "uuid_from_cognito_user_id")
    current_user_uuid = DB.query_value(
      sql = sql, 
      params= {
      'cognito_user_id': cognito_user_id
    })

    print(f"UUID: {current_user_uuid}")

    DDB = DDB.client()
    data = DDB.list_message_groups(DDB, current_user_uuid)
    print(f"list_message_groups: {data}")

    model['data'] = data
    return model


# results = [
#   {
#     'uuid': '24b95582-9e7b-4e0a-9ad1-639773ab7552',
#     'profile_picture': '/logo_cruddur_campbot.png',
#     'display_name': 'Cruddur Campbot',
#     'handle':  'cruddur_campbot',
#     'created_at': now.isoformat()
#   },
#   {
#     'uuid': '417c360e-c4e6-4fce-873b-d2d71469b4ac',
#     'profile_picture': '/logo_pinata.png',
#     'display_name': 'Coding Piñata',
#     'handle':  'coding_pinata',
#     'created_at': now.isoformat()
# }]