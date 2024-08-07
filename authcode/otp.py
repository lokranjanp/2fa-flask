import pyotp
import random
import json

def generate_otp(user_secret):
    """generates otp for a user using their stored secret key"""
    counter = random.randint(0, 696969)
    hotp = pyotp.HOTP(user_secret)
    return hotp.at(counter)

def cache_otp(r, username, otp):
    """Caches the OTP and username in Redis"""
    user_data = {
        "otp": otp,
        "username": username
    }
    r.setex(f'otp:{username}', 300, json.dumps(user_data))


def verify_otp(r, username, input_otp):
    """Verify the OTP against the cached one"""
    otp_data_json = r.get(f'otp:{username}')
    if otp_data_json:
        otp_data = json.loads(otp_data_json)
        cached_otp = otp_data["otp"]

        if cached_otp == input_otp:
            # Log it as a success
            r.delete(f'otp:{username}')
            return True
        else:
            # Log it as a failure
            return False
    else:
        print("No OTP found in cache.")
        return False
