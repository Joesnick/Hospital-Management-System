from flask import Blueprint, jsonify, request
from models import db, Doctor
from datetime import datetime

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([
        {
            'id': d.id,
            'name': d.name,
            'lastname': d.lastname,
            'id_number': d.id_number,
            'license': d.license,
            'specialty': d.specialty,
            'phone': d.phone
        }
        for d in doctors
    ])


# Crear un nuevo doctor con validaciones
@doctors_bp.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.get_json()

    # Validación adicional para los campos nuevos
    if not data['id_number'] or not data['license']:
        return jsonify({'error': 'ID number and License number are required'}), 400

    new_doctor = Doctor(
        name=data['name'],
        lastname=data['lastname'],
        id_number=data['id_number'],
        license=data['license'],
        specialty=data['specialty'],
        phone=data['phone']
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor added successfully'}), 201
