"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    res = {
        "message": "ok",
        "family": members
    }
    return jsonify(res), 200


@app.route("/member/<int:member_id>")
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        res = {
            "message": "ok",
            "member": member
        }
        return jsonify(res), 200

    if member is None:
    
        res = {
            "message": "user not found"
        }
        return jsonify(res), 404


@app.route("/member", methods=['POST'])
def add_member():
    new_member = request.data
    new_member_decode = json.loads(new_member)
    if 'id' not in new_member_decode:
        new_member_decode['id'] = jackson_family._generateId()

    member = jackson_family.get_member(new_member_decode['id'])

    if member:
        res = {
            "message": "Id already in use"
        }
        return jsonify(res), 400

    members = jackson_family.add_member(new_member_decode)
    res = {
        "message": "ok",
        "members": members
    }
    return jsonify(res), 200


@app.route("/member/<int:member_id>", methods=['DELETE'])
def delete_member(member_id):
    members = jackson_family.delete_member(member_id)
    res = {
        "message": "ok",
        "members": members
    }
    return jsonify(res), 200







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
