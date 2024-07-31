from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest
from app.models import User, Card
from app import db


api = Namespace('card', description='Card related operations')

add_card_model = api.model('AddCardModel', {
    'card_number': fields.Integer(required=True, description='Card number')
})


@api.route('/add_card')
class CardController(Resource):
    @api.doc(
        responses={
            201: 'Successfully added card',
            400: 'Card already exists',
            404: 'User not found'
        }
    )
    @api.expect(add_card_model, validate=True)
    @api.doc(security='Bearer', responses={403: 'Missing Authorization Header'})
    def post(self):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            user = User.query.filter_by(id=current_user['id']).first()
            if not user:
                return {"message": "User not found"}, 404

            data = request.get_json()
            card_number = data.get('card_number')

            if Card.query.filter_by(card_number=card_number).first():
                return {"message": "Card already exists"}, 400

            new_card = Card(card_number=card_number, owner=user)
            db.session.add(new_card)
            db.session.commit()

            return {"message": "Card added successfully"}, 200
        except NoAuthorizationError as e:
            return {"message": "Missing Authorization Header"}, 403
        except BadRequest as e:
            error_msg = getattr(e, 'data', {}).get('errors', {})
            return {"message": error_msg}, 400
        except Exception as e:
            return {"message": str(e)}, 500


file_upload = api.parser()
file_upload.add_argument('file', location='files', type=FileStorage, required=True)


@api.route('/add_card_file')
class CardFileController(Resource):
    @api.doc(
        responses={
            200: 'Successfully added card',
            400: 'Card already exists',
            404: 'User not found'
        }
    )
    @api.expect(file_upload, validate=True)
    @api.doc(security='Bearer', responses={403: 'Missing Authorization Header'})
    def post(self):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            user = User.query.filter_by(id=current_user['id']).first()
            if not user:
                return {"message": "User not found"}, 404

            args = file_upload.parse_args()
            file = args['file']
            if not file:
                return {"message": "No file provided"}, 400

            cards = extract_card_numbers(file)
            added_cards = add_cards(cards, user)
            if not added_cards:
                return {"message": "No cards added"}, 200
            return {"added_cards": added_cards}, 200
        except NoAuthorizationError as e:
            return {"message": "Missing Authorization Header"}, 403
        except BadRequest as e:
            error_msg = getattr(e, 'data', {}).get('errors', {})
            return {"message": error_msg}, 400
        except Exception as e:
            return {"message": str(e)}, 500


def extract_card_numbers(file):
    cards = []

    for line in file:
        line = line.decode('utf-8').strip()
        if line.startswith('C'):

            card_number = int(line[8:26].strip())
            cards.append(card_number)

    return list(set(cards))


def add_cards(cards: list, user: User):
    added_cards = []
    existing_cards = []
    for card in cards:
        if not Card.query.filter_by(card_number=card).first():
            added_cards.append(card)
            new_card = Card(card_number=card, owner=user)
            db.session.add(new_card)
        else:
            existing_cards.append(card)
    db.session.commit()
    return added_cards
