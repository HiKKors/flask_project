"""
Главный файл
Здесь добавляются новые ресурсы (таблицы базы данных)
Указываются параметры сервера
"""
# from application import app, api

# from Controllers.calendarDayController import CalendarDayController
# from Controllers.eventController import EventControler 

# if __name__ == '__main__':
#     api.add_resource(CalendarDayController)
#     api.add_resource(EventControler)
#     app.run(debug=True, port=3000, host="127.0.0.1")
    
    
# КОД ДЛЯ СОЗДАНИЯ БАЗЫ ДАННЫХ

from Services.dbCreateService import Connection
if __name__ == "__main__":
    con = Connection()
    con.connect()
