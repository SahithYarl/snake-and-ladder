from flask import Flask, request, render_template, jsonify
from database import db, UserAction
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://snake_user:yourpassword@localhost/snake_ladder'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Game configuration
board = {99: 10, 76: 54, 34: 1, 27: 5}  # Snakes
ladders = {3: 22, 8: 30, 28: 84, 58: 77}  # Ladders


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/roll-dice', methods=['POST'])
def roll_dice():
    user_id = request.json.get('user_id', 'anonymous')
    current_position = request.json.get('current_position', 0)
    dice_roll = random.randint(1, 6)

    new_position = current_position + dice_roll
    new_position = board.get(new_position, ladders.get(new_position, new_position))

    # Log action in the database
    action = UserAction(user_id=user_id, action=f"Rolled {dice_roll}, moved to {new_position}")
    db.session.add(action)
    db.session.commit()

    return jsonify({
        'dice_roll': dice_roll,
        'new_position': new_position
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
