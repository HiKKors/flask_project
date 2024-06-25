from dataclasses import dataclass

@dataclass
class DayEventsDo:
    id: int = None
    eventName: str = None
    description: str = None
    invitees: str = None