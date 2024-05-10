import sqlite3

con =  sqlite3.connect('calendar_days.db')

class Connection:
    def createTable(self):
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
                                WeekDay TEXT,
                                DayType TEXT,
                                FOREIGN KEY (id) REFERENCES event (DateId)
                            );
                        """)
                        
    def insertCalendarData(self):
        sql = """INSERT INTO calendarDay
            (WeekDay, DayType)
            values(?, ?)
            """
            
        data = [('Пятница', 'Будний'),
                ('Четверг', 'Будний'),
                ('Пятница', 'Будний')]
        
        with con:
            con.executemany(sql, data)
            
    def connect(self):
        self.createTable()
        self.insertCalendarData()