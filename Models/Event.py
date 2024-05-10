class Event:
    id = None
    eventName = None
    description = None
    location = None
    dateId = None
    startTime = None
    endTime = None
    program = None
    invitees = None
    
    def __init__(self):
        self.id = Event.id
        self.eventName = Event.eventName
        self.description = Event.description
        self.location = Event.location
        self.dateId = Event.dateId
        self.startTime = Event.startTime
        self.endTime = Event.endTime
        self.program = Event.program
        self.invitees = Event.invitees
        
    def serialize(self):
        return {
            'id': self.id,
            'eventName': self.eventName,
            'description': self.description,
            'location': self.location,
            'dateId': self.dateId,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'program': self.program,
            'invitees': self.invitees
        }
    