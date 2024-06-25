import pytest

from Models.DayEvent import DayEvent

from Services.dbCreateService import Connection
from Services.dayEventService import DayEventService

con = Connection()

_dayEventService = DayEventService()

def recreate_table():
    con.drop_dayEvent()
    con.createDayEventTable()
    con.insertDayEventData()
    
def recreate_empty_table():
    con.drop_dayEvent()
    con.createDayEventTable()

def test_get_one_day_event_correct_1():
    recreate_table()
    
    dayEvent = DayEvent(
        DayId=1,
        EventId=1,
        location='Ул. Ленина',
        startTime='10:00',
        endTime='16:00',
        program='Открытие, Космическая ярмарка, Научный квест "В поисках новых планет"'
    )
    
    res_dayEvent = _dayEventService.findOneDayEvent(day_id=1, event_id=1)
    
    assert(
        res_dayEvent.DayId.id == dayEvent.DayId
        and res_dayEvent.EventId.id == dayEvent.EventId
        and res_dayEvent.location == dayEvent.location
        and res_dayEvent.startTime == dayEvent.startTime
        and res_dayEvent.endTime == dayEvent.endTime
        and res_dayEvent.program == dayEvent.program
    )
    
def test_get_one_day_event_correct_2():
    recreate_table()
    
    dayEvent = DayEvent(
        DayId=3,
        EventId=2,
        location='Площадь Ленина',
        startTime='09:00',
        endTime='12:00',
        program='Построение Парадного расчета, Прохождение, Бессметрный полк'
    )
    
    res_dayEvent = _dayEventService.findOneDayEvent(day_id=3, event_id=2)
    
    assert(
        res_dayEvent.DayId.id == dayEvent.DayId
        and res_dayEvent.EventId.id == dayEvent.EventId
        and res_dayEvent.location == dayEvent.location
        and res_dayEvent.startTime == dayEvent.startTime
        and res_dayEvent.endTime == dayEvent.endTime
        and res_dayEvent.program == dayEvent.program
    )
    
def test_get_one_day_event_failed_1():
    recreate_table()
    
    dayEvent = DayEvent(
        DayId=1,
        EventId=1,
        location='Ул. Ленина',
        startTime='10:00',
        endTime='16:00',
        program='Открытие, Космическая ярмарка, Научный квест '
    )
    
    res_dayEvent = _dayEventService.findOneDayEvent(day_id=1, event_id=1)
    
    assert(
        res_dayEvent.DayId.id == dayEvent.DayId
        and res_dayEvent.EventId.id == dayEvent.EventId
        and res_dayEvent.location == dayEvent.location
        and res_dayEvent.startTime == dayEvent.startTime
        and res_dayEvent.endTime == dayEvent.endTime
        and res_dayEvent.program == dayEvent.program
    )
    
def test_get_one_day_event_failed_2():
    recreate_table()
    
    dayEvent = DayEvent(
        DayId=3,
        EventId=2,
        location='Площадь Ленина',
        startTime='11:00',
        endTime='12:00',
        program='Построение Парадного расчета, Прохождение, Бессметрный полк'
    )
    
    res_dayEvent = _dayEventService.findOneDayEvent(day_id=3, event_id=2)
    
    assert(
        res_dayEvent.DayId.id == dayEvent.DayId
        and res_dayEvent.EventId.id == dayEvent.EventId
        and res_dayEvent.location == dayEvent.location
        and res_dayEvent.startTime == dayEvent.startTime
        and res_dayEvent.endTime == dayEvent.endTime
        and res_dayEvent.program == dayEvent.program
    )
    
def test_add_day_event_correct_1():
    recreate_empty_table()
    
    new_dayEvent = DayEvent(
        DayId=1,
        EventId=1,
        location='Ул. Ленина',
        startTime='10:00',
        endTime='16:00',
        program='Открытие, Космическая ярмарка, Научный квест "В поисках новых планет"'
    )
    
    initial_day_events_count = len(_dayEventService.findAllDayEvents(day_id=1))
    
    _dayEventService.addDayEvent(new_dayEvent)
    
    current_day_events_count = len(_dayEventService.findAllDayEvents(day_id=1))
    
    assert current_day_events_count == initial_day_events_count + 1
    
def test_add_day_event_correct_2():
    recreate_empty_table()
    
    new_dayEvent = DayEvent(
        DayId=3,
        EventId=2,
        location='Площадь Ленина',
        startTime='09:00',
        endTime='12:00',
        program='Построение Парадного расчета, Прохождение, Бессметрный полк'
    )
    
    initial_day_events_count = len(_dayEventService.findAllDayEvents(day_id=3))
    
    _dayEventService.addDayEvent(new_dayEvent)
    
    current_day_events_count = len(_dayEventService.findAllDayEvents(day_id=3))
    
    assert current_day_events_count == initial_day_events_count + 1
    
    
def test_add_day_event_failed_duplicate():
    recreate_table()
    
    new_dayEvent = DayEvent(
        DayId=3,
        EventId=2,
        location='Площадь Ленина',
        startTime='09:00',
        endTime='12:00',
        program='Построение Парадного расчета, Прохождение, Бессметрный полк'
    )
    
    initial_day_events_count = len(_dayEventService.findAllDayEvents(day_id=3))
    
    _dayEventService.addDayEvent(new_dayEvent)
    
    current_day_events_count = len(_dayEventService.findAllDayEvents(day_id=3))
    
    assert current_day_events_count == initial_day_events_count + 1
    
def test_add_day_event_failed_validation():
    recreate_table()
    
    new_dayEvent = DayEvent(
        DayId=4,
        EventId=232,
        location='Площадь Ленина',
        endTime='12:00',
        program='Построение Парадного расчета, Прохождение, Бессметрный полк'
    )
    
    initial_day_events_count = len(_dayEventService.findAllDayEvents(day_id=4))
    
    _dayEventService.addDayEvent(new_dayEvent)
    
    current_day_events_count = len(_dayEventService.findAllDayEvents(day_id=4))
    
    assert current_day_events_count == initial_day_events_count + 1
    
def test_delete_day_event_correct_1():
    recreate_table()
    
    initial_day_events_count = len(_dayEventService.findAllDayEvents(day_id=1))
    
    _dayEventService.deleteDayEvent(day_id=1, event_id=1)
    
    current_day_events_count = len(_dayEventService.findAllDayEvents(day_id=1))
    
    assert current_day_events_count == initial_day_events_count - 1
    
def test_delete_day_event_correct_2():
    recreate_table()
    
    initial_day_events_count = len(_dayEventService.findAllDayEvents(day_id=2))
    
    _dayEventService.deleteDayEvent(day_id=2, event_id=1)
    
    current_day_events_count = len(_dayEventService.findAllDayEvents(day_id=2))
    
    assert current_day_events_count == initial_day_events_count - 1
    
def test_delete_day_event_failed_1():
    recreate_table()
    
    initial_day_events_count = len(_dayEventService.findAllDayEvents(day_id=4))
    
    _dayEventService.deleteDayEvent(day_id=1, event_id=1)
    
    current_day_events_count = len(_dayEventService.findAllDayEvents(day_id=4))
    
    assert current_day_events_count == initial_day_events_count - 1
    
def test_delete_day_event_failed_2():
    recreate_table()
    
    initial_day_events_count = len(_dayEventService.findAllDayEvents(day_id=5))
    
    _dayEventService.deleteDayEvent(day_id=5, event_id=1)
    
    current_day_events_count = len(_dayEventService.findAllDayEvents(day_id=5))
    
    assert current_day_events_count == initial_day_events_count - 1
    
    
    