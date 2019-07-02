import json
from functools import wraps
from urllib.request import urlopen

from flask import request
from jose import jwt

AUTH0_DOMAIN = 'dev-p5iqfqz0.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'https://localhost:5000'


class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate Authentication failures
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    Obtains the access token from the Authorization Header
    :return: token: JWT token
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
        }, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer'
        }, 401)
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found'
        }, 401)
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be Bearer token'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    """
    Checks if the permissions are included in the payload
    :param permission: Required permission
    :param payload: Decoded JWT
    """
    if permission not in payload.get('permissions', []):
        raise AuthError({
            'code': 'unauthorised',
            'description': 'Required permissions not available in the token'
        }, 401)
    return True


def verify_decode_jwt(token):
    """
    Verify and return decoded JWT
    :param token: JWT from request header
    :return: payload: Decoded JWT
    """
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Invalid header. Use an RS256 signed JWT Access Token'
        }, 401)
    if unverified_header['alg'] == 'HS256':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Invalid header. Use an RS256 signed JWT Access Token'
        }, 401)
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token is expired'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims, please check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)
        return payload


def requires_auth(permission=''):
    """
    Creates and returns a decorator for authentication
    :param permission: Required permission
    :return: requires_auth_decorator: Authentication decorator
    """

    def requires_auth_decorator(f):
        """
        :param f: Function to be wrapped
        :return: wrapper: Wrapper function
        """

        @wraps(f)
        def wrapper(*args, **kwargs):
            """
            This function validates and checks permission from the JWT
            It throws an AuthError exception if permission do not match or the JWT is invalid
            :return: f: Wrapped function with decoded JWT payload
            """
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
