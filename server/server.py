from flask import Flask, jsonify, request, abort
from horsesDAO import horseDAO
import betfairApi as bf

app = Flask(__name__, static_url_path='', static_folder='../html/')

# # default to login page
# @app.route('/')
# def index(self):
#   return redirect("127.0.0.1:5000/login.html"))

# upcoming racemeetings
@app.route('/events')
def getRaceMeetings():
  return jsonify(bf.getEvents())

# upcoming races @ upcoming race meetings
@app.route('/upcraces')
def getRacesMeetingDet():
  return jsonify(bf.getUpcRaces())

# horses in the database
@app.route('/horses')
def getAll():
  results = horseDAO.getAll()
  return jsonify(results)

#curl "http://127.0.0.1:5000/horses/1"
@app.route('/horses/<int:id>')
def findById(id):
  foundHorse = horseDAO.findByID(id)
  return jsonify(foundHorse)

#curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{}' http://127.0.0.1:5000/horses
@app.route('/horses', methods=['POST'])
def create():
  #global nextId
  if not request.json:
    abort(400)
  # other checking that properly formatted
  horse = {
      "id": request.json['id'],
      "Name": request.json['Name'],
      "Age": request.json['Age'],
      "Sex": request.json['Sex'],
      "Owner": request.json['Owner'],
      "Trainer": request.json['Trainer'],
      "Form": request.json['Form']
  }
  values =(horse['id'],horse['Name'],horse['Age'],horse['Sex'],horse['Owner'],horse['Trainer'],horse['Form'])
  horseDAO.create(values)
  return jsonify(horse)

#curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X PUT -d '{"id":}' http://127.0.0.1:5000/horses/3
@app.route('/horses/<int:id>', methods=['PUT'])
def update(id):
  foundHorse = horseDAO.findByID(id)
  if not foundHorse:
    abort(404)
  if not request.json:
    abort(400)
  reqJson = request.json
  if 'Name' in reqJson:
    foundHorse['Name']= reqJson['Name']
  if 'Age' in reqJson:
    foundHorse['Age']= reqJson['Age']
  if 'Sex' in reqJson:
    foundHorse['Sex']= reqJson['Sex']
  if 'Owner' in reqJson:
    foundHorse['Owner']= reqJson['Owner']
  if 'Trainer' in reqJson:
    foundHorse['Trainer']= reqJson['Trainer']
  if 'Form' in reqJson:
    foundHorse['Form']= reqJson['Form']
  values = (foundHorse['Name'],foundHorse['Age'],foundHorse['Sex'],foundHorse['Owner'],foundHorse['Trainer'],foundHorse['Form'],foundHorse['id'])
  horseDAO.update(values)
  return jsonify(foundHorse)

@app.route('/horses/<int:id>', methods=['DELETE'])
def delete(id):
  horseDAO.delete(id)
  return jsonify({"deleted successfully":True})

if __name__ == '__main__' :
    app.run(debug= True)
