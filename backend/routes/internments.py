from flask import Blueprint, jsonify, request
from models import db, Internment, Room
from datetime import datetime

internments_bp = Blueprint('internments', __name__)

# Obtener internamientos
@internments_bp.route('/internments', methods=['GET'])
def get_internments():
    internments = Internment.query.all()
    return jsonify([
        {'id': i.id, 'admission_date': str(i.admission_date), 'discharge_date': str(i.discharge_date), 
         'patient_id': i.patient_id, 'room_id': i.room_id}
        for i in internments
    ])

@internments_bp.route('/internments', methods=['POST'])
def add_internment():
    data = request.get_json()
    room = Room.query.get_or_404(data['room_id'])

    if not room.available:
        return jsonify({'error': 'Room is not available'}), 400

    # Crear internamiento
    new_internment = Internment(
        admission_date=datetime.strptime(data['admission_date'], '%Y-%m-%d'),
        discharge_date=data.get('discharge_date'),
        patient_id=data['patient_id'],
        room_id=data['room_id']
    )
    room.available = False
    db.session.add(new_internment)
    db.session.commit()
    return jsonify({'message': 'Internment added successfully'}), 201

@internments_bp.route('/internments/<int:id>/discharge', methods=['PUT'])
def discharge_internment(id):
    internment = Internment.query.get_or_404(id)
    internment.discharge_date = datetime.now().date()
    room = Room.query.get_or_404(internment.room_id)
    room.available = True  # Libera la habitación
    
    db.session.commit()
    return jsonify({'message': 'Patient discharged and room is now available'})
