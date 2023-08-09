from lib.db import db

class UpdateProfile:
  def run(cognito_user_id, bio, display_name):
    print(f"cognito id: {cognito_user_id} \nbio: {bio}\ndisplay_name: {display_name}\n===============================")
    model = {
      'errors': None,
      'data': None
    }

    if display_name == None or len(display_name) < 1:
      model['errors'] = ['display_name_blank']
      print(f"model['errors']: {model['errors']}")

    if model['errors']:
      model['data'] = {
        'bio': bio,
        'display_name': display_name
      }
    else:
      handle = UpdateProfile.update_profile(bio, display_name, cognito_user_id)
      print(f"handle: {handle} ===============================")
      data = UpdateProfile.query_users_short(handle)
      model['data'] = data
    return model

  def update_profile(bio,display_name,cognito_user_id):
    if bio == None:    
      bio = ''

    sql = db.template('users','update')
    handle = db.query_commit(sql,{
      'cognito_user_id': cognito_user_id,
      'bio': bio,
      'display_name': display_name
    })

  def query_users_short(handle):
    print(f"query_users_short =======   ┻━━━━━━━┻ ︵ {handle}  ╰(°□°╰)")
    sql = db.template('users','short')
    data = db.query_json_object(sql,{
      'handle': handle
    })
    return data