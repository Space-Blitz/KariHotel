from flask_jwt_extended import (jwt_required, get_jwt_identity, create_access_token)
from flask import Blueprint, Response, request, jsonify

import time

from multiprocessing import Process

from models.fields import LOGIN, REGISTER
from controllers.validator import check_for_required_values
from controllers.connect import Database as db


auth = Blueprint('auth', __name__)

# doctype_credit = 'credit'

@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
    Login a user
    returns: user data
    """
    data = request.get_json()
    check_for_required_values(data, LOGIN)
    heavy_process=Process(  # Create a daemonic process with heavy "my_func"
        target=db.my_func,
        args=['word',],
        daemon=True
    )
    heavy_process.start()
    # heavy_process.join()
    # return Response(
    #     mimetype='application/json',
    #     status=200
    # )
    
    return jsonify({'message':'Lift off'}), 200


@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    """
    Login a user
    returns: user data
    """
    return jsonify({'message':'Lift off'}), 200




@auth.route('/api/v1/auth/request-password-reset', methods=['POST'])
def request_to_reset_password():
    """
    Login a user
    returns: user data
    """
    return jsonify({'message':'Lift off'}), 200

@auth.route('/api/v1/auth/reset-password', methods=['PATCH'])
def reset_password():
    """
    Login a user
    returns: user data
    """
    return jsonify({'message':'Lift off'}), 200




