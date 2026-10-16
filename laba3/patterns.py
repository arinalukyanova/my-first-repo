from abc import ABC, abstractmethod

class Singleton:
    __instance = None 

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__data = "Единственные настройки системы"
        return cls.__instance

    def get_data(self) -> str:
        return self.__data





class Logger(ABC):

    @abstractmethod
    def log(self, message: str) -> None:
        raise NotImplementedError(
            "Метод log() должен быть реализован в дочернем классе!"
        )



class FileLogger(Logger):

    def log(self, message: str) -> None:
        print(f"Запись в файл: {message}")



class ConsoleLogger(Logger):

    def log(self, message: str) -> None:
        print(f"Вывод в консоль: {message}")



class LoggerFactory(ABC):

    @abstractmethod
    def create_logger(self) -> Logger:
        raise NotImplementedError(
            "Метод create_logger() должен быть реализован в дочернем классе!"
        )

    def log_message(self, message: str) -> None:
        logger = self.create_logger()
        logger.log(message)



class FileLoggerFactory(LoggerFactory):

    def create_logger(self) -> Logger:
        return FileLogger()



class ConsoleLoggerFactory(LoggerFactory):

    def create_logger(self) -> Logger:
        return ConsoleLogger()





class Button(ABC):

    @abstractmethod
    def paint(self) -> None:
        raise NotImplementedError("Метод paint() должен быть реализован!")



class Checkbox(ABC):

    @abstractmethod
    def paint(self) -> None:
        raise NotImplementedError("Метод paint() должен быть реализован!")



class WindowsButton(Button):

    def paint(self) -> None:
        print("Отрисована кнопка в стиле Windows")



class WindowsCheckbox(Checkbox):

    def paint(self) -> None:
        print("Отрисован чекбокс в стиле Windows")



class MacButton(Button):

    def paint(self) -> None:
        print("Отрисована кнопка в стиле Mac")



class MacCheckbox(Checkbox):

    def paint(self) -> None:
        print("Отрисован чекбокс в стиле Mac")



class GUIFactory(ABC):

    @abstractmethod
    def create_button(self) -> Button:
        raise NotImplementedError("Метод create_button() должен быть реализован!")

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        raise NotImplementedError(
            "Метод create_checkbox() должен быть реализован!"
        )



class WindowsFactory(GUIFactory):

    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()



class MacFactory(GUIFactory):

    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()



class Application:

    def __init__(self, factory: GUIFactory):
        self.__button = factory.create_button()
        self.__checkbox = factory.create_checkbox()

    def paint(self) -> None:
        self.__button.paint()
        self.__checkbox.paint()





class Pizza:

    def __init__(self):
        self.__dough = ""
        self.__sauce = ""
        self.__topping = ""

    def set_dough(self, dough: str) -> None:
        self.__dough = dough

    def set_sauce(self, sauce: str) -> None:
        self.__sauce = sauce

    def set_topping(self, topping: str) -> None:
        self.__topping = topping

    def __str__(self) -> str:
        return f"Пицца: тесто={self.__dough}, соус={self.__sauce}, начинка={self.__topping}"



class PizzaBuilder(ABC):

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def build_dough(self) -> None:
        pass

    @abstractmethod
    def build_sauce(self) -> None:
        pass

    @abstractmethod
    def build_topping(self) -> None:
        pass

    @abstractmethod
    def get_pizza(self) -> Pizza:
        pass



class HawaiianPizzaBuilder(PizzaBuilder):

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.__pizza = Pizza()

    def build_dough(self) -> None:
        self.__pizza.set_dough("пышное тесто")

    def build_sauce(self) -> None:
        self.__pizza.set_sauce("сладковатый соус")

    def build_topping(self) -> None:
        self.__pizza.set_topping("ветчина + ананас")

    def get_pizza(self) -> Pizza:
        pizza = self.__pizza
        self.reset()
        return pizza



class PizzaDirector:

    def __init__(self, builder: PizzaBuilder):
        self.__builder = builder

    def make_pizza(self) -> Pizza:
        self.__builder.build_dough()
        self.__builder.build_sauce()
        self.__builder.build_topping()
        return self.__builder.get_pizza()





if __name__ == "__main__":
    print("--- 1. SINGLETON ---")
    s1 = Singleton()
    s2 = Singleton()
    print("Совпадают ли объекты s1 и s2?:", s1 is s2)
    print("Данные:", s1.get_data())

    print("\n--- 2. FACTORY METHOD ---")
    file_factory = FileLoggerFactory()
    file_factory.log_message("Сообщение для файла")

    console_factory = ConsoleLoggerFactory()
    console_factory.log_message("Сообщение для консоли")

    print("\n--- 3. ABSTRACT FACTORY ---")
    win_app = Application(WindowsFactory())
    win_app.paint()

    mac_app = Application(MacFactory())
    mac_app.paint()

    print("\n--- 4. BUILDER ---")
    builder = HawaiianPizzaBuilder()
    director = PizzaDirector(builder)
    hawaiian_pizza = director.make_pizza()
    print("Готовый продукт:", hawaiian_pizza)