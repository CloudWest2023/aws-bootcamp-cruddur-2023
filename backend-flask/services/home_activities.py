from datetime import datetime, timedelta, timezone
from opentelemetry import trace # uses only opentelemetry-api in requirements.txt

from lib.db import db

# tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run(cognito_user_id=None):
  # def run(logger):
  #   logger.info("Logs from HomeActivities.py")
  # LOGGER.info('Hello Cloudwatch! from  /api/activities/home')
  # with tracer.start_as_current_span("mock-data-home-activities"): # This line creates spans
  #   span = trace.get_current_span()           # this and the next lines add attributes to spans
  #   now = datetime.now(timezone.utc).astimezone()
  #   span.set_attribute("app.now", now.isoformat())
  #   span.set_attribute("app.env", "local machine")
    # span.set_attribute("app.result_length", len(results))
    
    sql = db.template('activities', 'home')
    results = db.query_json_array(sql)
    print(f"sql statement: {sql}\n")

    return results