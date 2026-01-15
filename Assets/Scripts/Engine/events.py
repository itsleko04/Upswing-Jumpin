class Event:
    """Глобальная реализация событий"""
    def __init__(self):
        self.__functions = []

    def connect(self, func):
        """Подписать метод"""
        self.__functions.append(func)

    def disconnect(self, func):
        """Отписать метод"""
        self.__functions.remove(func)

    def invoke(self):
        """Вызвать событие"""
        for func in self.__functions:
            func()

    def clear(self):
        self.__functions.clear()


class EventWithArgs:
    """Глобальная реализация событий с обязательными аргументами"""
    def __init__(self):
        self.__functions = []

    def connect(self, func):
        """Подписать метод"""
        self.__functions.append(func)

    def disconnect(self, func, args):
        """Отписать метод"""
        self.__functions.remove(func)

    def invoke(self, args):
        """Вызвать событие"""
        for func in self.__functions:
            func(args)

    def clear(self):
        self.__functions.clear()