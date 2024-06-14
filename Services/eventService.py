import sqlite3
from Models.Event import Event

from Exceptions.event_not_found_exception import EventNotFoundException
from Exceptions.event_duplicate_exception import EventDuplicateException
from Exceptions.EventIdException import EventIdException
from Exceptions.date_not_found_exception import DateNotFoundException

con = sqlite3.connect('db.db', check_same_thread=False)

class EventService:
    def findEvent(self, id):
        if id <= 0:
            raise EventIdException('id должен быть больше 0')
        """
        Параметры: id нужного мероприятия
        Возвращает: мероприятие с введенным id (формат: json)
        """
        
        with con:
            query = """SELECT 
                        id,
                        eventName,
                        description,
                        location,
                        DateId,
                        startTime,
                        endTime,
                        program,
                        invitees
                        FROM event
                        WHERE id = ?"""

            """Получаем одну запись"""
            raw_event = con.execute(query, (id,)).fetchone() 
            """Если ничего не найдено вызываем ошибку"""
            if raw_event == None:
                raise EventNotFoundException(f'Мероприятие с id {id} не найдено')
            
            event = Event()
            
            event.id = raw_event[0]
            event.eventName = raw_event[1]
            event.description = raw_event[2]
            event.location = raw_event[3]
            event.DateId = raw_event[4]
            event.startTime = raw_event[5]
            event.endTime = raw_event[6]
            event.program = raw_event[7]
            event.invitees = raw_event[8]
    
        return event
        
    def findAllEvents(self):
        """
        Возвращает: Все записи из таблицы event в формате json
        
        Создается список со всеми мероприятиями
        С помощью fetchall получаем все записи из таблицы
        Проходимся циклом по полученному списку
        Создаем объект с данными об одном мероприятии
        Добавляем объект в список со всеми записями 
        """
        events = []
        with con:
            query = """SELECT
                        id,
                        eventName,
                        description,
                        location,
                        DateId,
                        startTime,
                        endTime,
                        program,
                        invitees
                        FROM event"""
            
            raw_events = con.execute(query).fetchall()

            for row in raw_events:
                event = {
                    'id': row[0],
                    'eventName': row[1],
                    'description': row[2],
                    'location': row[3],
                    'DateId': row[4],
                    'startTime': row[5],
                    'endTime': row[6],
                    'program': row[7],
                    'invitees': row[8]
                }
                events.append(event)
        
        return events
    
    def addEvent(self, event_object: Event):        
        """Параметры: ожидаемый тип данных"""
        date_id = event_object.DateId
        with con:
            sql_find_date = """SELECT * FROM calendarDay
            WHERE id = ?"""
            dateResult = con.execute(sql_find_date, (date_id,)).fetchone()
            
            if dateResult == None:
                raise DateNotFoundException(f'День с id {date_id} не найден')
                
            
            sql_select = """SELECT * FROM event
            WHERE eventName = ? AND description = ? AND location = ? AND DateId = ? AND startTime = ? AND endTime = ? AND program = ? AND invitees = ?"""
            
            searchResult = con.execute(sql_select, (
                event_object.eventName,
                event_object.description,
                event_object.location,
                event_object.DateId,
                event_object.startTime,
                event_object.endTime,
                event_object.program,
                event_object.invitees
            )).fetchone()
            
            if searchResult is not None:
                raise EventDuplicateException('Такое мероприятие уже есть')
            
            sql_insert = """
            INSERT INTO event
            (eventName, description, location, DateId, startTime, endTime, program, invitees)
            values(?, ?, ?, ?, ?, ?, ?, ?)"""
            raw_event = con.execute(sql_insert, (
                event_object.eventName,
                event_object.description,
                event_object.location,
                event_object.DateId,
                event_object.startTime,
                event_object.endTime,
                event_object.program,
                event_object.invitees
            ))
            
            print('НОВЫЙ ОБЪЕКТ:',raw_event)
            con.execute(sql_insert, (
                event_object.eventName,
                event_object.description,
                event_object.location,
                event_object.DateId,
                event_object.startTime,
                event_object.endTime,
                event_object.program,
                event_object.invitees
            ))
            
    def deleteEvent(self, id):
        if id <= 0:
            raise EventIdException('id должен быть больше 0')
        """
        Параметры: id мероприятия, которое хотим удалить
        Возвращает: id удаленного мероприятия
        """
        with con:
            sql_select = """SELECT * FROM event WHERE id = ?"""
            raw_event = con.execute(sql_select, (id,)).fetchone()
            
            sql_delete = """DELETE FROM event
            WHERE id = ?"""
            
            if raw_event == None:
                raise EventNotFoundException(f'Мероприятие с id {id} не найдено')
            else:
                raw_event = con.execute(sql_delete, (id,))
                return id
    
    def delete_data(self):
        with con:
            sql_delete = """DELETE FROM event"""
            
            raw_event = con.execute(sql_delete)
    
    def updateEvent(self, id, event_object: Event):
        if id <= 0:
            raise EventIdException('id должен быть больше 0')
        """в con.execute кроме всех полей прописываем id, так как для изменения записи нужны все поля"""
        with con:
            sql_select = """SELECT * FROM event
            WhERE eventName = ? AND description = ? AND location = ? AND DateId = ? AND startTime = ? AND endTime = ? AND program = ? AND invitees = ?"""
            
            searchResult = con.execute(sql_select, (
                event_object.eventName,
                event_object.description,
                event_object.location,
                event_object.DateId,
                event_object.startTime,
                event_object.endTime,
                event_object.program,
                event_object.invitees
            )).fetchone()
            
            if searchResult is not None:
                raise EventDuplicateException('Такое мероприятие уже есть')
            
            raw_event_id = con.execute("""SELECT id FROM event WHERE id = ?""", (id,)).fetchone()
            if raw_event_id == None:
                raise EventNotFoundException(f'Мероприятие с id {id} не найдено')   
            
            sql_update = """
            UPDATE event
            SET
                eventName = ?,
                description = ?,
                location = ?,
                DateId = ?,
                startTime = ?,
                endTime = ?,
                program = ?,
                invitees = ?
            WHERE
                id = ?
            """
            
            con.execute(sql_update, (
                event_object.eventName,
                event_object.description,
                event_object.location,
                event_object.DateId,
                event_object.startTime,
                event_object.endTime,
                event_object.program,
                event_object.invitees,
                id
            ))
        