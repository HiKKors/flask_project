from application import app

from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse

from Models.CalendarDays import CalendarDays
from Services.calendarDaysService import CalendarDayService

_calendarDayService = CalendarDayService()

class CalendarDayController(Resource):
    @staticmethod
    @app.route('/cds/v1/calendarDays', methods=['GET'])
    def get_calendarDays():
        return jsonify({'calendar_days': _calendarDayService.findAllCalendarDays()})
        
    @app.route('/cds/v1/calendarDays/<int:calendar_day_id>', methods=['GET'])
    def get_calendarDay(calendar_day_id = None):
        calendar_day = _calendarDayService.findCalendarDay(calendar_day_id)
        return jsonify(calendar_day.serialize())
        
    @staticmethod
    @app.route('/cds/v1/calendarDays/<int:id>', methods=['DELETE'])
    def delete_calendarDay(id):
        _calendarDayService.deteleCalendarDay(id)
        return jsonify(id)
    
    @staticmethod
    @app.route('/cds/v1/calendarDays', methods=['POST'])
    def add_calendarDay():
        request_data = request.get_json()#получаем тело запроса
        
        calendarDay = CalendarDays()
        calendarDay.WeekDay = request_data['WeekDay']
        calendarDay.DayType = request_data['DayType']

        _calendarDayService.addCalendarDay(calendarDay)

        return jsonify({'calendarDays': _calendarDayService.findAllCalendarDays()})
    
    @staticmethod
    @app.route('/cds/v1/calendarDays/<int:id>', methods=['PUT'])
    def update_calendarDay(id):
        request_data = request.get_json()
        
        calendarDay = CalendarDays()
        calendarDay.WeekDay = request_data['WeekDay']
        calendarDay.DayType = request_data['DayType']

        _calendarDayService.updateCalendarDay(id, calendarDay)

        return jsonify({'calendarDays': _calendarDayService.findAllCalendarDays()})
