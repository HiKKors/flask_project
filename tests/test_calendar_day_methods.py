import pytest

from Services import CalendarDayService
from Models import CalendarDays

from Services.dbCreateService import Connection

calendarDay_service = CalendarDayService()

con = Connection()

def test_gen_one_day_correct_1():
    """Тестирование функции findCalendarDay() с правильными данными
    Дропаем таблицу и заново вводим данные чтобы тест был пройден
    """
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    calendarDay = CalendarDays(Date='2024-04-12',
                               WeekDay='Пятница',
                               DayType='Будний')
    
    res_day = calendarDay_service.findCalendarDay(id=1)
    
    assert (
        res_day.Date == calendarDay.Date
        and res_day.WeekDay == calendarDay.WeekDay
        and res_day.DayType == calendarDay.DayType
    )
    
def test_gen_one_day_correct_2():
    """
    Тестирование функции findCalendarDay() с правильными данными (второй кейс).
    Проверяется поиск события по заданному id.
    """  
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    calendarDay = CalendarDays(Date='2024-05-09',
                               WeekDay='Четверг',
                               DayType='Будний')
    
    res_day = calendarDay_service.findCalendarDay(id=2)
    
    assert (
        res_day.Date == calendarDay.Date
        and res_day.WeekDay == calendarDay.WeekDay
        and res_day.DayType == calendarDay.DayType
    )
    
def test_gen_one_day_failed_1():
    """Тестирование функции findCalendarDay() с неправильными данными"""
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    calendarDay = CalendarDays(Date='2024-04-12',
                               WeekDay='Пятница',
                               DayType='Будний')
    
    res_day = calendarDay_service.findCalendarDay(id=0)
    
    assert (
        res_day.Date == calendarDay.Date
        and res_day.WeekDay == calendarDay.WeekDay
        and res_day.DayType == calendarDay.DayType
    )
    
def test_gen_one_day_failed_2():
    """Тестирование функции findCalendarDay() с неправильными данными (второй кейс)"""
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    calendarDay = CalendarDays(Date='2024-05-09',
                               WeekDay='Четверг',
                               DayType='Будний')
    
    res_day = calendarDay_service.findCalendarDay(id=3)
    
    assert (
        res_day.Date == calendarDay.Date
        and res_day.WeekDay == calendarDay.WeekDay
        and res_day.DayType == calendarDay.DayType
    )
    
def test_add_calendar_day_correct_1():
    """
    Тестирование функции addCalendarDay() с корректными данными.
    Проверяется добавление нового события.
    """
    calendarDay_service.delete_data()
    
    new_calendar_day = CalendarDays(Date='2024-14-06',
                               WeekDay='Суббота',
                               DayType='Выходной')
    
    initial_days_count = len(calendarDay_service.findAllCalendarDays())
    
    calendarDay_service.addCalendarDay(new_calendar_day)
    
    days_count_after_add = len(calendarDay_service.findAllCalendarDays())
    
    assert days_count_after_add == initial_days_count + 1
    
def test_add_calendar_day_correct_2():
    """
    Тестирование функции addCalendarDay() с корректными данными.
    Проверяется добавление нового события (второй кейс).
    """
    calendarDay_service.delete_data()
    
    new_calendar_day = CalendarDays(Date='2024-22-11',
                               WeekDay='Понедельник',
                               DayType='Будний')
    
    initial_days_count = len(calendarDay_service.findAllCalendarDays())
    
    calendarDay_service.addCalendarDay(new_calendar_day)
    
    days_count_after_add = len(calendarDay_service.findAllCalendarDays())
    
    assert days_count_after_add == initial_days_count + 1
    
def test_add_calendar_day_failed_1():
    """
    Тестирование функции addCalendarDay() с некорректными данными.
    Пыаемся добавить дубликат
    """
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    new_calendar_day = CalendarDays(Date='2024-04-12',
                               WeekDay='Пятница',
                               DayType='Будний')
    
    initial_days_count = len(calendarDay_service.findAllCalendarDays())
    
    calendarDay_service.addCalendarDay(new_calendar_day)
    
    days_count_after_add = len(calendarDay_service.findAllCalendarDays())
    
    assert days_count_after_add == initial_days_count + 1
    
def test_add_calendar_day_failed_2():
    """
    Тестирование функции addEvent() с некорректными данными.
    Пыаемся добавить запись без обязательного поля
    """
    calendarDay_service.delete_data()
    
    new_calendar_day = CalendarDays(WeekDay='Понедельник',
                               DayType='Будний')
    
    initial_days_count = len(calendarDay_service.findAllCalendarDays())
    
    calendarDay_service.addCalendarDay(new_calendar_day)
    
    days_count_after_add = len(calendarDay_service.findAllCalendarDays())
    
    assert days_count_after_add == initial_days_count + 1
    
