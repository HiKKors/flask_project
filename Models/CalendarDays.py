class CalendarDays:
    """
    Класс модели дней
    
    Создаем переменные с дефолтным значением - None, это наши поля таблицы
    """
    id = None
    event_id = None
    WeekDay = None
    DayType = None
    
    def __init__(self):
        """
        Затем инициализируем их
        """
        self.id = CalendarDays.id
        self.event_id = CalendarDays.event_id
        self.WeekDay = CalendarDays.WeekDay
        self.DayType = CalendarDays.DayType
        
    def serialize(self):
        """
        Метод сериализации объекта
        Возвращает объект типа json
        """
        return {
            'id': self.id,
            'event_id': self.event_id,
            'WeekDay': self.WeekDay,
            'DayType': self.DayType
        }