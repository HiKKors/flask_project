from application import app, api

from Controllers.calendarDayController import CalendarDayController
from Controllers.eventController import EventControler 

if __name__ == '__main__':
    # добавляем ресурсы
    api.add_resource(CalendarDayController)
    api.add_resource(EventControler)
    app.run(debug=True, port=3000, host="127.0.0.1")