def test_delete_day_correct_1():
    """
    Тестирование функции deteleCalendarDay() с корректными данными.
    Проверяется удаление события по существующему id.
    """
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    # находим количество всех записей
    initial_days_count = len(calendarDay_service.findAllCalendarDays())
    
    calendarDay_service.deteleCalendarDay(id=1)
    
    days_count_after_delete = calendarDay_service.findAllCalendarDays()
    # проверяем количество после добавления
    assert len(days_count_after_delete) == initial_days_count - 1
    
def test_delete_day_correct_2():
    """
    Тестирование функции deteleCalendarDay() с корректными данными.
    Проверяется удаление события по существующему id (второй кейс).
    """
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    # находим количество всех записей
    initial_days_count = len(calendarDay_service.findAllCalendarDays())
    
    calendarDay_service.deteleCalendarDay(id=2)
    
    days_count_after_delete = calendarDay_service.findAllCalendarDays()
    # проверяем количество после добавления
    assert len(days_count_after_delete) == initial_days_count - 1
    
def test_delete_day_failed_1():
    """
    Тестирование функции deteleCalendarDay() с корректными данными.
    Проверяется удаление дня по не существующему id.
    """
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    # находим количество всех записей
    initial_days_count = len(calendarDay_service.findAllCalendarDays())
    
    calendarDay_service.deteleCalendarDay(id=3)
    
    days_count_after_delete = calendarDay_service.findAllCalendarDays()
    # проверяем количество после добавления
    assert len(days_count_after_delete) == initial_days_count - 1
    
def test_delete_day_failed_2():
    """
    Тестирование функции deteleCalendarDay() с корректными данными.
    Проверяется удаление дня по не существующему id (второй кейс).
    """
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    # находим количество всех записей
    initial_days_count = len(calendarDay_service.findAllCalendarDays())
    
    calendarDay_service.deteleCalendarDay(id=0)
    
    days_count_after_delete = calendarDay_service.findAllCalendarDays()
    # проверяем количество после добавления
    assert len(days_count_after_delete) == initial_days_count - 1
    
def test_update_calendar_day_correct_1():
    """
    Тестирование функции updateCalendarDay() с корректными данными.
    Проверяется обновление данных дня по id.
    """
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    day = CalendarDays(
        Date = '2024-16-01', 
        WeekDay = 'Обновленный день недели', 
        DayType = 'Обновленный тип дня' 
        )
    
    day_id = 1
    
    calendarDay_service.updateCalendarDay(day_id, day)
    updated_day = calendarDay_service.findCalendarDay(id=1)
    
    
    assert updated_day is not None
    assert updated_day.Date == '2024-16-01'
    assert updated_day.WeekDay == 'Обновленный день недели'
    assert updated_day.DayType == 'Обновленный тип дня'  
    
    
def test_update_calendar_day_сorrect_2():
    """
    Тестирование функции updateCalendarDay() с корректными данными.
    Проверяется обновление данных дня по id (второй кейс).
    """
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    day = CalendarDays(
        Date = '2024-09-03', 
        WeekDay = 'Обновленный день недели(2)', 
        DayType = 'Обновленный тип дня(2)' 
        )
    
    day_id = 2
    
    calendarDay_service.updateCalendarDay(day_id, day)
    updated_day = calendarDay_service.findCalendarDay(id=2)
    
    
    assert updated_day is not None
    assert updated_day.Date == '2024-09-03'
    assert updated_day.WeekDay == 'Обновленный день недели(2)'
    assert updated_day.DayType == 'Обновленный тип дня(2)'  
    
    
def test_update_calendar_day_failed_id():
    """
    Тестирование функции updateCalendarDay() с корректными данными.
    Проверяется обновление данных дня по несуществующему id.
    """
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    day = CalendarDays(
        Date = '2024-09-03', 
        WeekDay = 'Обновленный день недели(2)', 
        DayType = 'Обновленный тип дня(2)' 
        )
    
    day_id = 6
    
    calendarDay_service.updateCalendarDay(day_id, day)
    updated_day = calendarDay_service.findCalendarDay(id=2)
    
    
    assert updated_day is not None
    assert updated_day.Date == '2024-09-03'
    assert updated_day.WeekDay == 'Обновленный день недели(2)'
    assert updated_day.DayType == 'Обновленный тип дня(2)' 

def test_update_event_failed_duplicate():
    """
    Тестирование функции updateCalendarDay() с корректными данными.
    Проверяется обновление данных дубликатом.
    """
    con.drop_calendarDay()
    con.createTableCalendarDays()
    con.insertCalendarData()
    
    day = CalendarDays(
        Date = '2024-04-12', 
        WeekDay = 'Пятница', 
        DayType = 'Будний' 
        )
    
    day_id = 1
    
    calendarDay_service.updateCalendarDay(day_id, day)
    updated_day = calendarDay_service.findCalendarDay(id=2)
    
    
    assert updated_day is not None
    assert updated_day.Date == '2024-09-03'
    assert updated_day.WeekDay == 'Обновленный день недели(2)'
    assert updated_day.DayType == 'Обновленный тип дня(2)' 