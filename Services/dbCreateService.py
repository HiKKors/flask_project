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
                                location TEXT,
                                DateId INTEGER NOT NULL,
                                startTime INTEGER NOT NULL,
                                endTime INTEGER NOT NULL,
                                program TEXT,
                                invitees TEXT,
                                FOREIGN KEY (DateId) REFERENCES calendarDay (id)
                            );
                        """)
                        
    def insertEventData(self):
        """Заполняет тестовыми данными"""
        sql = """INSERT INTO event
            (eventName, description, location, DateId, startTime, endTime, program, invitees)
            values(?, ?, ?, ?, ?, ?, ?, ?)
            """
        
        """тестовые данные"""
        data = [
            ('День космонавтики', 
             'Праздник Дня Космонавтики: Откройте Вселенную вместе с нами! Присоединяйтесь к увлекательным мероприятиям, посвященным освоению космоса и достижениям человечества в космических исследованиях.', 
             'Площадь Ленина', 
             1,
             '09:00',
             '20:00',
             'Открытие, конкурс, шоу',
             'Иванов, Петров, Киселев'),
            ('День Победы',
             'Мероприятие в честь Дня Победы: Память и Почитание',
             'Ул. Ленина',
             2,
             '10:00',
             '12:00',
             'Парад Победы, Бессмертный полк',
             'Зубков, Крылов, Морозов')
        ]

        with con:
            """соединение данных и запроса"""
            con.executemany(sql, data)
            
    def drop_event(self):
        sql_drop = """DROP TABLE event"""
        
        with con:
            con.execute(sql_drop)
            
    def drop_calendarDay(self):
        sql_drop = """DROP TABLE calendarDay"""
        
        with con:
            con.execute(sql_drop)
        
    def connect(self):
        self.createTableCalendarDays()
        self.insertCalendarData()
        self.createEventTable()
        self.insertEventData()