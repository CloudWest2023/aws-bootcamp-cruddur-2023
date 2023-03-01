from datetime import datetime, timedelta, timezone
class MessageGroups:
  def run(user_handle):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()
    results = [
      {
        'uuid': '24b95582-9e7b-4e0a-9ad1-639773ab7552',
        'display_name': 'Cruddur Campbot',
        'handle':  'campbot',
        'created_at': now.isoformat()
      },
      {
        'uuid': '417c360e-c4e6-4fce-873b-d2d71469b4ac',
        'profile_picture': '/logo_matryoshka_in_the_cloud.png',
        'display_name': 'Matryoshka in the Cloud',
        'handle':  'Matryoshka in the Cloud',
        'created_at': now.isoformat()
    }]
    model['data'] = results
    return model