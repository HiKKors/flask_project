import json
from jsonschema import validate

class EventValidator:
    def get_schema(self):
        with open('Schemas/eventSchema.json') as f:
            schema = json.load(f)
        return schema
    
    def validate_event(self, eventData):
        schema = self.get_schema()
        validate(instance=eventData, schema=schema)