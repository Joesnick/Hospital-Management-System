from flask import Blueprint, jsonify, request
from models import db, Appointment
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

# Obtener todas las citas
@appointments_bp.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([
        {'id': a.id, 'date': str(a.date), 'time': str(a.time), 'status': a.status, 'purpose': a.purpose, 'patient_id': a.patient_id, 'doctor_id': a.doctor_id}
        for a in appointments
    ])

# Crear una nueva cita
@appointments_bp.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.get_json()

    # Validar campos obligatorios
    if not all([data.get('date'), data.get('time'), data.get('purpose'), data.get('status'), data.get('patient_id'), data.get('doctor_id')]):
        return jsonify({'error': 'All fields are required: date, time, purpose, status, patient_id, doctor_id'}), 400

    # Validar fecha
    try:
        appointment_date = datetime.strptime(data['date'], '%Y-%m-%d')
        appointment_time = datetime.strptime(data['time'], '%H:%M').time()  # Validación de hora
    except ValueError:
        return jsonify({'error': 'Invalid date or time format'}), 400

    # Validar estado
    if data['status'] not in ['pending', 'completed', 'canceled']:
        return jsonify({'error': 'Status must be pending, completed, or canceled'}), 400

    # Crear y guardar la cita
    new_appointment = Appointment(
        date=appointment_date,
        time=appointment_time,
        purpose=data['purpose'],
        status=data['status'],
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id']
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment added successfully'}), 201


# Actualizar una cita
@appointments_bp.route('/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    
    data = request.get_json()
    appointment.date = data.get('date', appointment.date)
    appointment.status = data.get('status', appointment.status)
    db.session.commit()
    return jsonify({'message': 'Appointment updated successfully'})

# Eliminar una cita
@appointments_bp.route('/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted successfully'})
