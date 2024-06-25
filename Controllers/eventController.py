from flask import Response
from application import app

from flask import jsonify, request
from flask_restful import Resource, reqparse

from Models.Event import Event
from Services.eventService import EventService

from Exceptions.event_not_found_exception import EventNotFoundException
from Exceptions.event_duplicate_exception import EventDuplicateException
from Exceptions.IncorrectIdException import IncorrectIdException
from Exceptions.exceptionDetails import ExceptionDetails


# для валидации
from jsonschema.exceptions import ValidationError
from Validators.eventValidator import EventValidator

from logger import logger

# связь с сервисом базы данных
_eventService = EventService()
# связь с валидатором
_eventValidator = EventValidator()

def format_validation_error(e):
    """Форматирование ошибки валидации для включения названий полей."""
    error_details = {
        "message": e.message,
        "field": e.path
    }
    return error_details

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
        
    @app.route('/es/v1/events/<event_id>', methods=['GET'])
    def get_event(event_id):
        print(event_id)
        """
        Параметры: event_id
        
        GET-операция
        Запрашивает у сервиса и возвращает объект со одной записью с id = event_id
        
        Обрабтка исключения: при отсутствии введенного id в ответ поступает строка с соответствующим сообщением 
        """
        
        try:
            if not event_id.isdigit():
                raise IncorrectIdException('Id должен быть числом')
            
            event = _eventService.findEvent(event_id)
            return jsonify(event)
        except EventNotFoundException as exp:
            logger.error(f"Произошла ошибка при поиске мероприятия с id: {event_id}. Подробности: {exp}")
            return Response(exp.message, status=404)
        except IncorrectIdException as exc:
            logger.error(f"Произошла ошибка при вводе id: {event_id}. Подробности: {exc}")
            return Response(exc.message, status=404)
        
        
    @staticmethod
    @app.route('/es/v1/events/<id>', methods=['DELETE'])
    def delete_event(id):
        """
        Параметры: id
        
        DELETE-операция
        Запрашивает у сервиса и возвращает id удаленного мероприятия
        
        Обрабтка исключения: при отсутствии введенного id в ответ поступает строка с соответствующим сообщением
        """
        try:
            if not id.isdigit():
                raise IncorrectIdException('Id должен быть числом')
            
            _eventService.deleteEvent(id)
            return jsonify(id)
        except IncorrectIdException as exc:
            return Response(exc.message, status=400)
        except EventNotFoundException as exp:
            logger.error(f"Произошла ошибка при поиске мероприятия с id: {id}. Подробности: {exp}")
            return Response(exp.message, status=404)
        
    @staticmethod
    @app.route('/es/v1/events', methods=['POST'])
    def add_event():
        """
        POST-операция
        Добавляет новую запись в таблицу
        
        Возвращает: все записи, вместе с новой, в формате json
        
        При обновлении записи, если она является дубликатом, ответом будет являтся строка, говорящая о том что это дубликат, код ошибки - 409
        """
        try:
            if not request.data:
                return "Вы не ввели данные", 400
            request_data = request.get_json()#получаем тело запроса
            _eventValidator.validate_event(request_data)
                
            event = Event()
            event.eventName = request_data['eventName']
            event.description = request_data['description']
            event.invitees = request_data['invitees']
    
            _eventService.addEvent(event)
            return jsonify({'events': _eventService.findAllEvents()})
        except ValidationError as error:
            # Форматирование ошибки валидации для включения названий полей
            error_details = [format_validation_error(error) for e in error.context] or [format_validation_error(error)]
            logger.error(f'{request_data}\n Произошла ошибка ввода. Подробности: {error_details}')
            return Response(f'Ошибка ввода\nОшибка в поле {error_details[0]["field"]}\n Подробности: {error_details[0]["message"]}')
        except EventDuplicateException as exp:
            logger.error(f"{request_data}\nПроизошла ошибка при добавлении мероприятия. Подробности: {exp}")
            return Response(exp.message, status=409)
    
    
    @staticmethod
    @app.route('/es/v1/events/<id>', methods=['PUT'])
    def update_event(id):
        """
        Параметры: id
        
        PUT-операция
        Обновляет данные для записи с введенным id 
        
        Возвращает: Список всех записей
        
        При обновлении записи, если она является дубликатом, ответом будет являтся строка, говорящая о том что это дубликат, код ошибки - 409
        """
        try:
            if not id.isdigit():
                raise IncorrectIdException('Id должен быть числом')
            
            request_data = request.get_json()
            _eventValidator.validate_event(request_data)
            
            event = Event()
            event.eventName = request_data['eventName']
            event.description = request_data['description']
            event.invitees = request_data['invitees']

        
            _eventService.updateEvent(id, event)
            return jsonify({'events': _eventService.findAllEvents()})
        except IncorrectIdException as exp:
            return Response(exp.message, status=404)
        except ValidationError as error:
            # Форматирование ошибки валидации для включения названий полей
            error_details = [format_validation_error(error) for e in error.context] or [format_validation_error(error)]
            logger.error(f'{request_data}\n Произошла ошибка ввода. Подробности: {error_details}')
            return Response(f'Ошибка ввода\nОшибка в поле {error_details[0]["field"]}\n Подробности: {error_details[0]["message"]}')
        except EventNotFoundException as exp:
            return Response(exp.message, status=404)
        except EventDuplicateException as exp:
            return Response(exp.message, status=409)

