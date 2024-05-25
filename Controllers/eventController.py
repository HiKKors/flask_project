from flask import Response
from application import app

from flask import jsonify, request
from flask_restful import Resource, reqparse

from Models.Event import Event
from Services.eventService import EventService

from Exceptions.event_not_found_exception import EventNotFoundException

# связь с сервисом
_eventService = EventService()

class EventControler(Resource):
    """
    Класс контроллер таблицы event
    Содержит методы для каждой CRUD операции
    """
    @staticmethod
    @app.route('/es/v1/events', methods=['GET'])
    def get_events():
        """
        GET-операция
        Запрашивает у сервиса и возвращает объект со всеми записями в таблице event
        """
        return jsonify({'events': _eventService.findAllEvents()})
    
    @app.route('/es/v1/events/<int:event_id>', methods=['GET'])
    def get_event(event_id):
        """
        Параметры: event_id
        
        GET-операция
        Запрашивает у сервиса и возвращает объект со одной записью с id = event_id
        """
        try:
            event = _eventService.findEvent(event_id)
            return jsonify(event.serialize())
        except EventNotFoundException as exp:
            return Response(exp.message, status=404)
        
    @staticmethod
    @app.route('/es/v1/events/<int:id>', methods=['DELETE'])
    def delete_event(id):
        """
        Параметры: id
        
        DELETE-операция
        Запрашивает у сервиса и возвращает id удаленного мероприятия
        """
        try:
            _eventService.deleteEvent(id)
            return jsonify(id)
        except EventNotFoundException as exp:
            return Response(exp.message, status=404)
        
    @staticmethod
    @app.route('/es/v1/events', methods=['POST'])
    def add_event():
        """
        POST-операция
        Добавляет новую запись в таблицу
        
        Возвращает: все записи, вместе с новой, в формате json
        """
        request_data = request.get_json()#получаем тело запроса
        
        event = Event()
        event.eventName = request_data['eventName']
        event.description = request_data['description']
        event.location = request_data['location']
        event.startTime = request_data['startTime']
        event.endTime = request_data['endTime']
        event.program = request_data['program']
        event.invitees = request_data['invitees']

        _eventService.addEvent(event)

        return jsonify({'events': _eventService.findAllEvents()})
    
    
    @staticmethod
    @app.route('/es/v1/events/<int:id>', methods=['PUT'])
    def update_event(id):
        """
        Параметры: id
        
        PUT-операция
        Обновляет данные для записи с введенным id 
        
        Возвращает: Список всех записей
        """
        request_data = request.get_json()
        # print(request_data)
        
        event = Event()
        event.eventName = request_data['eventName']
        event.description = request_data['description']
        event.location = request_data['location']
        event.startTime = request_data['startTime']
        event.endTime = request_data['endTime']
        event.program = request_data['program']
        event.invitees = request_data['invitees']

        try:
            _eventService.updateEvent(id, event)
            return jsonify({'events': _eventService.findAllEvents()})
        except EventNotFoundException as exp:
            return Response(exp.message, status=404)

