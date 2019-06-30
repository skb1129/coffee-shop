import json

from flask import Flask, request, jsonify
from flask_cors import CORS

from .database.models import setup_db, Drink

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''


# db_drop_and_create_all()


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
def add_drink():
    """
    Permission "post:drinks" endpoint: "/drinks"
    :json title: string, recipe: dict
    :return: drinks: List containing newly created drink in long format
    """
    drink = Drink(title=request.json['title'], recipe=json.dumps([request.json['recipe']]))
    drink.insert()
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def update_drink(drink_id):
    """
    Permission "patch:drinks" endpoint: "/drinks/<id>"
    :json title: string, recipe: dict
    :param drink_id: Integer representing the drink to be updated
    :return: drinks: List containing the updated drink in long format
    """
    drink = Drink.query.get(drink_id)
    if not drink:
        return jsonify({
            'error': f'No drink found with id: {drink_id}',
            'success': False,
            'drinks': []
        }), 404
    drink.title = request.json['title'] if 'title' in request.json else drink.title
    drink.recipe = json.dumps(request.json['recipe']) if 'recipe' in request.json else drink.recipe
    drink.update()
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
