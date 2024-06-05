from dataclasses import dataclass

@dataclass
class CalendarDays:
    """
    Класс модели дней
    
    Создаем переменные с дефолтным значением - None, это наши поля таблицы
    """
    id: int = None
    Date: str = None
    WeekDay: str = None
    DayType: str = None