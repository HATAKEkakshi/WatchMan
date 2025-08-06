import random    
import string
from itsdangerous import BadSignature,Serializer,URLSafeSerializer,URLSafeTimedSerializer,SignatureExpired
from fastapi import HTTPException, status
from bson import ObjectId
import jwt
from uuid import uuid4
from config.secert import security_settings
from phonenumbers.phonenumberutil import region_code_for_country_code
import pycountry
from passlib.context import CryptContext
from pathlib import Path
from datetime import datetime,timezone,timedelta
APP_DIR= Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR.parent / "templates"
_serializer=URLSafeTimedSerializer(security_settings.JWT_SECRET)
# Password hashing context
password_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_country_from_dial_code(dial_code: str) -> str:
    try:
        # Remove '+' if present and convert to integer
        code = int(dial_code.strip().replace("+", ""))
        
        # Get ISO Alpha-2 region code (e.g., 'IN' for +91)
        region_code = region_code_for_country_code(code)
        if not region_code:
            return "Country not recognized for this code."

        # Use pycountry to get full country name
        country = pycountry.countries.get(alpha_2=region_code)
        return country.name if country else "Country not found in database."
    except Exception as e:
        return f"Invalid input: {e}"
def id_generator(length=7):
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    return ''.join(random.choices(characters, k=length))
def generate_country(dial_code: str) -> str:
     try:
        # Remove '+' if present and convert to integer
        code = int(dial_code.strip().replace("+", ""))
        
        # Get ISO Alpha-2 region code (e.g., 'IN' for +91)
        region_code = region_code_for_country_code(code)
        if not region_code:
            return "Country not recognized for this code."

        # Use pycountry to get full country name
        country = pycountry.countries.get(alpha_2=region_code)
        return country.name if country else "Country not found in database."
     except Exception as e:
        return f"Invalid input: {e}"
def password_hash(password: str) -> str:
    password_hash=password_context.hash(password)
    return password_hash
def generate_access_token(data:dict, expiry:timedelta=timedelta(days=1))->str:
    return jwt.encode(
        payload={
            **data,
            "jti":str(uuid4()),
            "exp": int((datetime.now(timezone.utc) + expiry).timestamp()),
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET
    )

def decode_access_token(token:str)->dict| None:
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token has expired"
        )
    except jwt.PyJWTError:
        return None
def generate_url_safe_token(data:dict,salt:str|None=None)->str:
    return _serializer.dumps(data,salt=salt)
def decode_url_safe_token(token,salt:str,expiry:timedelta|None=None)->dict|None:
    try:
        return _serializer.loads(token,salt=salt,max_age=expiry.total_seconds() if expiry else None)
    except(BadSignature,SignatureExpired):
        return None
def generate_otp_token(data:dict, expiry:timedelta=timedelta(days=1))->str:
    return jwt.encode(
        payload={
            **data,
            "exp": int((datetime.now(timezone.utc) + expiry).timestamp()),
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET
    )
def decode_otp_token(token:str)->dict| None:
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token has expired"
        )
    except jwt.PyJWTError:
        return None
def clean_document(doc: dict) -> dict:
    clean = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            clean[k] = str(v)  # ✅ convert ObjectId to string
        elif isinstance(v, datetime):
            clean[k] = v.isoformat()
        else:
            clean[k] = v
    return clean