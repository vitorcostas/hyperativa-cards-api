from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.models import User
from app.utils import validate_password


api = Namespace('Login', description='Login related operations')

login_model = api.model('LoginModel', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})


@api.route('/login')
class LoginController(Resource):
    @api.doc(
        responses={
            200: 'Successfully logged in',
            401: 'Invalid username or password'
        }
    )
    @api.expect(login_model, validate=True)
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(username=username).first()
            if not user or not validate_password(password, user.password):
                return {"message": "Invalid credentials"}, 401

            access_token = create_access_token(identity={'username': user.username, 'id': user.id})
            return {'access_token': access_token}, 200
        except Exception as e:
            return {"message": str(e)}, 500



