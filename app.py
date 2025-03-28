from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:paris12ysolo12@localhost:5432/api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String, unique = True)

    def __init__(self, nombre):
        self.nombre = nombre

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)



@app.route('/', methods=['GET'])
def get_welcome_screen():
   return jsonify({
        'name' : 'Luis'
   })

@app.route('/test', methods=['POST'])
def post_test():

    nombre = request.json['nombre']
    
    new_name = Test(nombre)

    db.session.add(new_name)
    db.session.commit()

    return product_schema.jsonify(new_name)

if __name__ == '__main__':
    app.run(debug=True, port='3001')