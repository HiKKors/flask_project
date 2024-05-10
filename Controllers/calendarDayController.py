from flask import Blueprint

calendarDay_api = Blueprint('calendarDay_api', __name__)

@calendarDay_api.route('/ts/v1/days', methods=['GET'])
def get():
    return 'Вывод из контроллера дней'