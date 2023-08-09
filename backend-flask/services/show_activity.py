from datetime import datetime, timedelta, timezone
class ShowActivities:
  def run(activity_uuid):
    now = datetime.now(timezone.utc).astimezone()
    results = [{
      'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
      'handle':  'Andrew Brown',
      'message': 'Cloud is fun but super tough!',
      'created_at': (now - timedelta(days=2)).isoformat(),
      'expires_at': (now + timedelta(days=5)).isoformat(),
      'replies': {
        'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
        'handle':  'mariachiinajar',
        'message': 'hello, world! This is mariachi!',
        'created_at': (now - timedelta(days=2)).isoformat()
      }
    }]
    return results