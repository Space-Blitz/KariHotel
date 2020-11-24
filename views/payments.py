from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask import Blueprint, Response, request, jsonify
from multiprocessing import Process

from controllers.connect import db


payment = Blueprint('payments', __name__)
# doctype_credit = 'credit'
class Payments():

    def __init__(self):
        self.database = Database()
        self.name = 'tam'

    @payment.route('/api/v1/payment', methods=['POST'])
    # @jwt_required
    def submit_payment():
        """
        Make any paymnets
        returns: user data
        """
        print(request.get_json())
        # db. 
        # print(self.name)
        return jsonify({'message':'Lift off from payments'}), 200