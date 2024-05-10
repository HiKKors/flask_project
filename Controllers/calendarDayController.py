from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse

from Models.CalendarDays import CalendarDays
from Services.calendarDaysService import CalendarDayService

app = Flask(__name__)
api = Api()

_calendarDayService = CalendarDayService()

class CalendarDayController(Resource):
    @staticmethod
    @app.route('/cds/v1/calendarDays', methods=['GET'])
    @app.route('/cds/v1/calendarDays/<int:calendar_day_id>', methods=['GET'])
    def get_calendarDays(calendar_day_id = None):
        if calendar_day_id != None:
            calendar_day = _calendarDayService.findCalendarDay(calendar_day_id)
            return jsonify(calendar_day.serialize())
        else:
            return jsonify({'calendar_days': _calendarDayService.findAllCalendarDays()})
        
    @staticmethod
    @app.route('/cds/v1/calendarDays/<int:id>', methods=['DELETE'])
    def delete_calendarDay(id):
        pass
    
    @staticmethod
    @app.route('/cds/v1/calendarDays', methods=['POST'])
    def add_calendarDay():
        pass
    
    @staticmethod
    @app.route('/cds/v1/calendarDays/<int:id>', methods=['PUT'])
    def update_calendarDay(id):
        pass

    def start(self):
        api.init_app(app)
        return app