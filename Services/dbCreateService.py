import sqlite3

con =  sqlite3.connect('db.db')

class Connection:
    def createTableCalendarDays(self):
        """Создает таблицу calendarDay"""
        with con:
            data = con.execute("""
                select count(*)
                from sqlite_master
                where
                type='table' and name='calendarDay';
            """)
            
            for row in data:
                if row[0] == 0:
                    with con:
                        con.execute("""
                            CREATE TABLE IF NOT EXISTS calendarDay (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Date TEXT NOT NULL,
                                WeekDay TEXT,
                                DayType TEXT
                            );
                        """)
                        
    def insertCalendarData(self):
        """Заполняет таблицу тестовыми данными"""
        sql = """INSERT INTO calendarDay
            (Date, WeekDay, DayType)
            values(?, ?, ?)
            """
            
        data = [('2024-04-12', 'Пятница', 'Будний'),
                ('2024-04-13', 'Суббота', 'Выходной'),
                ('2024-05-09', 'Четверг', 'Будний'),]
        
        with con:
            con.executemany(sql, data)
            
    def createEventTable(self):
        """Создает таблицу мероприятий"""
        with con:
            data = con.execute("""
                select count(*)
                from sqlite_master
                where
                type='table' and name='event';
            """)
            
            for row in data:
                if row[0] == 0:
                    with con:
                        con.execute("""
                            CREATE TABLE IF NOT EXISTS event (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                eventName TEXT,
                                description TEXT,
                                invitees TEXT
                            );
                        """)
                        
    def insertEventData(self):
        """Заполняет тестовыми данными"""
        sql = """INSERT INTO event
            (eventName, description, invitees)
            values(?, ?, ?)
            """
        
        """тестовые данные"""
        data = [
            ('День космонавтики', 
             'Праздник Дня Космонавтики: Откройте Вселенную вместе с нами! Присоединяйтесь к увлекательным мероприятиям, посвященным освоению космоса и достижениям человечества в космических исследованиях.', 
             'Иванов, Петров, Киселев'),
            ('День Победы',
             'Мероприятие в честь Дня Победы: Память и Почитание',
             'Зубков, Крылов, Морозов')
        ]

        with con:
            """соединение данных и запроса"""
            con.executemany(sql, data)
            
            
            
    def createDayEventTable(self):
        with con:
            data = con.execute("""
                select count(*)
                from sqlite_master
                where
                type='table' and name='DayEvent';
            """)
            
            for row in data:
                if row[0] == 0:
                    with con:
                        con.execute("""
                            CREATE TABLE IF NOT EXISTS DayEvent (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                DayId INTEGER NOT NULL,
                                EventId INTEGER NOT NULL,
                                location TEXT,
                                startTime TEXT, 
                                endTime TEXT,
                                program TEXT,
                                FOREIGN KEY (DayId) REFERENCES calendarDay(id) ON DELETE CASCADE,
                                FOREIGN KEY (EventId) REFERENCES event(id) ON DELETE CASCADE
                            )
                        """)
        
    def insertDayEventData(self):
        sql_insert = """
            INSERT INTO DayEvent (DayId, EventId, location, startTime, endTime, program) 
            VALUES(
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """
        
        data = [
            (
                1, 1, 'Ул. Ленина', '10:00', '16:00', 'Открытие, Космическая ярмарка, Научный квест "В поисках новых планет"'
            ),
            (
                2, 1, 'Ул. Ленина', '15:00', '22:00', 'Космический кинозал, Лекции и дискуссии, Звездная ночь, Завершение'
            ),
            (
                3, 2, 'Площадь Ленина', '09:00', '12:00', 'Построение Парадного расчета, Прохождение, Бессметрный полк'
            )
        ]
        
        with con:
            """соединение данных и запроса"""
            con.executemany(sql_insert, data)
            
    def drop_event(self):
        sql_drop = """DROP TABLE event"""
        
        with con:
            con.execute(sql_drop)
            
    def drop_calendarDay(self):
        sql_drop = """DROP TABLE calendarDay"""
        
        with con:
            con.execute(sql_drop)
            
    def drop_dayEvent(self):
        sql_drop = """DROP TABLE DayEvent"""
        
        with con:
            con.execute(sql_drop)
        
    def connect(self):
        self.createTableCalendarDays()
        self.insertCalendarData()
        self.createEventTable()
        self.insertEventData()
        self.createDayEventTable()
        self.insertDayEventData()