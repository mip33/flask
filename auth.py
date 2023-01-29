from database import UserModel, Session, Advertisement, TokenModel
from errors import HttpError
from app import bcrypt
import uuid
import time


def password_auth(session: Session, user_data: dict):
    user = session.query(UserModel).filter(UserModel.email == user_data['email']).first()

    if not user:
        raise HttpError(404, 'user with such email does not exist')
    if not bcrypt.check_password_hash(user.password_hash.encode(), user_data['password'].encode()):
        raise HttpError(401, 'wrong password')

    return user


def token_auth(session: Session, token: str):
    try:
        token = uuid.UUID(token)
    except (ValueError, TypeError):
        raise HttpError(401, 'incorrect token')
    token = session.query(TokenModel).get(token)
    if not token:
        raise HttpError(401, 'indicated token is not found')
    if time.time() - token.creation_time.timestamp() > 86400:
        raise HttpError(401, 'token has expired, please request new one')
    return token


def owner_token_auth(session: Session, adv_id: int, token: TokenModel):
    advertisement = session.query(Advertisement).get(adv_id)
    if not advertisement:
        raise HttpError(404, 'indicated advertisement does not exist')
    if advertisement.owner != token.user_id:
        raise HttpError(401, 'advertisements could only be deleted by their authorised owner')
    return advertisement
