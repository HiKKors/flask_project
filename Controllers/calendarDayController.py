from flask import Response
from application import app

from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse

from Models.CalendarDays import CalendarDays
from Services.calendarDaysService import CalendarDayService

from Exceptions.calendarDay_not_found_exception import CalendarDayNotFoundException
from Exceptions.calendarDay_duplicate_exception import CalendarDayDyplicateException

from jsonschema.exceptions import ValidationError
from Validators.calendarDayValidator import CalendarDayValidator

from logger import logger

def format_validation_error(e):
    """Форматирование ошибки валидации для включения названий полей."""
    error_details = {
        "message": e.message,
        "field": e.path
    }
    return error_details

_calendarDayService = CalendarDayService()
_calendarDayValidator = CalendarDayValidator()

class CalendarDayController(Resource):
    """
    Класс контроллер таблицы calendarDay
    Содержит методы для каждой CRUD операции
    """
    @staticmethod
    @app.route('/cds/v1/calendarDays', methods=['GET'])
    def get_calendarDays():
        """
        GET-операция
        Запрашивает у сервиса и возвращает объект со всеми записями в таблице calendarDay
        """
        return jsonify({'calendar_days': _calendarDayService.findAllCalendarDays()})
        
    @app.route('/cds/v1/calendarDays/<int:calendar_day_id>', methods=['GET'])
    def get_calendarDay(calendar_day_id = None):
        """
        Параметры: calendar_day_id
        
        GET-операция
        Запрашивает у сервиса и возвращает объект со одной записью с id = calendar_day_id
        """
        try:
            calendar_day = _calendarDayService.findCalendarDay(calendar_day_id)
            return jsonify(calendar_day.serialize())
        except CalendarDayNotFoundException as exp:
            logger.error(f'Произошла ошибка при поиске календарного дня с id {calendar_day_id}. Подробности: {exp}')
            return Response(exp.message, status=404)
        
        
    @staticmethod
    @app.route('/cds/v1/calendarDays/<int:id>', methods=['DELETE'])
    def delete_calendarDay(id):
        """
        Параметры: id
        
        DELETE-операция
        Запрашивает у сервиса и возвращает id удаленного дня
        """
        try:
            _calendarDayService.deteleCalendarDay(id)
            return jsonify(id)
        except CalendarDayNotFoundException as exp:
            logger.error(f'Произошла ошибка при поиске календарного дня с id {id}. Подробности: {exp}')
            return Response(exp.message, status=404)
        
    @staticmethod
    @app.route('/cds/v1/calendarDays', methods=['POST'])
    def add_calendarDay():
        """
        POST-операция
        Добавляет новую запись в таблицу
        
        Возвращает: все записи, вместе с новой, в формате json
        """
        try:
            request_data = request.get_json()#получаем тело запроса
            print(request_data)
            _calendarDayValidator.validate_calendar_day(request_data)
        
            calendarDay = CalendarDays()
            calendarDay.Date = request_data['Date']
            calendarDay.WeekDay = request_data['WeekDay']
            calendarDay.DayType = request_data['DayType']
        
            _calendarDayService.addCalendarDay(calendarDay)
            
            return jsonify({'calendarDays': _calendarDayService.findAllCalendarDays()})
        except ValidationError as error:
            error_details = [format_validation_error(error) for e in error.context] or [format_validation_error(error)]
            logger.error(f'{request_data}\n Произошла ошибка ввода. Подробности: {error_details}')
            return Response(f'Ошибка ввода\nОшибка в поле {error_details[0]["field"]}\n Подробности: {error_details[0]["message"]}')
        except CalendarDayDyplicateException as exp:
            logger.error(f"{request_data}\nПроизошла ошибка при добавлении календарного дня. Подробности: {exp}")
            return Response(exp.message, status=409)
    
    @staticmethod
    @app.route('/cds/v1/calendarDays/<int:id>', methods=['PUT'])
    def update_calendarDay(id):
        """
        Параметры: id
        
        PUT-операция
        Обновляет данные для записи с введенным id 
        
        Возвращает: Список всех записей
        """
        try:
            request_data = request.get_json()
            _calendarDayValidator.validate_calendar_day(request_data)
            
            calendarDay = CalendarDays()
            calendarDay.Date = request_data['Date']
            calendarDay.WeekDay = request_data['WeekDay']
            calendarDay.DayType = request_data['DayType']

        
            _calendarDayService.updateCalendarDay(id, calendarDay)
            return jsonify({'calendarDays': _calendarDayService.findAllCalendarDays()})
        except ValidationError as error:
            error_details = [format_validation_error(error) for e in error.context] or [format_validation_error(error)]
            logger.error(f'{request_data}\n Произошла ошибка ввода. Подробности: {error_details}')
            return Response(f'Ошибка ввода\nОшибка в поле {error_details[0]["field"]}\n Подробности: {error_details[0]["message"]}')
        except CalendarDayNotFoundException as exp:
            logger.error(f'Ошибка поиска каледнарного дня с id {id}. Подробности: {exp}')
            return Response(exp.message, status=404)
        except CalendarDayDyplicateException as exp:
            return Response(exp.message, status=409)
