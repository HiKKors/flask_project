from application import app

from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse

from Models.CalendarDays import CalendarDays
from Services.calendarDaysService import CalendarDayService

_calendarDayService = CalendarDayService()

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
        calendar_day = _calendarDayService.findCalendarDay(calendar_day_id)
        return jsonify(calendar_day.serialize())
        
    @staticmethod
    @app.route('/cds/v1/calendarDays/<int:id>', methods=['DELETE'])
    def delete_calendarDay(id):
        """
        Параметры: id
        
        DELETE-операция
        Запрашивает у сервиса и возвращает id удаленного дня
        """
        _calendarDayService.deteleCalendarDay(id)
        return jsonify(id)
    
    @staticmethod
    @app.route('/cds/v1/calendarDays', methods=['POST'])
    def add_calendarDay():
        """
        POST-операция
        Добавляет новую запись в таблицу
        
        Возвращает: все записи, вместе с новой, в формате json
        """
        request_data = request.get_json()#получаем тело запроса
        
        calendarDay = CalendarDays()
        calendarDay.WeekDay = request_data['WeekDay']
        calendarDay.DayType = request_data['DayType']

        _calendarDayService.addCalendarDay(calendarDay)

        return jsonify({'calendarDays': _calendarDayService.findAllCalendarDays()})
    
    @staticmethod
    @app.route('/cds/v1/calendarDays/<int:id>', methods=['PUT'])
    def update_calendarDay(id):
        """
        Параметры: id
        
        PUT-операция
        Обновляет данные для записи с введенным id 
        
        Возвращает: Список всех записей
        """
        request_data = request.get_json()
        
        calendarDay = CalendarDays()
        calendarDay.WeekDay = request_data['WeekDay']
        calendarDay.DayType = request_data['DayType']

        _calendarDayService.updateCalendarDay(id, calendarDay)

        return jsonify({'calendarDays': _calendarDayService.findAllCalendarDays()})
