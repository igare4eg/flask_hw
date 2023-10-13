from app import app
from flask import jsonify, request
from flask.views import MethodView
from pydantic import BaseModel, ValidationError

from models import UserModel, Session, AdsModel
from sqlalchemy.exc import IntegrityError

from validate import CreateAdsSchema, CreateUserSchema


class ApiException(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


@app.errorhandler(ApiException)
def error_handler(error: ApiException):
    response = jsonify({"status": "error", "message": error.message})
    response.status_code = error.status_code
    return response


def validate(data: dict, schema_class):
    try:
        return schema_class(**data).dict()
    except ValidationError as er:
        return ApiException(400, er.errors())


class UserView(MethodView):
    def get(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            if user is None:
                raise ApiException(404, "user not found")
            return jsonify({"id": user_id, "email": user.email})

    def post(self):
        user_data = validate(request.json, CreateUserSchema)
        with Session() as session:
            new_user = UserModel(**user_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, "email is busy")
            return jsonify({"id": new_user.id, "email": new_user.email})

    def delete(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            session.delete(user)
            session.commit()
            return jsonify({"status": "deleted"})


class AdsView(MethodView):
    def get(self, ads_id: int):
        with Session() as session:
            ads = session.query(AdsModel).get(ads_id)
            if ads is None:
                raise ApiException(404, "advertisement not found")
            return jsonify(
                {
                    "id": ads.id,
                    "title": ads.title,
                    "description": ads.description,
                    "created_at": ads.created_at,
                    "user_id": ads.user_id,
                }
            )

    def post(self):
        ads_data = validate(request.json, CreateAdsSchema)
        print(ads_data)
        with Session() as session:
            if ads_data["user_id"] is None:
                raise ApiException(403, "please login")
            new_ads = AdsModel(**ads_data)
            session.add(new_ads)
            session.commit()
            return jsonify(
                {
                    "id": new_ads.id,
                    "title": new_ads.title,
                    "description": new_ads.description,
                    "created_at": new_ads.created_at,
                    "user_id": new_ads.user_id,
                }
            )

    def delete(self, ads_id: int):
        with Session() as session:
            ads = session.query(AdsModel).get(ads_id)
            session.delete(ads)
            session.commit()
            return jsonify({"status": "deleted"})
