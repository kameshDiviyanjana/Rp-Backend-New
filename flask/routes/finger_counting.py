# finger_counting.py
from flask import Blueprint, jsonify

finger_counting_bp = Blueprint('finger_countingss', __name__)

@finger_counting_bp.route('/', methods=['GET'])
def count_fingers():
    return jsonify({"message": "Finger counting works!"})
