from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flask import Blueprint, Response, request, jsonify, abort

from controllers.extensions import task_after_function
from controllers.validator import check_for_required_values
from models.fields import MM_PAYMENTS
from controllers.connect import db, Database
from models.constants import SECRET_HASH


payment = Blueprint('payments', __name__)



@payment.route('/api/v1/payment/mobilemoney', methods=['POST'])
@jwt_required
def submit_mobile_money_payment():
    """
    Submit request to make mobile money payment.
    returns: user data
    """
    data = request.get_json()
    check_for_required_values(data, MM_PAYMENTS)
    redirect = db.insertPayment(data)
    return jsonify({'message':'Payment Initiated', 'url':redirect}), 200

@payment.route('/api/v1/payment/webhook', methods=['POST'])
def mobile_money_webhook():
    """
    Confirm payment
    returns: user data
    """
    data = request.get_json()
#     if request.headers.get("verif-hash")==SECRET_HASH:
    if True:
        print(data)
        try:
            if data['data']['status'].lower()=='successful':
                task_after_function(
                target=Database.update_payment,
                args=[data['data']['status'].lower(),data['data']['tx_ref']],
                daemon=True
                ).start()
            return jsonify({'message':'Successful'}),200
        except Exception as error:
            print(str(error))
            abort(400,desription='Failed transaction')
    return jsonify({'message':'Failed'}),400
    

    print(data)
    print(str(request))
    # check_for_required_values(data, MM_PAYMENTS)
    # rows= db.get_transactions()
    return jsonify({'message':'Successful.'}), 200


@payment.route('/api/v1/transactions', methods=['GET'])
@jwt_required
def get_transactions():
    """
    Get all transactions
    returns: user data
    """
    rows= db.get_all_transactions()
    return jsonify(rows), 200


@payment.route('/api/v1/accomodation-types', methods=['GET'])
def get_accomodation_types():
    """
    Get all  accomodation types
    returns: user data
    """
    rows= db.get_accomodation_categories()
    return jsonify(rows), 200

@payment.route('/api/v1/payment_stats', methods=['GET'])
@jwt_required
def get_payment_stats():
    """
    Get all  accomodation types
    returns: user data
    """
    rows= db.get_bookings_stats()
    return jsonify(rows), 200

# @payment.route('/api/v1/accomodation-types', methods=['POST'])
# @jwt_required
# def add_accomodation_type():
#     """
#     Get all accomodation types
#     returns: user data
#     """
#     data = request.get_json()
#     check_for_required_values(data, MM_PAYMENTS)
#     rows= db.get_transactions()
#     return jsonify({'message':'Successful registration. Please login'}), 200

# @payment.route('/api/v1/accomodation-types/<type_id>', methods=['PUT'])
# @jwt_required
# def edit_accomodation_type(type_id):
#     """
#     Make any paymnets
#     returns: user data
#     """
#     data = request.get_json()
#     check_for_required_values(data, MM_PAYMENTS)
#     rows= db.get_transactions()
#     return jsonify({'message':'Successful registration. Please login'}), 200


