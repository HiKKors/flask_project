from flask import Response
from application import app

from flask import jsonify, request
from flask_restful import Resource

from Models.DayEvent import DayEvent

from Models.Transfer.DayEventsDo import DayEventsDo

from Services.dayEventService import DayEventService
from Services.eventService import EventService
from Services.calendarDaysService import CalendarDayService

from Exceptions.calendarDay_not_found_exception import CalendarDayNotFoundException
from Exceptions.event_not_found_exception import EventNotFoundException
from Exceptions.empty_query_exception import EmptyQueryException
from Exceptions.IncorrectIdException import IncorrectIdException
from Exceptions.event_duplicate_exception import EventDuplicateException

from logger import logger

from jsonschema.exceptions import ValidationError
from Validators.dayEventValidator import DayEventValidator

_dayEventValidator = DayEventValidator()

_eventService = EventService()
_calendarDayService = CalendarDayService()
_dayEventService = DayEventService()

def format_validation_error(e):
    """Форматирование ошибки валидации для включения названий полей."""
    error_details = {
        "message": e.message,
        "field": e.path
    }
    return error_details

class DayEventsController(Resource):
    @staticmethod
    @app.route('/des/v1/calendarDay/<day_id>/events', methods = ['GET'])
    def get_day_events(day_id):
        try:
            if day_id.isdigit() == False:
                raise IncorrectIdException('id должен быть числом')
            
            _calendarDayService.findCalendarDay(day_id)
            
            day_events = []
            raw = _dayEventService.findAllDayEvents(day_id)
            
            date = raw[0].DayId.Date
            
            for item in raw:
                day_event_do = DayEventsDo(
                    id = item.EventId.id,
                    eventName = item.EventId.eventName,
                    description = item.EventId.description,
                    invitees = item.EventId.invitees
                    
                )
                day_events.append(day_event_do)
                
            return jsonify({date: day_events})
        except CalendarDayNotFoundException as exp:
            logger.error(f'Произошла ошибка при поиске календарного дня с id {day_id}. Подробности: {exp}')
            return Response(exp.message, status=404)
        except IncorrectIdException as exp:
            logger.error(f'Произошла ошибка при вводе id {day_id}. Подробности: {exp}')
            return Response(exp.message, status=404)
        
        
    @staticmethod
    @app.route('/des/v1/calendarDay/<day_id>/events/<event_id>', methods = ['GET'])  
    def get_day_event(day_id, event_id):
        try:
            if day_id.isdigit() == False or event_id.isdigit() == False:
                raise IncorrectIdException('все id должны быть числом')
            
            _calendarDayService.findCalendarDay(day_id)
            _eventService.findEvent(event_id)
            
            raw = _dayEventService.findOneDayEvent(day_id, event_id)
            
            date = raw.DayId.Date
            
            if raw == None:
                raise EmptyQueryException('Запрос не должен быть пустым')
            day_event_do = DayEventsDo(
                id = raw.EventId.id,
                eventName = raw.EventId.eventName,
                description = raw.EventId.description,
                invitees = raw.EventId.invitees  
            )
                
            return jsonify({date: day_event_do})
        except CalendarDayNotFoundException as exp:
            logger.error(f'Произошла ошибка при поиске календарного дня с id {day_id}. Подробности: {exp}')
            return Response(exp.message, status=404)
        except EventNotFoundException as exp:
            logger.error(f'Произошла ошибка при поиске мероприятия с id {day_id}. Подробности: {exp}')
            return Response(exp.message, status=404)
        except EmptyQueryException as exp:
            logger.error(f'Произошла ошибка при добавлении мероприятия. Подробности: {exp}')
            return Response(exp.message, status=400)
        except IncorrectIdException as exp:
            logger.error(f'Произошла ошибка при вводе id. Подробности: {exp}')
            return Response(exp.message, status=404)
        
    @staticmethod    
    @app.route('/des/v1/calendarDay/events', methods=['POST'])
    def add_day_event():
        try:
            data = request.get_json()
            _dayEventValidator.validate_day_event(data)
            
            dayEvent = DayEvent()
            dayEvent.DayId = data['DayId']
            dayEvent.EventId = data['EventId']
            dayEvent.location = data['location']
            dayEvent.startTime = data['startTime']
            dayEvent.endTime = data['endTime']
            dayEvent.program = data['program']
            
            _eventService.findEvent(data['EventId'])
            _calendarDayService.findCalendarDay(data['EventId'])
            _dayEventService.addDayEvent(dayEvent)    
            
            day_events = []
            
            raw = _dayEventService.findAllDayEvents(data['DayId'])
                
            date = raw[0].DayId.Date
            
            for item in raw:
                day_event_do = DayEventsDo(
                    id = item.EventId.id,
                    eventName = item.EventId.eventName,
                    description = item.EventId.description,
                    invitees = item.EventId.invitees
                    
                )
                day_events.append(day_event_do)
                
            return jsonify({date: day_events})
        except ValidationError as error:
            # Форматирование ошибки валидации для включения названий полей
            error_details = [format_validation_error(error) for e in error.context] or [format_validation_error(error)]
            logger.error(f'{data}\n Произошла ошибка ввода. Подробности: {error_details}')
            return Response(f'Ошибка ввода\nОшибка в поле {error_details[0]["field"]}\n Подробности: {error_details[0]["message"]}')
        except CalendarDayNotFoundException as exp:
            logger.error(f'Произошла ошибка при поиске календарного дня с id {data["DayId"]}. Подробности: {exp}')
            return Response(exp.message, status=404)
        except EventNotFoundException as exp:
            logger.error(f'Произошла ошибка при поиске мероприятия с id {data["EventId"]}. Подробности: {exp}')
            return Response(exp.message, status=404)
        except EventDuplicateException as exp:
            logger.error(f'Произошла ошибка при добавлении мероприятия. Подробности {exp}')
            return Response(exp.message, status=409)
    
    @staticmethod
    @app.route('/des/v1/calendarDay/<day_id>/events/<event_id>', methods = ['DELETE'])
    def delete_day_event(day_id, event_id):
        try:
            if day_id.isdigit() == False or event_id.isdigit() == False:
                raise IncorrectIdException('все id должны быть числом')
            
            _calendarDayService.findCalendarDay(day_id)
            _eventService.findEvent(event_id)
            
            _dayEventService.deleteDayEvent(day_id, event_id)
            
            return jsonify(event_id)
        except CalendarDayNotFoundException as exp:
            logger.error(f'Произошла ошибка при поиске календарного дня с id {day_id}. Подробности: {exp}')
            return Response(exp.message, status=404)
        except EventNotFoundException as exp:
            logger.error(f'Произошла ошибка при поиске мероприятия с id {event_id}. Подробности: {exp}')
            return Response(exp.message, status=404)
        except IncorrectIdException as exp:
            logger.error(f'Произошла ошибка при вводе id. Подробности: {exp}')
            return Response(exp.message, status=404)