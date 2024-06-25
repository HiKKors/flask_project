from dataclasses import dataclass
from Models.Event import Event
from Models.CalendarDays import CalendarDays

@dataclass
class DayEvent:
    id: int = None
    DayId: CalendarDays = None
    EventId: Event = None
    location: str = None
    startTime: str = None
    endTime: str = None
    program: str = None