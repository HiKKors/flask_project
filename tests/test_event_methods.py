import pytest

from Services import EventService
from Models import Event

from Services.dbCreateService import Connection

event_service = EventService()

con = Connection()

def test_get_one_event_correct_1():
    """Тестирование функции findEvent() с правильными данными
    Дропаем таблицу и заново вводим данные чтобы тест был пройден
    """
    
    con.drop_event()
    con.createEventTable()
    con.insertEventData()
    
    event = Event(eventName = 'День космонавтики', 
             description = 'Праздник Дня Космонавтики: Откройте Вселенную вместе с нами! Присоединяйтесь к увлекательным мероприятиям, посвященным освоению космоса и достижениям человечества в космических исследованиях.', 
             invitees = 'Иванов, Петров, Киселев')
    
    """Ищем данные с id 1"""
    res_event = event_service.findEvent(id=1)
    assert(
        res_event.eventName == event.eventName
        and res_event.description == event.description
        and res_event.invitees == event.invitees
    )
    
def test_get_one_event_correct_2():  
    """
    Тестирование функции findEvent() с правильными данными (второй кейс).
    Проверяется поиск события по заданному id.
    """  
    event_1 = Event(eventName = 'День Победы', 
             description = 'Мероприятие в честь Дня Победы: Память и Почитание', 
             invitees = 'Зубков, Крылов, Морозов')
    
    res_event_1 = event_service.findEvent(id=2)
    assert(
        res_event_1.eventName == event_1.eventName
        and res_event_1.description == event_1.description
        and res_event_1.invitees == event_1.invitees
    )
    
def test_get_one_event_failed_1():
    """Тестирование функции findEvent() с неправильными данными"""
    # тест с первой записью
    event = Event(eventName = 'День космонафтики', 
             description = 'Праздник Дня Космонафтики: Откройте Вселенную вместе с нами! Присоединяйтесь к увлекательным мероприятиям, посвященным освоению космоса и достижениям человечества в космических исследованиях.', 
             invitees = 'Иванов, Петров, Киселев')
    
    res_event = event_service.findEvent(id=1)
    assert(
        res_event.eventName == event.eventName
        and res_event.description == event.description
        and res_event.invitees == event.invitees
    )
    
    # тест со второй записью
def test_get_one_event_failed_2():
    """Создаем переменную с не верными данными"""
    event_1 = Event(eventName = 'День Побеты', 
             description = 'Мероприятие в честь Дня Победы: Память и Почитание', 
             invitees = 'Зубков, Крылов, Морозов')
    """Производим поиск"""
    res_event_1 = event_service.findEvent(id=2)
    
    assert(
        res_event_1.eventName == event_1.eventName
        and res_event_1.description == event_1.description
        and res_event_1.invitees == event_1.invitees
    )
    
def test_add_event_correct_1():
    """
    Тестирование функции addEvent() с корректными данными.
    Проверяется добавление нового события.
    """
    event_service.delete_data()
    
    new_event = Event(
        eventName='День космонавтики', 
        description='Праздник Дня Космонавтики: Откройте Вселенную вместе с нами! Присоединяйтесь к увлекательным мероприятиям, посвященным освоению космоса и достижениям человечества в космических исследованиях.', 
        invitees='Иванов, Петров, Киселев'
    )
    # находим количество всех записей
    initial_events_count = len(event_service.findAllEvents())
    
    event_service.addEvent(new_event)
    
    events_with_new_event = event_service.findAllEvents()
    # проверяем количество после добавления
    assert len(events_with_new_event) == initial_events_count + 1
    
def test_add_event_correct_2():
    """
    Тестирование функции addEvent() с корректными данными (второй кейс).
    Добавление второго события.
    """
    new_event = Event(
        eventName='День Победы', 
        description='Мероприятие в честь Дня Победы: Память и Почитание', 
        invitees='Зубков, Крылов, Морозов'
    )
    
    initial_events_count = len(event_service.findAllEvents())
    
    event_service.addEvent(new_event)
    
    events_with_new_event = event_service.findAllEvents()
    
    assert len(events_with_new_event) == initial_events_count + 1
    
def test_add_event_failed_1():
    """
    Тестирование функции addEvent() с некорректными данными.
    Пыаемся добавить дубликат
    """
    new_event = Event(
        eventName='День космонавтики', 
        description='Праздник Дня Космонавтики: Откройте Вселенную вместе с нами! Присоединяйтесь к увлекательным мероприятиям, посвященным освоению космоса и достижениям человечества в космических исследованиях.', 
        invitees='Иванов, Петров, Киселев'
    )
    
    # находим количество всех записей
    initial_events_count = len(event_service.findAllEvents())
    
    # пытаемся добавить дубликат
    event_service.addEvent(new_event)
    
    events_with_new_event = event_service.findAllEvents()
    
    # проверяем количество после добавления
    assert len(events_with_new_event) == initial_events_count + 1
    
def test_add_event_failed_2():
    """
    Тестирование функции addEvent() с корректными данными.
    Добавляем запись без обязательного поля
    """
    # создаем запись без какого-то поля
    new_event = Event(
        eventName='День космонавтики', 
        description='Праздник Дня Космонавтики: Откройте Вселенную вместе с нами! Присоединяйтесь к увлекательным мероприятиям, посвященным освоению космоса и достижениям человечества в космических исследованиях.', 
        invitees='Иванов, Петров, Киселев'
    )
    
    # находим количество всех записей
    initial_events_count = len(event_service.findAllEvents())
    
    # пытаемся добавить запись
    event_service.addEvent(new_event)
    
    events_with_new_event = event_service.findAllEvents()
    
    # проверяем количество после добавления
    assert len(events_with_new_event) == initial_events_count + 1
    
