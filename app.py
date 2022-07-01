
from sqlite3 import dbapi2
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS, cross_origin
#from bson import ObjectId

# Instantiation
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/proyecto'
mongo = PyMongo(app)
# Settings
CORS(app, resources={r"/*": {"origins": "*"}})


# Database
db = mongo.db.usuarios
db2 = mongo.db.users

# ------------------------------------------------ ROUTES ---------------------------------------------------------------

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


@app.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
  print(request.json['email'])
  print(request.json['password'])
  user = db2.find_one({'email': request.json['email']})
  if request.json['password'] == user['password']:
    print(user)
    print(type(user))
    #print(type(jsonify(user)))
    #print(type({}))
    #print(jsonify({}))
    print(type(jsonify(str(user))))
    return jsonify(str(user))
  else:
    return {}
  

# Función para la creacion o registro de usuarios
@app.route('/users', methods=['POST'])
def createUser():
  print(request.json)
  id = db2.insert_one({
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password'],
    'intentos': 3
  })
  print(id.inserted_id)
  return str(id.inserted_id)

# Funcion para la consulta de usuarios
@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)


# Funcion para la consulta especifica de usuario
@app.route('/users/<id>', methods=['GET'])
def getUser(id):
  user = db.find_one({'_id': ObjectId(id)})
  print(user)
  return jsonify({
      '_id': str(ObjectId(user['_id'])),
      'name': user['name'],
      'email': user['email'],
      'password': user['password']
  })

# Funcion para eliminar un usuario especifico
@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
  db.delete_one({'_id': ObjectId(id)})
  return jsonify({'message': 'User Deleted'})


# Funcion para editar un usuario en especifico
@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
  print(request.json)
  db.update_one({'_id': ObjectId(id)}, {"$set": {
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password']
  }})
  return jsonify({'message': 'User Updated'})

if __name__ == "__main__":
    app.run(debug=True)
