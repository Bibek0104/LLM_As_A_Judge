import jwt

from datetime import datetime, timedelta

from fastapi import Request, HTTPException


SECRET_KEY = "ericsson_llm_judge"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


USERS = {
    "admin": "admin123",
    "bibek": "bibek123"
}


def authenticate(username: str, password: str):

    if username in USERS and USERS[username] == password:
        return True

    return False


def create_token(username: str):

    payload = {
        "sub": username,
        "exp": datetime.utcnow()
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


def get_current_user(request: Request):

    token = request.cookies.get("access_token")

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please login first."
        )

    return verify_token(token)