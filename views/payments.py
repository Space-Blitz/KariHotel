from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask import Blueprint, Response, request, jsonify

from controllers.extensions import task_after_function
from controllers.connect import db


payment = Blueprint('payments', __name__)
# doctype_credit = 'credit'


@payment.route('/api/v1/payment', methods=['POST'])
# @jwt_required
def submit_payment():
    """
    Make any paymnets
    returns: user data
    """
    data = request.get_json()
    check_for_required_values(data, REGISTER)
    access_token = db.signup(
        data.get('email'),
        data.get('user_id'),
        data.get('price'),
        data.get('rooms'),
        round(data.get('rooms')*data.get('price')),

        data.get('date_booked_for'),
        data.get('payment_status'),
        data.get('payment_type'),
        data.get('payment_'),
        data.get('contact')
    )
    task_after_function(  # Create a daemonic process with heavy function
        target=Emails.send_registration_email,
        args=[data.get('email'),data.get('surname'), data.get('password'), data.get('contact'), data.get('othernames'),access_token,],
        daemon=True
    ).start()
    return jsonify({'message':'Successful registration. Please login'}), 200
