from lib.db import db
# from aws_xray_sdk.core import xray_recorder

class UserActivities:
  def run(user_handle):
    print("UserActivities.run")
    # try:
    model = {
      'errors': None,
      'data': None
    }

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else: 
      sql = db.template('users', 'show')
      print(f"sql: {sql}")
      results = db.query_json_object(sql, {'handle': user_handle})
      print(f"results: {results}")
      model['data'] = results
  
    # # XRAY -----------------------
    # subsegment = xray_recorder.begin_subsegment('user_activities_mock-data')
    # dict = {
    #     "now": now.isoformat(),
    #     "results-size": len(model['data'])
    # }
    # subsegment.put_metadata('key', dict, 'namespace')

    return model