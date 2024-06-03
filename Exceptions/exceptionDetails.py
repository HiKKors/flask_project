from dataclasses import dataclass

@dataclass
class ExceptionDetails:
    type: str = None
    title: str = None
    status: int = None
    detail: str = None
    instance: str = None