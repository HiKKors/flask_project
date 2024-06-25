import sqlite3
from Models.Event import Event
from Models.DayEvent import DayEvent
from Models.CalendarDays import CalendarDays

from Exceptions.calendarDay_not_found_exception import CalendarDayNotFoundException
from Exceptions.event_duplicate_exception import EventDuplicateException


con = sqlite3.connect('db.db', check_same_thread=False)

class DayEventService:
    def findAllDayEvents(self, day_id):
        print(day_id)
        day_events = []
        with con:
            search_day = """
            SELECT * FROM calendarDay
            WHERE id = ?
            """
            raw_day = con.execute(search_day, (day_id, )).fetchone()
            
            if raw_day is None:
                raise CalendarDayNotFoundException('Дня с таким id не найдено')
            
            
            select_query = """
                SELECT e.id, e.eventName, e.description, e.invitees, cd.id, cd.Date, cd.WeekDay, cd.DayType, de.id, de.location, de.startTime, de.endTime, de.program
                FROM event e, calendarDay cd, DayEvent de
                WHERE cd.id = de.DayId AND e.id = de.EventId AND cd.id = ?
            """
            
            raw_events = con.execute(select_query, [day_id]).fetchall()            
            for raw_event in raw_events:
                event = Event(
                    id = raw_event[0],
                    eventName = raw_event[1],
                    description = raw_event[2],
                    invitees = raw_event[3],
                )
                calendarDay = CalendarDays(
                    id = raw_event[4],
                    Date = raw_event[5],
                    WeekDay = raw_event[6],
                    DayType = raw_event[7]
                )
                day_event = DayEvent(
                    id = raw_event[8],
                    DayId = calendarDay,
                    EventId = event,
                    location = raw_event[9],
                    startTime = raw_event[10],
                    endTime = raw_event[11],
                    program = raw_event[12]
                )
                
                day_events.append(day_event)
                
        return day_events
    
    def findOneDayEvent(self, day_id, event_id):
        
        select_query = """
                SELECT e.id, e.eventName, e.description, e.invitees, cd.id, cd.Date, cd.WeekDay, cd.DayType, de.id, de.location, de.startTime, de.endTime, de.program
                FROM event e, calendarDay cd, DayEvent de
                WHERE cd.id = de.DayId AND e.id = de.EventId AND cd.id = ? AND e.id = ?
            """
            
        raw_event = con.execute(select_query, (day_id, event_id, )).fetchone()            
        
        event = Event(
            id = raw_event[0],
            eventName = raw_event[1],
            description = raw_event[2],
            invitees = raw_event[3],
        )
        calendarDay = CalendarDays(
            id = raw_event[4],
            Date = raw_event[5],
            WeekDay = raw_event[6],
            DayType = raw_event[7]
        )
        day_event = DayEvent(
            id = raw_event[8],
            DayId = calendarDay,
            EventId = event,
            location = raw_event[9],
            startTime = raw_event[10],
            endTime = raw_event[11],
            program = raw_event[12]
        )
        
        return day_event
    
    def addDayEvent(self, object: DayEvent):
        with con:
            select_query = """
                SELECT * FROM DayEvent
                WHERE DayId = ? AND EventId = ? AND location = ? AND startTime = ? AND endTime = ? AND program = ?
            """
            
            raw_result = con.execute(select_query, (
                object.DayId,
                object.EventId,
                object.location,
                object.startTime,
                object.endTime,
                object.program
            )).fetchone()
            
            if raw_result is not None:
                raise EventDuplicateException('Такое мероприятие уже есть в этот день')
            
            
            insert_query = """
                INSERT INTO DayEvent(DayId, EventId, location, startTime, endTime, program)
                VALUES(?, ?, ?, ?, ?, ?)
            """
            
            raw = con.execute(insert_query, (
                object.DayId,
                object.EventId,
                object.location,
                object.startTime,
                object.endTime,
                object.program
            ))
        
        
        
    def deleteDayEvent(self, day_id, event_id):
        with con:
            delete_query = """
                DELETE FROM DayEvent
                WHERE DayId = ? AND EventId = ?
            """
        
            con.execute(delete_query, (day_id, event_id, ))
            

    def deleteDayEventData(self):
        with con:
            delete_query = """
                DELETE FROM DayEvent
            """
        