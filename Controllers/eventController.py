import os

from flask import Response
from application import app

from flask import jsonify, request
from flask_restful import Resource, reqparse

from Models.Event import Event
from Services.eventService import EventService

from Exceptions.event_not_found_exception import EventNotFoundException
from Exceptions.event_duplicate_exception import EventDuplicateException

# для валидации
from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect, CSRFError

# связь с сервисом
_eventService = EventService()

# app.config['SECRET_KEY'] = 'your secret key'
# csrf = CSRFProtect(app)


# class EventForm(FlaskForm):
#     eventName = StringField('Event Name', validators = [DataRequired()])
#     description = TextAreaField('Description', validators=[DataRequired()])
#     location = StringField('Location', validators=[DataRequired()])
#     date = DateField('Date', format = '%Y-%m-%d')
#     startTime = TimeField('Start Time', format='%H:%M')
#     endTime = TimeField('End Time', format='%H:%M')
#     program = TextAreaField('Program', validators=[DataRequired()])
#     invitees = StringField('Invitees', validators=[DataRequired()])
    
# @app.before_request
# def disable_csrf_protection_on_api():
#     if request.path.startswith("/es/"):
#         csrf.exempt(disable_csrf_protection_on_api)

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
        event.date = request_data['date']
        event.startTime = request_data['startTime']
        event.endTime = request_data['endTime']
        event.program = request_data['program']
        event.invitees = request_data['invitees']

            
        try:
            _eventService.addEvent(event)
            return jsonify({'events': _eventService.findAllEvents()})
        except EventDuplicateException as exp:
            return Response(exp.message, status=409)
    
    
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
        event.date = request_data['date']
        event.startTime = request_data['startTime']
        event.endTime = request_data['endTime']
        event.program = request_data['program']
        event.invitees = request_data['invitees']

        try:
            _eventService.updateEvent(id, event)
            return jsonify({'events': _eventService.findAllEvents()})
        except EventNotFoundException as exp:
            return Response(exp.message, status=404)
        except EventDuplicateException as exp:
            return Response(exp.message, status=409)

