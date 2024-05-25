import sqlite3
from Models.CalendarDays import CalendarDays

from Exceptions.calendarDay_not_found_exception import CalendarDayNotFoundException

con = sqlite3.connect('db.db', check_same_thread=False)


class CalendarDayService:
    def findCalendarDay(self, id):
        """
        Параметры: id нужного дня
        Возвращает: данные о дне с введенным id (формат: json)
        """
        with con:
            query = """SELECT 
                        id,
                        event_id,
                        WeekDay,
                        DayType
                        FROM calendarDay
                        WHERE id = ?"""

            """Получаем одну запись"""
            raw_day = con.execute(query, (id,)).fetchone()
            if raw_day == None:
                raise CalendarDayNotFoundException('В этот день нет никаких мероприятий')
            
            calendarDay = CalendarDays()
            
            calendarDay.id = raw_day[0]
            calendarDay.event_id = raw_day[1]
            calendarDay.WeekDay = raw_day[2]
            calendarDay.DayType = raw_day[3]
    
        return calendarDay
        
    def findAllCalendarDays(self):
        """
        Возвращает: все записи из таблицы calendarDay в формате json
        
        Создается список со всеми днями
        С помощью fetchall получаем все записи из таблицы
        Проходимся циклом по полученному списку
        Создаем объект с данными об одном дне
        Добавляем в список со всеми записями 
        """
        calendarDays = []
        with con:
            query = """SELECT
                        id,
                        event_id,
                        WeekDay,
                        DayType
                        FROM calendarDay"""
                        
            raw_day = con.execute(query).fetchall()
            for row in raw_day:
                event = {
                    'id': row[0],
                    'event_id': row[1],
                    'WeekDay': row[2],
                    'DayType': row[3]
                }
                calendarDays.append(event)
                
        return calendarDays
    
    def addCalendarDay(self, calendar_object: CalendarDays):
        with con:
            sql_insert = """
            INSERT INTO calendarDay
            (event_id, WeekDay, DayType)
            values(?, ?, ?)"""

            con.execute(sql_insert, (
                calendar_object.event_id,
                calendar_object.WeekDay,
                calendar_object.DayType
            ))
            
    def deteleCalendarDay(self, id):
        with con:
            sql_delete = """DELETE FROM calendarDay
            WHERE id = ?"""
            
            raw_calendarDay = con.execute(sql_delete, (id,)).fetchone()
            if raw_calendarDay == None:
                raise CalendarDayNotFoundException(f'Даты с id {id} не найдено')
            
        return id
    
    def updateCalendarDay(self, id, calendar_object: CalendarDays):
        with con:
            raw_calendarDay_id = con.execute("SELECT id FROM calendarDay WHERE id=?", (id,)).fetchone()
            if raw_calendarDay_id == None:
                raise CalendarDayNotFoundException(f'Даты с id {id} не найдено')
            
            sql_update = """
            UPDATE calendarDay
            SET
                event_id = ?,
                WeekDay = ?,
                DayType = ?
            WHERE
                id = ?
            """
            
            con.execute(sql_update, (
                calendar_object.event_id,
                calendar_object.WeekDay,
                calendar_object.DayType,
                id
            ))