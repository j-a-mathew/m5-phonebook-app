from audioop import add
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/contacts', methods = ['POST']) # send data to database --> can be seen in Insomnia
@token_required # pulls from helpers.py --> make sure none of function will happen unless it gets what it wants, proper data/user
def create_contact(current_user_token):
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Contact(name, email, phone_number, address, user_token=user_token)

    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response) # show on API what values are put to database / confirmation

@api.route('/contacts', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all() 
    # bring back all contacts inside of the database
    response = contacts_schema.dump(contacts) # multiple 'contacts'
    return jsonify(response)

# Get a single contact
@api.route('/contacts/<id>', methods = ['GET']) # <id> is a variable in the URL
@token_required
def get_single_contact(current_user_token, id):
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)

# Update endpoint
@api.route('/contacts/<id>', methods = ['POST', 'PUT'])
@token_required
def update_contact(current_user_token, id):
    contact = Contact.query.get(id)
    contact.name = request.json['name']
    contact.email = request.json['email']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

# Delete endpoint
@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)