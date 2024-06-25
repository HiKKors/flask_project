import sqlite3
from Models.CalendarDays import CalendarDays

from Exceptions.calendarDay_not_found_exception import CalendarDayNotFoundException
from Exceptions.calendarDay_duplicate_exception import CalendarDayDyplicateException
from Exceptions.calendarDayIdException import CalendarDayIdException

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
                        Date,
                        WeekDay,
                        DayType
                        FROM calendarDay
                        WHERE id = ?"""

            """Получаем одну запись"""
            raw_day = con.execute(query, (id,)).fetchone()
            if raw_day == None:
                raise CalendarDayNotFoundException(f'Дня с id {id} нет в базе данных')
            
            calendarDay = CalendarDays()
            
            calendarDay.id = raw_day[0]
            calendarDay.Date = raw_day[1]
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
                        Date,
                        WeekDay,
                        DayType
                        FROM calendarDay"""
                        
            raw_day = con.execute(query).fetchall()
            for row in raw_day:
                event = {
                    'id': row[0],
                    'Date': row[1],
                    'WeekDay': row[2],
                    'DayType': row[3]
                }
                calendarDays.append(event)
                
        return calendarDays
    
    def addCalendarDay(self, calendar_object: CalendarDays):
        with con:
            sql_select = """SELECT * FROM calendarDay
            WHERE Date = ? AND WeekDay = ? AND DayType = ?"""
            
            searchResult = con.execute(sql_select, (
                calendar_object.Date,
                calendar_object.WeekDay,
                calendar_object.DayType,
            )).fetchone()
            
            if searchResult is not None:
                raise CalendarDayDyplicateException('Такое календарный день уже есть')
            
            sql_insert = """
            INSERT INTO calendarDay
            (Date, WeekDay, DayType)
            values(?, ?, ?)"""

            con.execute(sql_insert, (
                calendar_object.Date,
                calendar_object.WeekDay,
                calendar_object.DayType
            ))
            
    def deteleCalendarDay(self, id):
        if id <= 0:
            raise CalendarDayIdException('id должен быть больше 0')
        with con:
            sql_select = """SELECT * FROM calendarDay WHERE id = ?"""
            
            raw_calendarDay = con.execute(sql_select, (id,)).fetchone()
            
            if raw_calendarDay == None:
                raise CalendarDayNotFoundException(f'Дня с id {id} нет в базе данных')
            
            sql_delete = """DELETE FROM calendarDay
            WHERE id = ?"""
            
            con.execute(sql_delete, (id,)).fetchone()
            
            
        return id
    
    def updateCalendarDay(self, id, calendar_object: CalendarDays):
        if id <= 0:
            raise CalendarDayIdException('id должен быть больше 0')
        with con:
            raw_calendarDay_id = con.execute("SELECT id FROM calendarDay WHERE id=?", (id,)).fetchone()
            if raw_calendarDay_id == None:
                raise CalendarDayNotFoundException(f'Дня с id {id} нет в базе данных')
            
            sql_update = """
            UPDATE calendarDay
            SET
                Date = ?,
                WeekDay = ?,
                DayType = ?
            WHERE
                id = ?
            """
            
            con.execute(sql_update, (
                calendar_object.Date,
                calendar_object.WeekDay,
                calendar_object.DayType,
                id
            ))
            
    def delete_data(self):
        sql_delete = """DELETE FROM calendarDay"""
        
        with con:
            con.execute(sql_delete)