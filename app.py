from flask import Flask, request, jsonify
from bson.objectid import ObjectId
import pymongo

app = Flask(__name__)

# MongoDB configuration
myclient = pymongo.MongoClient("mongodb+srv://shanilevi88761234:gcU9wrihkCKBsYWk@cluster0.0gpkkw0.mongodb.net/")
mydb = myclient["shani"]
mycol = mydb["cars"]

@app.route('/carss', methods=['POST'])
def add_car():
    data = request.json
    car_id = mycol.insert_one(data).inserted_id
    return jsonify({'message': 'Car added successfully', 'car_id': str(car_id)})

@app.route('/carss', methods=['GET'])
def get_cars():
    cars = list(mycol.find())
    # Convert ObjectId to string manually in the response
    for car in cars:
        car['_id'] = str(car['_id'])
    return jsonify(cars)

@app.route('/carss/<string:id>', methods=['GET'])
def get_car(id):
    car = mycol.find_one({'_id': ObjectId(id)})
    if car:
        # Convert ObjectId to string manually in the response
        car['_id'] = str(car['_id'])
        return jsonify(car)
    return jsonify({'message': 'Car not found'}), 404

@app.route('/carss/<string:id>', methods=['PUT'])
def update_car(id):
    data = request.json
    result = mycol.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.modified_count:
        return jsonify({'message': 'Car updated successfully'})
    return jsonify({'message': 'Car not found'}), 404

@app.route('/carss/<string:id>', methods=['DELETE'])
def delete_car(id):
    result = mycol.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Car deleted successfully'})
    return jsonify({'message': 'Car not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)






