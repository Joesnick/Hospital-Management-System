from flask import Blueprint, jsonify, request
from models import db, Prescription
from datetime import datetime

prescriptions_bp = Blueprint('prescriptions', __name__)

# Obtener todas las recetas médicas
@prescriptions_bp.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    prescriptions = Prescription.query.all()
    return jsonify([
        {'id': p.id, 'code': p.code, 'date': str(p.date), 'medicine': p.medicine, 'dose': p.dose, 
         'duration': p.duration, 'patient_id': p.patient_id, 'doctor_id': p.doctor_id}
        for p in prescriptions
    ])

# Crear una nueva receta
@prescriptions_bp.route('/prescriptions', methods=['POST'])
def add_prescription():
    data = request.get_json()

    # Validación de campos obligatorios
    if not data.get('code') or not data.get('date') or not data.get('medicine') or not data.get('dose') or not data.get('duration'):
        return jsonify({'error': 'All fields are required: code, date, medicine, dose, duration'}), 400

    # Validación de formato de fecha
    try:
        prescription_date = datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Validación de duración (debe ser un número positivo)
    if not isinstance(data['duration'], int) or data['duration'] <= 0:
        return jsonify({'error': 'Duration must be a positive integer'}), 400

    # Crear y guardar la receta si todas las validaciones son correctas
    new_prescription = Prescription(
        code=data['code'],
        date=prescription_date,
        medicine=data['medicine'],
        dose=data['dose'],
        duration=data['duration'],
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id']
    )
    db.session.add(new_prescription)
    db.session.commit()
    return jsonify({'message': 'Prescription added successfully'}), 201

# Actualizar una receta
@prescriptions_bp.route('/prescriptions/<int:id>', methods=['PUT'])
def update_prescription(id):
    prescription = Prescription.query.get(id)
    if not prescription:
        return jsonify({'message': 'Prescription not found'}), 404
    
    data = request.get_json()
    prescription.code = data.get('code', prescription.code)
    prescription.date = data.get('date', prescription.date)
    prescription.medicine = data.get('medicine', prescription.medicine)
    prescription.dose = data.get('dose', prescription.dose)
    prescription.duration = data.get('duration', prescription.duration)
    db.session.commit()
    return jsonify({'message': 'Prescription updated successfully'})

# Eliminar una receta
@prescriptions_bp.route('/prescriptions/<int:id>', methods=['DELETE'])
def delete_prescription(id):
    prescription = Prescription.query.get(id)
    if not prescription:
        return jsonify({'message': 'Prescription not found'}), 404
    
    db.session.delete(prescription)
    db.session.commit()
    return jsonify({'message': 'Prescription deleted successfully'})
