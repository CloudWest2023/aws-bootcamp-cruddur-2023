from datetime import datetime, timedelta, timezone
class NotificationsActivities:
  def run():
    now = datetime.now(timezone.utc).astimezone()
    results = [
      {
        'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109aaa',
        'profile_picture': '/bubble_w03.png',
        'handle':  'Cruddur Campbot 03',
        'message': '*Week 03 — Decentralized Authentication*',
        'created_at': (now - timedelta(days=2)).isoformat(),
        'expires_at': (now + timedelta(days=5)).isoformat(),
        'likes_count': 5,
        'replies_count': 1,
        'reposts_count': 0,
        'replies': [
          {
            'uuid': '26e12864-1c26-5c3a-9658-97a10f8faaaa',
            'profile_picture': '/logo_mariachi_in_a_jar_white.png',
            'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109aaa',
            'handle':  'Mariachi in a Jar',
            'message': 'Technical Tasks\nProvision via ClickOps a Amazon Cognito User Pool.\nInstall and configure Amplify client-side library for Amazon Congito.\nImplement API calls to Coginto in custom login, signup page.\nShow conditional elements and data based on logged in or logged out',
            'likes_count': 0,
            'replies_count': 0,
            'reposts_count': 0,
            'created_at': (now - timedelta(days=2)).isoformat()
          },
          {
            'uuid': '26e12864-1c26-5c3a-9658-97a10f8faabc',
            'profile_picture': '/logo_mariachi_in_a_jar_white.png',
            'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109aaa',
            'handle':  'Mariachi in a Jar',
            'message': 'Business Scenario\nThe fractional CTO has suggested that authentication be solved before implementing any other business logic in the application and to ensure that we use a decentralized authentication service and specifically Amazon Cognito.',
            'likes_count': 0,
            'replies_count': 0,
            'reposts_count': 0,
            'created_at': (now - timedelta(days=2)).isoformat()
          },
          {
            'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea70',
            'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eeh',
            'profile_picture': '/logo_mariachi_in_a_jar_white.png',
            'handle':  'Mariachi in a Jar',
            'message': 'Weekly Outcome\nPractical knowledge of implementing a decentralized authentication service into a web-application with custom login and signup pages in a react application.',
            'likes_count': 0,
            'replies_count': 0,
            'reposts_count': 0,
            'created_at': (now - timedelta(days=2)).isoformat()
          }
        ],
      },
      {
        'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109bbb',
        'profile_picture': '/bubble_w02.png',
        'handle':  'Cruddur Campbot 02',
        'message': 'Week 02 — Observability',
        'created_at': (now - timedelta(days=2)).isoformat(),
        'expires_at': (now + timedelta(days=5)).isoformat(),
        'likes_count': 5,
        'replies_count': 1,
        'reposts_count': 0,
        'replies': [
          {
            'uuid': '26e12864-1c26-5c3a-9658-97a10f8fbbb',
            'profile_picture': '/logo_mariachi_in_a_jar_white.png',
            'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109bbb',
            'handle':  'Mariachi in a Jar',
            'message': 'Task info',
            'likes_count': 0,
            'replies_count': 0,
            'reposts_count': 0,
            'created_at': (now - timedelta(days=2)).isoformat()
          }
        ],
      },
      {
        'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109ccc',
        'profile_picture': '/bubble_w01.png',
        'handle':  'Cruddur Campbot 01',
        'message': 'Week 01',
        'created_at': (now - timedelta(days=2)).isoformat(),
        'expires_at': (now + timedelta(days=5)).isoformat(),
        'likes_count': 5,
        'replies_count': 1,
        'reposts_count': 0,
        'replies': [
          {
            'uuid': '26e12864-1c26-5c3a-9658-97a10f8fccca',
            'profile_picture': '/logo_mariachi_in_a_jar_white.png',
            'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109ccc',
            'handle':  'Mariachi in a Jar',
            'message': 'Task info',
            'likes_count': 0,
            'replies_count': 0,
            'reposts_count': 0,
            'created_at': (now - timedelta(days=2)).isoformat()
          }
        ],
      },
      {
        'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109ddd',
        'profile_picture': '/bubble_w00.png',
        'handle':  'Cruddur Campbot 00',
        'message': 'Week 00',
        'created_at': (now - timedelta(days=2)).isoformat(),
        'expires_at': (now + timedelta(days=5)).isoformat(),
        'likes_count': 5,
        'replies_count': 1,
        'reposts_count': 0,
        'replies': [
          {
            'uuid': '26e12864-1c26-5c3a-9658-97a10f8fddda',
            'profile_picture': '/logo_mariachi_in_a_jar_white.png',
            'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109ddd',
            'handle':  'Mariachi in a Jar',
            'message': 'Task info',
            'likes_count': 0,
            'replies_count': 0,
            'reposts_count': 0,
            'created_at': (now - timedelta(days=2)).isoformat()
          }
        ],
      },
    ]
    return results