import sqlite3
from Models.Event import Event

con = sqlite3.connect('events.db', check_same_thread=False)


class EventService:
    def findEvent(self, id):
        with con:
            query = """SELECT 
                        id,
                        eventName,
                        description,
                        location,
                        dateId,
                        startTime,
                        endTime,
                        program,
                        invitees
                        FROM events
                        WHERE id = ?"""
        
            raw_event = con.execute(query, (id,)).fetchone()
            event = Event()
            
            event.id = raw_event[0]
            event.EventName = raw_event[1]
            event.Description = raw_event[2]
            event.Location = raw_event[3]
            event.DateId = raw_event[4]
            event.StartTime = raw_event[5]
            event.EndTime = raw_event[6]
            event.Program = raw_event[7]
            event.Invitees = raw_event[8]
    
        return event
        
    def findAllEvents(self):
        events = []
        with con:
            query = """SELECT
                        id,
                        eventName,
                        description,
                        location,
                        dateId,
                        startTime,
                        endTime,
                        program,
                        invitees
                        FROM events"""
                        
            raw_events = con.execute(query).fetchall()
            for row in raw_events:
                event = {
                    'id': row[0],
                    'eventName': row[1],
                    'description': row[2],
                    'location': row[3],
                    'dateId': row[4],
                    'startTime': row[5],
                    'endTime': row[6],
                    'program': row[7],
                    'invitees': row[8]
                }
                events.append(event)
                
        return events