"""
Главный файл
Здесь добавляются новые ресурсы (таблицы базы данных)
Указываются параметры сервера
"""
from application import app, api

from Controllers.calendarDayController import CalendarDayController
from Controllers.eventController import EventControler 
from Controllers.dayEventsController import DayEventsController

if __name__ == '__main__':
    api.add_resource(CalendarDayController)
    api.add_resource(EventControler)
    api.add_resource(DayEventsController)
    app.run(debug=True, port=3000, host="127.0.0.1")