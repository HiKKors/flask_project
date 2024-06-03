import json
from jsonschema import validate

class CalendarDayValidator:
    def get_schema(self):
        with open('Schemas/calendarDaySchema.json') as f:
            schema = json.load(f)
        return schema
    
    def validate_calendar_day(self, calendarDayData):
        schema = self.get_schema()
        validate(instance=calendarDayData, schema=schema)