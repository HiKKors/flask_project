import sqlite3

con = sqlite3.connect('event.db')

class Connection:
    def createTable(self):
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
                                dateId INTEGER,
                                startTime INTEGER NOT NULL,
                                endTime INTEGER NOT NULL,
                                program TEXT,
                                invitees TEXT
                            );
                        """)
                        
    def insertEventData(self):
        sql = """INSERT INTO event
            (eventName, description, location, dateId, startTime, endTime, program, invitees)
            values(?, ?, ?, ?, ?, ?, ?, ?)
            """
            
        data = [
            ('День космонавтики', 
             'Праздник Дня Космонавтики: Откройте Вселенную вместе с нами! Присоединяйтесь к увлекательным мероприятиям, посвященным освоению космоса и достижениям человечества в космических исследованиях.', 
             'Площадь Ленина', 
             '1', 
             '09:00:00',
             '20:00:00',
             'Открытие, конкурс, шоу',
             'Иванов, Петров, Киселев'),
            ('День Победы',
             'Мероприятие в честь Дня Победы: Память и Почитание',
             'Ул. Ленина',
             '2',
             '10:00:00',
             '12:00:00',
             'Парад Победы, Бессмертный полк',
             'Зубков, Крылов, Морозов')
        ]

        with con:
            con.executemany(sql, data)
            
            
    def connect(self):
        self.createTable()
        self.insertEventData()