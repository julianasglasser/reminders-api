from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Reminders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reminder = db.Column(db.String(200), unique=True)
    done = db.Column(db.String(10), unique=True)

    def __init__(self, reminder, done):
        self.reminder = reminder
        self.done = done


class RemindersSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('reminder', 'done')


reminder_schema = RemindersSchema()
reminders_schema = RemindersSchema(many=True)


# endpoint to create new reminder
@app.route("/reminder", methods=["POST"])
def add_user():
    reminder = request.json['reminder']
    done = request.json['done']

    new_reminder = Reminders(reminder, done)

    db.session.add(new_reminder)
    db.session.commit()

    return jsonify(new_reminder)


# endpoint to show all reminders
@app.route("/reminder", methods=["GET"])
def get_reminder():
    all_reminders = Reminders.query.all()
    result = reminders_schema.dump(all_reminders)
    return jsonify(result.data)


# endpoint to get reminder detail by id
@app.route("/reminder/<id>", methods=["GET"])
def reminder_detail(id):
    reminder = Reminders.query.get(id)
    return reminder_schema.jsonify(reminder)


# endpoint to update reminder
@app.route("/reminder/<id>", methods=["PUT"])
def reminder_update(id):
    user = Reminders.query.get(id)
    reminder = request.json['reminder']
    done = request.json['done']

    user.done = done
    user.reminder = reminder

    db.session.commit()
    return reminder_schema.jsonify(user)


# endpoint to delete reminder
@app.route("/reminder/<id>", methods=["DELETE"])
def user_delete(id):
    user = Reminders.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return reminder_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)
