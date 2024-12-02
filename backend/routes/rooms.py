from flask import Blueprint, jsonify, request
from models import db, Room, Internment
from datetime import datetime

rooms_bp = Blueprint('rooms', __name__)
internments_bp = Blueprint('internments', __name__)

# Obtener todas las habitaciones
@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([
        {'id': r.id, 'number': r.number, 'type': r.type, 'capacity': r.capacity, 'available': r.available}
        for r in rooms
    ])

# Crear una nueva habitación
@rooms_bp.route('/rooms', methods=['POST'])
def add_room():
    data = request.get_json()

    # Validación de campos obligatorios
    if not data.get('number') or not data.get('type') or not data.get('capacity'):
        return jsonify({'error': 'All fields are required: number, type, capacity'}), 400

    try:
        capacity = int(data.get('capacity'))  # Convertir a entero
    except (ValueError, TypeError):
        return jsonify({'error': 'Capacity must be a positive integer'}), 400

    room_type = data.get('type', '').lower()  # Convertir a minúsculas

    valid_types = ['single', 'shared', 'icu']
    if room_type not in valid_types:
        return jsonify({'error': f'Type must be one of the following: {", ".join([t.capitalize() for t in valid_types])}'}), 400

    # Crear y guardar la habitación si todas las validaciones son exitosas
    new_room = Room(
        number=data['number'],
        type=room_type.capitalize(),
        capacity=capacity,
        available=True
    )
    db.session.add(new_room)
    db.session.commit()
    return jsonify({'message': 'Room added successfully'}), 201