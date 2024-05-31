# КОД ДЛЯ СОЗДАНИЯ БАЗЫ ДАННЫХ

from Services.dbCreateService import Connection
if __name__ == "__main__":
    con = Connection()
    con.connect()
