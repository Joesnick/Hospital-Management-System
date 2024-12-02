from flask import Blueprint, jsonify, request
from models import db, Treatment

treatments_bp = Blueprint('treatments', __name__)


# Obtener todos los tratamientos
@treatments_bp.route('/treatments', methods=['GET'])
def get_treatments():
    treatments = Treatment.query.all()
    return jsonify([
        {'id': t.id, 'name': t.name, 'description': t.description, 'duration': t.duration}
        for t in treatments
    ])

# Crear un nuevo tratamiento
@treatments_bp.route('/treatments', methods=['POST'])
def add_treatment():
    data = request.get_json()

    # Validación de campos obligatorios
    if not data.get('code') or not data.get('name') or not data.get('description') or not data.get('duration') or not data.get('patient_id') or not data.get('doctor_id'):
        return jsonify({'error': 'All fields are required: code, name, description, duration, patient_id, doctor_id'}), 400

    # Validación de duración (debe ser un número positivo)
    if not isinstance(data['duration'], int) or data['duration'] <= 0:
        return jsonify({'error': 'Duration must be a positive integer'}), 400

    # Validación de código único
    existing_treatment = Treatment.query.filter_by(code=data['code']).first()
    if existing_treatment:
        return jsonify({'error': 'Treatment code must be unique'}), 400

    # Crear y guardar el tratamiento si todas las validaciones son exitosas
    new_treatment = Treatment(
        code=data['code'],
        name=data['name'],
        description=data['description'],
        duration=data['duration'],
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id']
    )
    db.session.add(new_treatment)
    db.session.commit()
    return jsonify({'message': 'Treatment added successfully'}), 201

# Actualizar un tratamiento
@treatments_bp.route('/treatments/<int:id>', methods=['PUT'])
def update_treatment(id):
    treatment = Treatment.query.get(id)
    if not treatment:
        return jsonify({'message': 'Treatment not found'}), 404
    
    data = request.get_json()
    treatment.name = data.get('name', treatment.name)
    treatment.description = data.get('description', treatment.description)
    treatment.duration = data.get('duration', treatment.duration)
    db.session.commit()
    return jsonify({'message': 'Treatment updated successfully'})

# Eliminar un tratamiento
@treatments_bp.route('/treatments/<int:id>', methods=['DELETE'])
def delete_treatment(id):
    treatment = Treatment.query.get(id)
    if not treatment:
        return jsonify({'message': 'Treatment not found'}), 404
    
    db.session.delete(treatment)
    db.session.commit()
    return jsonify({'message': 'Treatment deleted successfully'})
