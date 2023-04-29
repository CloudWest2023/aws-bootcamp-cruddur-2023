import time
import requests, json
# Web response handler
import urllib3

# JWT Library
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode
from flask_awscognito.exceptions import FlaskAWSCognitoError, TokenVerifyError

# class FlaskAWSCognitoError(Exception):
#     pass

# class TokenVerifyError(Exception):
#     pass

CYAN = '\033[96m'
ENDC = '\033[0m'

class JWTTokenVerifier:
    def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
        
        print(f"{CYAN}JWTTokenVerifier initialising...{ENDC}\n")
        
        self.region = region
        if not self.region:
            print("FlaskAWSCognitoError --- No AWS region provided")
            # raise FlaskAWSCognitoError("No AWS region provided")
        print(f"{CYAN}self.region: {self.region}{ENDC}\n")

        self.user_pool_id = user_pool_id
        print(f"{CYAN}self.user_pool_id: {self.user_pool_id}{ENDC}\n")
        
        self.user_pool_client_id = user_pool_client_id
        print(f"{CYAN}self.user_pool_client_id: {self.user_pool_client_id}{ENDC}\n")
        self.claims = None

        if not request_client:
            self.request_client = requests.get
        else:
            self.request_client = request_client

        self._load_jwk_keys()


    @classmethod
    def extract_access_token(self, request_headers):

        print(f"{CYAN}extract_access_token in action{ENDC}\n")
        
        access_token = None
        auth_header = request_headers.get("Authorization")
        
        if auth_header and " " in auth_header:
            _, access_token = auth_header.split()
            print(f"{CYAN}access_token: {access_token}{ENDC}\n")
            return access_token


    # AttributeError: 'JWTTokenVerifier' object has no attribute 'request_client'
    def get_client_keys(self, keys_url):
        
        http = urllib3.PoolManager()
        response = http.request('GET', keys_url)
        response = json.loads(response.data.decode('utf-8'))

        print(f"{CYAN}Response from keys_url: {response}{ENDC}")
        print(f"{CYAN}Response type: {type(response)}{ENDC}")
        # client_keys = response["keys"]
        # print(f"response keys:\n{client_keys}\n\n\n")
        return response


    def _load_jwk_keys(self):
        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        print()
        try:
            self.jwk_keys = self.get_client_keys(keys_url)  # AttributeError
        except requests.exceptions.RequestException as e:
            print("FlaskAWSCognitoError --- No AWS region provided")
            # raise FlaskAWSCognitoError(str(e)) from e


    @staticmethod
    def _extract_headers(token):
        try:
            headers = jwt.get_unverified_headers(token)
            return headers
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e


    def _find_pkey(self, headers):
        kid = headers["kid"]
        # search for the kid in the downloaded public keys
        key_index = -1
        for i in range(len(self.jwk_keys)):
            if kid == self.jwk_keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise TokenVerifyError("Public key not found in jwks.json")
        return self.jwk_keys[key_index]


    @staticmethod
    def _verify_signature(token, pkey_data):
        try:
            # construct the public key
            public_key = jwk.construct(pkey_data)
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e
        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit(".", 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise TokenVerifyError("Signature verification failed")


    @staticmethod
    def _extract_claims(token):
        try:
            claims = jwt.get_unverified_claims(token)
            return claims
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e


    @staticmethod
    def _check_expiration(claims, current_time):
        if not current_time:
            current_time = time.time()
        if current_time > claims["exp"]:
            raise TokenVerifyError("Token is expired")  # probably another exception


    def _check_audience(self, claims):
        # and the Audience  (use claims['client_id'] if verifying an access token)
        audience = claims["aud"] if "aud" in claims else claims["client_id"]
        if audience != self.user_pool_client_id:
            raise TokenVerifyError("Token was not issued for this audience")


    def verify(self, token, current_time=None):
        """ https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py """
        if not token:
            raise TokenVerifyError("No token provided")

        headers = self._extract_headers(token)
        pkey_data = self._find_pkey(headers)
        self._verify_signature(token, pkey_data)

        claims = self._extract_claims(token)
        self._check_expiration(claims, current_time)
        self._check_audience(claims)

        self.claims = claims

        return claims