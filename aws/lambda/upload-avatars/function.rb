require 'aws-sdk-s3'
require 'json'
require 'jwt'

def handler(event:, context:)
  puts "event: #{event}"

  # return CORS headers for preflight check
  if event['routeKey'] == ' OPTIONS /{proxy+}'
    puts ({step: 'preflight', message: 'preflight CORS check'}.to_json)
    {
      headers: {
        "Access-Control-Allow-Headers": "*, Authorization", 
        "Access-Control-Allow-Origin": "https://3000-mariachiina-awsbootcamp-f0x6sksrrgh.ws-us103.gitpod.io", 
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
      },
      statusCode: 200
    }
  else
    token = event['headers']['authorization'].split(' ')[1]
    puts { 'step': 'presignedurl', 'access_token': token }

    body_hash = JSON.parse(event["body"])
    extension = body_hash["extension"]

    decoded_token = JWT.decod token, nil, false
    puts "decoded toeken #{decoded_token.inspect}"
    cognito_user_id = decoded_token['sub']

    s3 = Aws::S3::Resource.new
    bucket_name = ENV["AWS_S3_BUCKET_UPLOADS"]
    object_key = `#{cognito_user_uuid}.#{extension}`

    puts({object_key: "object_key"}.to_json)

    obj = s3.bucket(bucket_name).object(object_key)
    url = obj.presigned_url(:put, expires_in: 300)
    url # this is the data that will be returned
    body = {url: url}.to_json
    { 
      headers: {
        "Access-Control-Allow-Headers": "*, Authorization",
        "Access-Control-Allow-Origin": "https://3000-mariachiina-awsbootcamp-f0x6sksrrgh.ws-us103.gitpod.io",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
      },
      statusCode: 200, 
      body: body 
    }
  end # if
end # def

puts handler(
  event: {}, 
  context: {}
)