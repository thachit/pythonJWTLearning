import time
from webbrowser import Error

import jwt
import datetime

username = 'thachit'
secret_key = 'pythonJWTLearning'
algorithm = 'HS256'
issuer = 'Python JWT Learning'
audience = 'Python JWT Audience'


current_time = datetime.datetime.now(datetime.timezone.utc)
exchange_count = 0

def create_access_token(
        user_id: str,
        sub: str,
        expire_at_delta: int = 1
):
    issue_at = datetime.datetime.now(datetime.timezone.utc)
    expired_at = issue_at + datetime.timedelta(minutes=expire_at_delta)

    access_token_payload = {
        "user_id": user_id,
        "sub": sub,
        "exp": expired_at,
        "iss": issuer,
        "aud": audience,
        "iat": issue_at
    }
    return jwt.encode(access_token_payload, secret_key, algorithm=algorithm), expired_at

def decode_token(token):
    return jwt.decode(
        token, secret_key, algorithms=[algorithm],
        issuer=issuer,
        audience=audience
    )

def exchange_refresh_token(refresh_token_to_exchange):
    payload = decode_token(refresh_token_to_exchange)
    sub = payload['sub']
    if sub != username:
        raise jwt.InvalidTokenError()

    new_access_token, expired_at = create_access_token(user_id=725, sub=username, expire_at_delta=1)
    new_refresh_token, expired_at = create_access_token(user_id=725, sub=username, expire_at_delta=1 * 24 * 60)
    return new_access_token, new_refresh_token


access_token, access_token_expired_at = create_access_token(user_id=725, sub=username, expire_at_delta=1)
refresh_token, refresh_token_expired_at = create_access_token(user_id=725, sub=username, expire_at_delta=1 * 24 * 60)

print("\n\n====================================================================================")
print(f"\n** TOKEN = {access_token}")
print(f"\n** REFRESH TOKEN = {refresh_token}")
print("\n\n====================================================================================")

while True:
    try:
        decoded_token = decode_token(access_token)
        # print(f"** Decoded Token = {decoded_token}")
    except jwt.ExpiredSignatureError:
        print("** Token has expired")
        print("\n\n====================================================================================")
        access_token, refresh_token = exchange_refresh_token(refresh_token)
        exchange_count += 1
        print(f"\n** {exchange_count} NEW TOKEN = {access_token}")
        print(f"\n** {exchange_count} NEW REFRESH TOKEN = {refresh_token}")
    except jwt.InvalidTokenError as e:
        print(f"** Invalid Token: {str(e)}")
    except Exception as e:
        print(f"** {e}")

    time.sleep(10)