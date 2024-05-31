class Event:
    """
    Класс модели мероприятий
    
    Создаем переменные с дефолтным значением - None
    """
    id = None
    eventName = None
    description = None
    location = None
    date = None
    startTime = None
    endTime = None
    program = None
    invitees = None
    
    def __init__(self):
        """
        Затем инициализируем их
        """
        self.id = Event.id
        self.eventName = Event.eventName
        self.description = Event.description
        self.location = Event.location
        self.date = Event.date
        self.startTime = Event.startTime
        self.endTime = Event.endTime
        self.program = Event.program
        self.invitees = Event.invitees
        
    def serialize(self):
        """
        Метод сериализации объекта
        Возвращает объект типа json
        """
        return {
            'id': self.id,
            'eventName': self.eventName,
            'description': self.description,
            'location': self.location,
            'date': self.date,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'program': self.program,
            'invitees': self.invitees
        }
    