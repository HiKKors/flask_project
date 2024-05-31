class EventNotFoundException(Exception):
    """Класс исключения связанный с отсутствием мероприятия с введенным id""" 
    def __init__(self, message):
        self.message = message