class CalendarDayNotFoundException(Exception):
    """Класс исключения связанный с отсутствием даты с введенным id""" 
    def __init__(self, message):
        self.message = message