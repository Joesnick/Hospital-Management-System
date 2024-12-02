from flask import Blueprint, jsonify, request
from models import db, Patient
from datetime import datetime

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()

    patients_data = [{
        'id': patient.id,
        'identification_number': patient.identification_number,
        'name': patient.name,
        'lastname': patient.lastname,
        'birthdate': patient.birthdate.strftime('%Y-%m-%d'),
        'address': patient.address,
        'phone': patient.phone
    } for patient in patients]
    
    return jsonify(patients_data), 200

@patients_bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()

    # Validación de campos obligatorios
    required_fields = ['identification_number', 'name', 'lastname', 'birthdate', 'address', 'phone']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    # Validación de formato de fecha
    try:
        birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Validación de número de teléfono
    if not data['phone'].isdigit() or len(data['phone']) not in [10, 12]:
        return jsonify({'error': 'Phone number must be 10 or 12 digits'}), 400

    # Crear y guardar el paciente si todas las validaciones están correctas
    new_patient = Patient(
        identification_number=data['identification_number'],
        name=data['name'],
        lastname=data['lastname'],
        birthdate=birthdate,
        address=data['address'],
        phone=data['phone']
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added successfully'}), 201
