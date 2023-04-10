from datetime import datetime, timedelta, timezone
from opentelemetry import trace # uses only opentelemetry-api in requirements.txt

from lib.db import pool, query_wrap_array

# tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run():
  # def run(logger):
  #   logger.info("Logs from HomeActivities.py")
  # LOGGER.info('Hello Cloudwatch! from  /api/activities/home')
  # with tracer.start_as_current_span("mock-data-home-activities"): # This line creates spans
  #   span = trace.get_current_span()           # this and the next lines add attributes to spans
  #   now = datetime.now(timezone.utc).astimezone()
  #   span.set_attribute("app.now", now.isoformat())
  #   span.set_attribute("app.env", "local machine")
    # span.set_attribute("app.result_length", len(results))
    
    sql = query_wrap_array(""" 
            SELECT
              activities.uuid,
              users.display_name,
              users.handle,
              activities.message,
              activities.replies_count,
              activities.reposts_count,
              activities.likes_count,
              activities.reply_to_activity_uuid,
              activities.expires_at,
              activities.created_at
            FROM public.activities
            LEFT JOIN public.users ON users.uuid = activities.user_uuid
            ORDER BY activities.created_at DESC
          """)
    print("======================PRINT SQL=======================")
    print(sql)
    print("\n")
    with pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql)
        # this will return a tuple 
        # the first field being the data
        json = cur.fetchone()
        print("=101010====================PRINT ROW======================")
        for dictionary in json[0]:
          for key, value in dictionary.items():
            print(f"{key}: {value}")
        print("\n\n")
    return json[0]