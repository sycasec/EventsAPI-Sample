import datetime
import sys
from flask import Flask, abort, request
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
web_api = Api(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WebCalendar.db'


class EventModel(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()
parser = reqparse.RequestParser()
parser.add_argument('event', type=str, help='The event name is required!', required=True)
parser.add_argument('date', type=inputs.date, help='The event date with the correct format is required! The correct format is YYYY-MM-DD!', required=True)
resource_fields = {'id': fields.Integer, 'event': fields.String, 'date': fields.DateTime(dt_format='iso8601')}


class EventByID(Resource):
    @marshal_with(resource_fields)
    def get(self, event_id):
        event = EventModel.query.filter(EventModel.id == event_id).first()
        if not event:
            abort(404, "The event doesn't exist!")
        return event

    def delete(self, event_id):
        event = EventModel.query.filter(EventModel.id == event_id).delete()
        if not event:
            abort(404, "The event doesn't exist")
        db.session.commit()
        return {'message': 'The event has been deleted!'}


class TodayPoint(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = EventModel.query.filter(EventModel.date == datetime.date.today()).all()
        if not result:
            abort(404, message='No events today!')
        return result


class EventsPoint(Resource):
    @marshal_with(resource_fields)
    def get(self):
        start = request.args.get('start_time')
        end = request.args.get('end_time')
        if start and end:
            between = EventModel.query.filter(EventModel.date.between(start, end)).all()
            return between
        else:
            result = EventModel.query.all()
            return result

    def post(self):
        args = parser.parse_args()
        event = EventModel(event=args['event'], date=args['date'])
        db.session.add(event)
        db.session.commit()
        response = {
            'message': 'The event has been added!',
            'event': args.event,
            'date': str(args.date.date())
        }
        return response


web_api.add_resource(EventByID, '/event/<int:event_id>')
web_api.add_resource(TodayPoint, '/event/today')
web_api.add_resource(EventsPoint, '/event')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(port=8080)