def test_delete_event_correct_1():
    """
    Тестирование функции deleteEvent() с корректными данными.
    Проверяется удаление события по существующему id.
    """
    con.drop_event()
    con.createEventTable()
    con.insertEventData()
    
    # находим количество всех записей
    initial_events_count = len(event_service.findAllEvents())
    
    event_service.deleteEvent(id=1)
    
    events_with_new_event = event_service.findAllEvents()
    # проверяем количество после добавления
    assert len(events_with_new_event) == initial_events_count - 1

def test_delete_event_correct_2():
    """
    Тестирование функции deleteEvent() с корректными данными.
    Проверяется удаление события по существующему id (второй кейс).
    """
    con.drop_event()
    con.createEventTable()
    con.insertEventData()
    
    # находим количество всех записей
    initial_events_count = len(event_service.findAllEvents())
    
    event_service.deleteEvent(id=2)
    
    events_with_new_event = event_service.findAllEvents()
    # проверяем количество после добавления
    assert len(events_with_new_event) == initial_events_count - 1
    
def test_delete_event_failed_1():
    """
    Тестирование функции deleteEvent() с корректными данными.
    Проверяется удаление события по не существующему id.
    """
    con.drop_event()
    con.createEventTable()
    con.insertEventData()
    
    # находим количество всех записей
    initial_events_count = len(event_service.findAllEvents())
    
    event_service.deleteEvent(id=3)
    
    events_with_new_event = event_service.findAllEvents()
    # проверяем количество после добавления
    assert len(events_with_new_event) == initial_events_count - 1
    
def test_delete_event_failed_2():
    """
    Тестирование функции deleteEvent() с корректными данными.
    Проверяется удаление события по не существующему id (второй кейс).
    """
    con.drop_event()
    con.createEventTable()
    con.insertEventData()
    
    # находим количество всех записей
    initial_events_count = len(event_service.findAllEvents())
    
    event_service.deleteEvent(id=4)
    
    events_with_new_event = event_service.findAllEvents()
    # проверяем количество после добавления
    assert len(events_with_new_event) == initial_events_count - 1
    
def test_update_event_correct_1():
    """
    Тестирование функции updateEvent() с корректными данными.
    Проверяется обновление данных события по id.
    """
    con.drop_event()
    con.createEventTable()
    con.insertEventData()
    
    event = Event(eventName = 'Обновленное название', 
             description = 'Обновленное описание', 
             invitees = 'Обновленные участники')
    
    event_id = 1
    
    event_service.updateEvent(event_id, event)
    updated_event = event_service.findEvent(id=1)
    
    
    assert updated_event is not None
    assert updated_event.eventName == 'Обновленное название'
    assert updated_event.description == 'Обновленное описание'
    assert updated_event.invitees == 'Обновленные участники'
    
def test_update_event_correct_2():
    """
    Тестирование функции updateEvent() с корректными данными.
    Проверяется обновление данных события по id (второй кейс).
    """
    con.drop_event()
    con.createEventTable()
    con.insertEventData()
    
    event = Event(eventName = 'Обновленное название2', 
             description = 'Обновленное описание2', 
             invitees = 'Обновленные участники__2')
    
    event_id = 2
    
    event_service.updateEvent(event_id, event)
    updated_event = event_service.findEvent(id=2)
    
    
    assert updated_event is not None
    assert updated_event.eventName == 'Обновленное название2'
    assert updated_event.description == 'Обновленное описание2'
    assert updated_event.invitees == 'Обновленные участники__2'
    
    
def test_update_event_failed_id():
    """
    Тестирование функции updateEvent() с корректными данными.
    Проверяется обновление данных события по несуществующему id.
    """
    con.drop_event()
    con.createEventTable()
    con.insertEventData()
    
    # Пишем данные которые хотим обновить
    event = Event(eventName = 'Обновленное название', 
             description = 'Обновленное описание', 
             invitees = 'Обновленные участники')
    
    # не существующий id
    event_id = 3
    
    # пытаемся обновить не существующую запись
    event_service.updateEvent(event_id, event)
    updated_event = event_service.findEvent(id=2)
    
    
    assert updated_event is not None
    assert updated_event.eventName == 'Обновленное название2'
    assert updated_event.description == 'Обновленное описание2'
    assert updated_event.invitees == 'Обновленные участники__2'

def test_update_event_failed_duplicate():
    """
    Тестирование функции updateEvent() с корректными данными.
    Проверяется обновление данных дубликатом.
    """
    con.drop_event()
    con.createEventTable()
    con.insertEventData()
    
    # Пишем данные которые уже есть 
    event = Event(
        eventName='День космонавтики', 
        description='Праздник Дня Космонавтики: Откройте Вселенную вместе с нами! Присоединяйтесь к увлекательным мероприятиям, посвященным освоению космоса и достижениям человечества в космических исследованиях.',  
        invitees='Иванов, Петров, Киселев'
    )
    # не существующий id
    event_id = 2
    
    # пытаемся обновить
    event_service.updateEvent(event_id, event)
    updated_event = event_service.findEvent(id=2)
    
    
    assert updated_event is not None
    assert updated_event.eventName == 'Обновленное название2'
    assert updated_event.description == 'Обновленное описание2'
    assert updated_event.invitees == 'Обновленные участники__2'