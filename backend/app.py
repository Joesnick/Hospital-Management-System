from flask import Flask, jsonify
from models import db
from routes.patients import patients_bp
from routes.doctors import doctors_bp
from routes.appointments import appointments_bp
from routes.treatments import treatments_bp
from routes.rooms import rooms_bp
from routes.internments import internments_bp
from routes.prescriptions import prescriptions_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:QWE123asd_@localhost:3306/hospital_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registrar los Blueprints
app.register_blueprint(patients_bp)
app.register_blueprint(doctors_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(treatments_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(internments_bp)
app.register_blueprint(prescriptions_bp)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource Not Found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': 'Please try again later'}), 500

if __name__ == '__main__':
    app.run(debug=True)
