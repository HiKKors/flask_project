# from flask import Blueprint
# import jsonify

# event_api = Blueprint('event_api', __name__)

from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse

from Models.Event import Event
from Services.eventService import EventService

app = Flask(__name__)
api = Api()

_eventService = EventService()

class EventControler(Resource):
    @staticmethod
    @app.route('/es/v1/event', methods=['GET'])
    @app.route('/es/v1/events/<int:event_id>', methods=['GET'])
    def get_events(event_id = None):
        if event_id != None:
            event = _eventService.findEvent(event_id)
            return jsonify(event.serialize())
        else:
            return jsonify({'events': _eventService.findAllEvents()})

    def start(self):
        api.init_app(app)
        return app