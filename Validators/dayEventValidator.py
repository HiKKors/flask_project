import json
from jsonschema import validate

class DayEventValidator:
    def get_schema(self):
        with open('Schemas/dayEventSchema.json') as f:
            schema = json.load(f)
        return schema
    
    def validate_day_event(self, dayEventData):
        schema = self.get_schema()
        validate(instance=dayEventData, schema=schema)