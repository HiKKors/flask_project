from flask import Flask
# from Controllers.calendarDayController import calendarDay_api
# from Controllers.eventController import event_api
from Models.Event import Event
from Services.Eventdb import Connection

from Controllers.eventController import EventControler


if __name__ == "__main__": 
    controller = EventControler()
    service = controller.start()
    service.run(debug=True, port=3000, host='127.0.0.1')



# app = Flask(__name__)

# app.register_blueprint(calendarDay_api)
# app.register_blueprint(event_api)

# if __name__ == '__main__':
#     app.run(debug=True, port=3000, host='127.0.0.1')