from flask import request, jsonify
from flask.views import MethodView
from validation import validate, CreateUserValidator, GetOrDeleteAllTokenValidator, DeleteTokenValidator, \
    CreateAdvertisementValidator, PatchAdvertisementValidator
from app import bcrypt
from database import UserModel, Session, TokenModel, Advertisement
from sqlalchemy.exc import IntegrityError
from errors import HttpError
from auth import password_auth, owner_token_auth, token_auth


def create_user():
    user_data = validate(request.json, CreateUserValidator)
    user_data['password_hash'] = bcrypt.generate_password_hash(user_data.pop('password').encode()).decode()

    with Session() as session:
        user = UserModel(**user_data)
        session.add(user)

        try:
            session.commit()
        except IntegrityError:
            raise HttpError(409, 'user with such email already exists')

        return jsonify({'status': 'success', 'id': user.id, 'email': user.email})


def get_token():
    user_data = validate(request.json, GetOrDeleteAllTokenValidator)

    with Session() as session:
        user = password_auth(session, user_data)
        token = TokenModel(user=user)
        session.add(token)

        try:
            session.commit()
        except IntegrityError:
            raise HttpError(418, 'something terrible and almost impossible happened, please try to get token again')

        return jsonify({
            'token': token.id,
            'message': 'save your token, you will not be able to get it again, only to create the new one'
        })


def delete_all_tokens():
    user_data = validate(request.json, GetOrDeleteAllTokenValidator)
    with Session() as session:
        user = password_auth(session, user_data)
        session.query(TokenModel).filter(TokenModel.user_id == user.id).delete()
        session.commit()
        return jsonify({'status': 'success'})


def delete_token():
    user_data = validate(request.json, DeleteTokenValidator)
    with Session() as session:
        user = password_auth(session, user_data)
        try:
            token = session.query(TokenModel).filter(TokenModel.id == user_data['token']).first()
        except (ValueError, TypeError):
            raise HttpError(401, 'incorrect token')
        if (not token) or (token.user_id != user.id):
            raise HttpError(404, 'indicated token does not exist')
        session.delete(token)
        session.commit()
        return jsonify({'status': 'success'})


class AdvertisementView(MethodView):

    def get(self, adv_id: int):
        with Session() as session:
            adv = session.\
                query(Advertisement).\
                filter(Advertisement.id == adv_id).\
                join(Advertisement.user).\
                first()

            if not adv:
                raise HttpError(404, 'indicated advertisement does not exist')

            return jsonify({'id': adv.id,
                            'title': adv.title,
                            'owner_email': adv.user.email,
                            'description': adv.description,
                            'created_at': adv.created_at})

    def post(self):
        adv_data = validate(request.json, CreateAdvertisementValidator)

        with Session() as session:
            token = token_auth(session, request.headers.get('token'))
            adv_data['owner'] = token.user_id
            new_adv = Advertisement(**adv_data)

            session.add(new_adv)
            session.commit()

            return jsonify({'status': 'success', 'id': new_adv.id, 'title': new_adv.title,
                            'description': new_adv.description, 'created_at': new_adv.created_at})

    def patch(self, adv_id: int):
        adv_data = validate(request.json, PatchAdvertisementValidator)

        with Session() as session:
            token = token_auth(session, request.headers.get('token'))
            advertisement = owner_token_auth(session, adv_id, token)

            for field, value in adv_data.items():
                setattr(advertisement, field, value)

            session.add(advertisement)
            session.commit()

            return jsonify({'status': 'success', 'id': advertisement.id, 'title': advertisement.title,
                            'description': advertisement.description})

    def delete(self, adv_id: int):
        with Session() as session:
            token = token_auth(session, request.headers.get('token'))
            advertisement = owner_token_auth(session, adv_id, token)

            session.delete(advertisement)
            session.commit()

            return jsonify({'status': 'success'})
