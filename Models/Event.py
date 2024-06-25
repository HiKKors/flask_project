from dataclasses import dataclass

@dataclass
class Event:
    """
    Класс модели мероприятий
    
    Создаем переменные с дефолтным значением - None
    """
    id: int = None
    eventName: str = None
    description: str = None
    invitees: str = None