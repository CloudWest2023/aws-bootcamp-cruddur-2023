from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os, sys
from utils.bcolors import *

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_group import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *


####################### AWS Cognito #######################
# from flask_awscognito import AWSCognitoAuthentication
from lib.cognito.jwt_token_verifier import JWTTokenVerifier
from flask_awscognito.exceptions import TokenVerifyError
# FlaskAWSCognitoError

####################### AWS CloudWatch #######################
import watchtower
import logging
from time import strftime

####################### AWS X-ray #######################
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

####################### HONEYCOMB #######################
# OTEL packages  --------------------------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor   # this is middleware
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

####################### ROLLBAR #######################
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

# --------------------------------- END OF LIBRARY --------------------------------- 



####################### HONEYCOMB #######################
# Initialize HONEYCOMB tracing and an exporter that can send dta to Honeycomb
provider = TracerProvider()

processor = BatchSpanProcessor(OTLPSpanExporter()) # Reads the env variables for the configuration of where to send the spans.
provider.add_span_processor(processor)

# Show this in the logs within the backend-flask app )STDOUT)
# simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(simple_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)
jwttv = JWTTokenVerifier(
  user_pool_id = os.getenv("AWS_COGNITO_USER_POOL_ID"),
  user_pool_client_id = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
  region = os.getenv("AWS_DEFAULT_REGION")
)

app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = os.getenv('AWS_COGNITO_USER_POOL_CLIENT_ID')
app.config['AWS_COGNITO_USER_POOL_ID'] = os.getenv('AWS_COGNITO_USER_POOL_ID')

# aws_auth = AWSCognitoAuthentication(app)


####################### HONEYCOMB #######################
# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()



####################### ROLLBAR #######################
rollbar_access_token = os.getenv("ROLLBAR_ACCESS_TOKEN")

with app.app_context():
  def init_rollbar() -> None:
      """init rollbar module"""
      rollbar.init(
          # access token
          rollbar_access_token,
          # environment name
          'production',
          # server root directory, makes tracebacks prettier
          root=os.path.dirname(os.path.realpath(__file__)),
          # flask already sets up logging
          allow_logging_basic_config=False)

      # send exceptions from `app` to rollbar, using flask's signal system.
      got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


@app.route('/rollbar/test_local')
def rollbar_test():
    rollbar.report_message('Seeing if rollbar works locally. NOT using dotenv', 'warning')
    return "rollbar local test"

# Configuring Logger to Use CloudWatch
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
# LOGGER.addHandler(console_handler)
# LOGGER.addHandler(cw_handler)
# LOGGER.info("some message")


####################### AWS X-RAY #######################
# xray_url = os.getenv("AWS_XRAY_URL")
# xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
# XRayMiddleware(app, xray_recorder)


frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')

origins = [frontend, backend]
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'],
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)

@app.route("/api/activities/home", methods=['GET'])
# @aws_auth.authentication_required
def data_home():
  printc(f"App Logger - REQUEST HEADERS ----------------")
  app.logger.debug(request.headers)
  
  access_token = jwttv.extract_access_token(request.headers)
  app.logger.debug(f'access token: {access_token}')

  try:
    printc(f"/api/activities/home - JWT Token Verifier's verify in action .... with access_token: {access_token}")
    claims = jwttv.verify(access_token)
    printc(f"/api/activities/home - claims: {claims}")

    # authenticated request
    app.logger.debug(f"authenticated")
    app.logger.debug(claims)
    app.logger.debug(claims['username'])
    data = HomeActivities.run(cognito_user_id=claims['username'])

  except TokenVerifyError as e:
    printc("Error: TokenVerifyError")
    # unauthenticated request
    app.logger.debug(e)
    app.logger.debug("NOT authenticated")
    data = HomeActivities.run()

  # DEBUG
  print("AUTH HEADER-------------------", file=sys.stdout)
  app.logger.debug("AUTH HEADER")
  app.logger.debug(request.headers.get('Authorization'))
  
  return data, 200


@app.route("/api/activities/notifications", methods=['GET'])
def data_nodifications():
  data = NotificationsActivities.run()
  return data, 200


@app.route("/api/activities/<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:   # Error validation
    return model['errors'], 422
  else:
    return model['data'], 200


@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():

  user_handle  = 'mariachiinajar'
  access_token = jwttv.extract_access_token(request.headers)

  try:
    printc(f"/api/activities/message_groups - JWT Token Verifier's verify in action .... with access_token: {access_token}")
    claims = jwttv.verify(access_token)
    printc(f"/api/activities/message_groups - claims: {claims}")

    # authenticated request
    app.logger.debug(f"authenticated")
    app.logger.debug(claims)
    app.logger.debug(claims['sub'])

    cognito_user_id = claims['sub']

    model = MessageGroups.run(cognito_user_id = cognito_user_id)

    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200

  except TokenVerifyError as e:
    printc("Error: TokenVerifyError")
    # unauthenticated request
    app.logger.debug("NOT authenticated")
    app.logger.debug(e)
    app.logger.debug(claims['sub'])

    claims = jwttv.verify(access_token)
    cognito_user_id = claims['sub']
    data = MessageGroups.run(cognito_user_id = cognito_user_id)
    
    return {}, 401  # This occurs when an unauthorised user tries to access something accessible only by authenticated user. 


@app.route("/api/messages/<string:message_group_uuid>", methods=['GET'])
def data_messages(message_group_uuid): 
  access_token = jwttv.extract_access_token(request.headers)

  try:
    claims = jwttv.verify(access_token)

    # authenticated request
    app.logger.debug("authenticated")
    app.logger.debug(claims)

    cognito_user_id = claims['sub']
    model = Messages.run(
      cognito_user_id = cognito_user_id,
      message_group_uuid = message_group_uuid
    )

    printc(f"=================== model\n{model}")

    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200

  except TokenVerifyError as e:
    # unauthenticated request
    app.logger.debug(e)
    return {}, 401


@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  message_group_uuid = request.json.get('message_group_uuid', None)
  user_receiver_handle = request.json.get('handle', None)
  message = request.json['message']

  access_token = jwttv.extract_access_token(request.headers)

  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return


@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  user_handle  = 'mariachiinajar'
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return


@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200


@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'mariachiinajar'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return


# @app.after_request
# def after_request(response):
#     timestamp = strftime('[%Y-%b-%d %H:%M]')
#     LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
#     return response

if __name__ == "__main__":
  app.run(debug=True)