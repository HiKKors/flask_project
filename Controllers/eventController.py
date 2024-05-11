from application import app

from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse

from Models.Event import Event
from Services.eventService import EventService

# связь с сервисом
_eventService = EventService()

class EventControler(Resource):
    @staticmethod
    @app.route('/es/v1/events', methods=['GET'])
    def get_events():
        return jsonify({'events': _eventService.findAllEvents()})
    
    @app.route('/es/v1/events/<int:event_id>', methods=['GET'])
    def get_event(event_id):
        event = _eventService.findEvent(event_id)
        return jsonify(event.serialize())
        
    @staticmethod
    @app.route('/es/v1/events/<int:id>', methods=['DELETE'])
    def delete_event(id):
        _eventService.deleteEvent(id)
        return jsonify(id)
    
    @staticmethod
    @app.route('/es/v1/events', methods=['POST'])
    def add_event():
        request_data = request.get_json()#получаем тело запроса
        
        event = Event()
        event.eventName = request_data['eventName']
        event.description = request_data['description']
        event.location = request_data['location']
        event.dateId = request_data['dateId']
        event.startTime = request_data['startTime']
        event.endTime = request_data['endTime']
        event.program = request_data['program']
        event.invitees = request_data['invitees']

        _eventService.addEvent(event)

        return jsonify({'events': _eventService.findAllEvents()})
    
    
    @staticmethod
    @app.route('/es/v1/events/<int:id>', methods=['PUT'])
    def update_event(id):
        request_data = request.get_json()
        
        event = Event()
        event.eventName = request_data['eventName']
        event.description = request_data['description']
        event.location = request_data['location']
        event.dateId = request_data['dateId']
        event.startTime = request_data['startTime']
        event.endTime = request_data['endTime']
        event.program = request_data['program']
        event.invitees = request_data['invitees']

        _eventService.updateEvent(id, event)

        return jsonify({'events': _eventService.findAllEvents()})

