import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:paris12ysolo12@localhost:5432/api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default='pendiente')
    created_at = db.Column(db.DateTime, server_default=db.func.now())#Esta funcion es algo rara, la investigue para que ponga la fecha que tenga la maquina

    def __init__(self, reporter, description, status='pendiente'):
        self.reporter = reporter
        self.description = description
        self.status = status

class IncidentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Incident
        load_instance = True

incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)

@app.route('/', methods=['GET'])
def get_welcome():
    return jsonify({'message': 'la API funca bien :)'})

@app.route('/incidents', methods=['POST'])
def create_incident():
    reporter = request.json.get('reporter')
    description = request.json.get('description')

    if not reporter:
        return jsonify({'error': 'El campo "reporter" es obligatorio'}), 400
    if not description or len(description) < 10:
        return jsonify({'error': 'La descripción debe tener al menos 10 caracteres'}), 400

    new_incident = Incident(reporter=reporter, description=description)
    db.session.add(new_incident)
    db.session.commit()

    return incident_schema.jsonify(new_incident), 201

@app.route('/incidents', methods=['GET'])
def get_incidents():
    all_incidents = Incident.query.all()
    return incidents_schema.jsonify(all_incidents)

@app.route('/incidents/<int:id>', methods=['GET'])
def get_incident(id):
    incident = Incident.query.get(id)
    if not incident:
        return jsonify({'error': 'Incidente no encontrado'}), 404
    return incident_schema.jsonify(incident)

@app.route('/incidents/<int:id>', methods=['PUT'])
def update_incident(id):
    incident = Incident.query.get(id)
    if not incident:
        return jsonify({'error': 'Incidente no encontrado'}), 404

    status = request.json.get('status')
    if status not in ['pendiente', 'en proceso', 'resuelto']:
        return jsonify({'error': 'Estado inválido. Debe ser: pendiente, en proceso o resuelto'}), 400

    incident.status = status
    db.session.commit()
    return incident_schema.jsonify(incident)

@app.route('/incidents/<int:id>', methods=['DELETE'])
def delete_incident(id):
    incident = Incident.query.get(id)
    if not incident:
        return jsonify({'error': 'Incidente no encontrado'}), 404

    db.session.delete(incident)
    db.session.commit()
    return jsonify({'message': 'Incidente eliminado correctamente'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3001)
