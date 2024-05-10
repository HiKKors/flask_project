class CalendarDays:
    id = None
    WeekDay = None
    DayType = None
    
    def __init__(self):
        self.id = CalendarDays.id
        self.WeekDay = CalendarDays.WeekDay
        self.DayType = CalendarDays.DayType
        
    def serialize(self):
        return {
            'id': self.id,
            'WeekDay': self.WeekDay,
            'DayType': self.DayType
        }