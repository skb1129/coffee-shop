import json

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .auth.auth import requires_auth, AuthError
from .database.models import setup_db, Drink, db_drop_and_create_all

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''


db_drop_and_create_all()


# Routes
@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    """
    Public endpoint: "/drinks"
    :return: drinks: List of drinks in short format
    """
    drinks = [drink.short() for drink in Drink.query.all()]
    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_all_drinks_detail():
    """
    Permission "get:drinks-detail" endpoint: "/drinks-detail"
    :return: drinks: List of drinks in long format
    """
    drinks = [drink.long() for drink in Drink.query.all()]
    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink():
    """
    Permission "post:drinks" endpoint: "/drinks"
    :json title: string, recipe: dict
    :return: drinks: List containing newly created drink in long format
    """
    drink = Drink(title=request.json['title'], recipe=json.dumps(request.json['recipe']))
    drink.insert()
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(drink_id):
    """
    Permission "patch:drinks" endpoint: "/drinks/<id>"
    :json title: string, recipe: dict
    :param drink_id: Integer representing the drink to be updated
    :return: drinks: List containing the updated drink in long format
    """
    drink = Drink.query.get(drink_id)
    if not drink:
        return abort(404, f'No drink found with id: {drink_id}')
    drink.title = request.json['title'] if 'title' in request.json else drink.title
    drink.recipe = json.dumps(request.json['recipe']) if 'recipe' in request.json else drink.recipe
    drink.update()
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    """
    Permission "delete:drinks" endpoint: "/drinks/<id>"
    :param drink_id: Integer representing the drink to be updated
    :return: delete: Id of the deleted record
    """
    drink = Drink.query.get(drink_id)
    if not drink:
        return abort(404, f'No drink found with id: {drink_id}')
    drink.delete()
    return jsonify({
        'success': True,
        'delete': drink_id
    })


# Error Handler
@app.errorhandler(HTTPException)
def http_exception_handler(error):
    """
    HTTP error handler for all endpoints
    :param error: HTTPException containing code and description
    :return: error: HTTP status code, message: Error description
    """
    return jsonify({
        'success': False,
        'error': error.code,
        'message': error.description
    }), error.code


@app.errorhandler(Exception)
def exception_handler(error):
    """
    Generic error handler for all endpoints
    :param error: Any exception
    :return: error: HTTP status code, message: Error description
    """
    return jsonify({
        'success': False,
        'error': 500,
        'message': f'Something went wrong: {error}'
    }), 500


@app.errorhandler(AuthError)
def auth_error_handler(error):
    """
    Authentication error handler for scoped endpoints
    :param error: AuthError instance
    :return: error: HTTP status code, message: Error description
    """
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response
