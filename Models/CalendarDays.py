class CalendarDays:
    """
    Класс модели дней
    
    Создаем переменные с дефолтным значением - None, это наши поля таблицы
    """
    id = None
    Date = None
    WeekDay = None
    DayType = None
    
    def __init__(self):
        """
        Затем инициализируем их
        """
        self.id = CalendarDays.id
        self.Date = CalendarDays.Date
        self.WeekDay = CalendarDays.WeekDay
        self.DayType = CalendarDays.DayType
        
    def serialize(self):
        """
        Метод сериализации объекта
        Возвращает объект типа json
        """
        return {
            'id': self.id,
            'Date': self.Date,
            'WeekDay': self.WeekDay,
            'DayType': self.DayType
        }