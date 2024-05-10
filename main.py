# from Controllers.calendarDayController import CalendarDayController
# if __name__ == "__main__":
#     controller = CalendarDayController()
#     service = controller.start()
#     service.run(debug=True, port=3000, host="127.0.0.1")

from Controllers.eventController import EventControler
if __name__ == "__main__":
    controller = EventControler()
    service = controller.start()
    service.run(debug=True, port=3000, host="127.0.0.1")

# from Models.CalendarDays import CalendarDays
# from Services.CalendarDaysdb import Connection
# if __name__ == "__main__":
#     con = Connection()
#     con.connect()
