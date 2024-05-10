import sqlite3
from Models.CalendarDays import CalendarDays

con = sqlite3.connect('calendar_days.db', check_same_thread=False)


class CalendarDayService:
    def findCalendarDay(self, id):
        with con:
            query = """SELECT 
                        id,
                        WeekDay,
                        DayType
                        FROM calendarDay
                        WHERE id = ?"""
        
            raw_day = con.execute(query, (id,)).fetchone()
            calendarDay = CalendarDays()
            
            calendarDay.id = raw_day[0]
            calendarDay.WeekDay = raw_day[1]
            calendarDay.DayType = raw_day[2]
    
        return calendarDay
        
    def findAllCalendarDays(self):
        calendarDays = []
        with con:
            query = """SELECT
                        id,
                        WeekDay,
                        DayType
                        FROM calendarDay"""
                        
            raw_day = con.execute(query).fetchall()
            for row in raw_day:
                event = {
                    'id': row[0],
                    'WeekDay': row[1],
                    'DatType': row[2]
                }
                calendarDays.append(event)
                
        return calendarDays