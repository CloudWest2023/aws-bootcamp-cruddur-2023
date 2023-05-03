import time
import requests, json
# Web response handler
import urllib3

# DEBUG log utils
import os, sys
current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..'))
sys.path.append(parent_path)
from utils.bcolors import *

# JWT Library
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode
from flask_awscognito.exceptions import FlaskAWSCognitoError, TokenVerifyError

# class FlaskAWSCognitoError(Exception):
#     pass

# class TokenVerifyError(Exception):
#     pass


class JWTTokenVerifier:
    def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
        
        printh("JWTTokenVerifier initialising...")
        
        self.region = region
        if not self.region:
            printc("FlaskAWSCognitoError --- No AWS region provided")
            # raise FlaskAWSCognitoError("No AWS region provided")
        printc(f"   JWTTV.region: {self.region}")

        self.user_pool_id = user_pool_id
        printc(f"   JWTTV.user_pool_id: {self.user_pool_id}")
        
        self.user_pool_client_id = user_pool_client_id
        printc(f"   JWTTV.user_pool_client_id: {self.user_pool_client_id}")
        self.claims = None

        if not request_client:
            self.request_client = requests.get
        else:
            self.request_client = request_client

        self._load_jwk_keys()

        printh("    ... JWTTokenVerifier initialised.")



    @classmethod
    def extract_access_token(self, request_headers):

        printc(f"extract_access_token in action ...")
        
        access_token = None
        auth_header = request_headers.get("Authorization")
        printc(f"   extract_access_token.auth_header: {auth_header}")
        
        if auth_header and " " in auth_header:
            _, access_token = auth_header.split()
            printc(f"   access_token: {access_token}")
            return access_token


    # AttributeError: 'JWTTokenVerifier' object has no attribute 'request_client'
    def get_client_keys(self, keys_url):
        printh(f"get_client_key() in action ...")

        http = urllib3.PoolManager()
        response = http.request('GET', keys_url)
        response = json.loads(response.data.decode('utf-8'))

        printc(f"   get_client_keys - Response from keys_url: {response}")
        printc(f"   get_client_keys - Response type: {type(response)}")
        # client_keys = response["keys"]
        # print(f"response keys:\n{client_keys}\n\n\n")
        printh(f"   ... get_client_key() completed.")
        return response


    def _load_jwk_keys(self):
        printh(f"_load_jwk_keys() in action ...")

        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        print(f"    _load_jwk_keys - keys_url: {keys_url}")

        try:
            self.jwk_keys = self.get_client_keys(keys_url)  # AttributeError
            printc(f"   _load_jwk_keys - jwk_keys: {self.jwk_keys}")
            printc(f"   _load_jwk_keys - jwk_keys['keys'].len: {len(self.jwk_keys['keys'])}")
        except requests.exceptions.RequestException as e:
            printc("    _load_jwk_keys - FlaskAWSCognitoError --- No AWS region provided")
            # raise FlaskAWSCognitoError(str(e)) from e
        
        printh(f"   ... _load_jwk_keys() completed.")


    @staticmethod
    def _extract_headers(token):
        printh("JWTTokenVerifier._extract_headers() in action ...")
        try:
            headers = jwt.get_unverified_headers(token)
            printc(f"   _extract_headers - headers: {headers}")
            return headers
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e
        
        printh("    ... JWTTokenVerifier._extract_headers() completed.")


    def _find_pkey(self, headers):
        printh("JWTTokenVerifier._find_pkey() in action ...")

        headers_kid = headers["kid"]
        printc(f"   headers_kid: {headers['kid']}")

        # search for the kid in the downloaded public keys
        key_index = -1

        printc(f"   jwk_keys['keys'] length: {len(self.jwk_keys['keys'])}")
        for i in range(len(self.jwk_keys['keys'])):
            printc(f"   jwk_keys['keys'][{i}]: {self.jwk_keys['keys'][i]}")
            if headers_kid == self.jwk_keys["keys"][i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise TokenVerifyError("Public key not found in jwks.json")

        printh("    ... JWTTokenVerifier._find_pkey() completed.")

        return self.jwk_keys['keys'][key_index]


    @staticmethod
    def _verify_signature(token, pkey_data):
        printh("JWTTokenVerifier._verify_signature in action ...")
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
        
        printh("    ... JWTTokenVerifier._verify_signature() completed.")


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

        printh("JWTTokenVerifier.verify in action ...")

        headers = self._extract_headers(token)
        printc(f"   JWTTokenVerifier.verify.headers: {headers}") 
        pkey_data = self._find_pkey(headers)
        printc(f"   JWTTokenVerifier.verify.pkey_data: {pkey_data}") 
        self._verify_signature(token, pkey_data)

        claims = self._extract_claims(token)
        self._check_expiration(claims, current_time)
        self._check_audience(claims)

        self.claims = claims

        return claims