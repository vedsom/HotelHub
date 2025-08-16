from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'rating': self.rating,
            'image': self.image
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False) 

with app.app_context():
    db.create_all()

    if Hotel.query.count() == 0:
        sample_hotels = [
            Hotel(name="Hotel Sunshine", location="New York", rating=4.5, image="assets/hotels/hotel1.jpg"),
            Hotel(name="Sea View Resort", location="Miami", rating=4.2, image="assets/hotels/hotel2.jpg"),
            Hotel(name="Mountain Retreat", location="Denver", rating=4.8, image="assets/hotels/hotel3.jpg")
        ]
        db.session.add_all(sample_hotels)
        db.session.commit()

    if User.query.count() == 0:
        default_user = User(username="admin", password="1234")
        db.session.add(default_user)
        db.session.commit()

@app.route('/hotels', methods=['GET'])
def get_hotels():
    hotels = Hotel.query.all()
    return jsonify([hotel.to_dict() for hotel in hotels])

@app.route('/hotels/<int:id>', methods=['GET'])
def get_hotel_by_id(id):
    hotel = Hotel.query.get(id)
    if hotel:
        return jsonify(hotel.to_dict())
    return jsonify({'error': 'Hotel not found'}), 404

@app.route('/hotels', methods=['POST'])
def add_hotel():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('location') or data.get('rating') is None:
        return jsonify({'error': 'Name, location, and rating are required'}), 400

    try:
        rating_value = float(data['rating'])
        if rating_value < 0 or rating_value > 5:
            return jsonify({'error': 'Rating must be between 0 and 5'}), 400
    except ValueError:
        return jsonify({'error': 'Rating must be a number'}), 400

    new_hotel = Hotel(
        name=data['name'].strip(),
        location=data['location'].strip(),
        rating=rating_value,
        image=data.get('image', None)
    )
    db.session.add(new_hotel)
    db.session.commit()
    return jsonify({'message': 'Hotel added successfully!'}), 201

@app.route('/hotels/<int:id>', methods=['PUT'])
def update_hotel(id):
    data = request.get_json()
    hotel = Hotel.query.get(id)
    if not hotel:
        return jsonify({'error': 'Hotel not found'}), 404

    if 'rating' in data:
        try:
            rating_value = float(data['rating'])
            if rating_value < 0 or rating_value > 5:
                return jsonify({'error': 'Rating must be between 0 and 5'}), 400
            hotel.rating = rating_value
        except ValueError:
            return jsonify({'error': 'Rating must be a number'}), 400

    if 'name' in data and data['name'].strip() != '':
        hotel.name = data['name'].strip()
    if 'location' in data and data['location'].strip() != '':
        hotel.location = data['location'].strip()
    if 'image' in data and data['image'].strip() != '':
        hotel.image = data['image'].strip()

    db.session.commit()
    return jsonify({'message': 'Hotel updated successfully!'})

@app.route('/hotels/<int:id>', methods=['DELETE'])
def delete_hotel(id):
    hotel = Hotel.query.get(id)
    if hotel:
        db.session.delete(hotel)
        db.session.commit()
        return jsonify({'message': 'Hotel deleted successfully!'})
    return jsonify({'error': 'Hotel not found'}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"success": True, "message": "Login successful!"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
