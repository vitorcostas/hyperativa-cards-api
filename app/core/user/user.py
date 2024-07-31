from flask import request, jsonify
from app.utils import encrypt_password
from flask_restx import Namespace, Resource, fields
from app.extentions import db
from app.models import User
from loguru import logger


api = Namespace('User', description='User related operations')

user_model = api.model('UserModel', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})


@api.route('/create_user')
class UserController(Resource):
    @api.doc(
        responses={
            201: 'Successfully created user',
            400: 'User already exists',
            500: 'Internal server error'
        }
    )
    @api.expect(user_model, validate=True)
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if User.query.filter_by(username=username).first():
                return {"message": "User already exists"}, 400

            hashed_password = encrypt_password(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"User {username} created successfully")
            return {"message": "User created successfully"}, 200
        except Exception as e:
            logger.error(e)
            return {"message": "Internal server error"}, 500
