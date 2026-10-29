from abc import ABC, abstractmethod
from enum import Enum

class SortingStrategy(ABC):

    @abstractmethod
    def sort(self, array: list) -> None:
        pass



class BubbleSortStrategy(SortingStrategy):

    def sort(self, array: list) -> None:
        print("Sorting using Bubble Sort")
        


class QuickSortStrategy(SortingStrategy):

    def sort(self, array: list) -> None:
        print("Sorting using Quick Sort")
        


class Sorter:

    def __init__(self):
        self.__strategy = None

    def set_strategy(self, strategy: SortingStrategy) -> None:
        self.__strategy = strategy

    def sort_array(self, array: list) -> None:
        if self.__strategy:
            self.__strategy.sort(array)





class RequestType(Enum):
    TYPE_A = 1
    TYPE_B = 2



class Request:

    def __init__(self, req_type: RequestType):
        self.__type = req_type

    def get_type(self) -> RequestType:
        return self.__type



class Handler(ABC):

    @abstractmethod
    def handle_request(self, request: Request) -> None:
        pass

    @abstractmethod
    def set_next_handler(self, next_handler: "Handler") -> None:
        pass



class ConcreteHandlerA(Handler):

    def __init__(self):
        self.__next_handler = None

    def set_next_handler(self, next_handler: Handler) -> None:
        self.__next_handler = next_handler

    def handle_request(self, request: Request) -> None:
        if request.get_type() == RequestType.TYPE_A:
            print("ConcreteHandlerA handled the request.")
        elif self.__next_handler is not None:
            self.__next_handler.handle_request(request)



class ConcreteHandlerB(Handler):

    def __init__(self):
        self.__next_handler = None

    def set_next_handler(self, next_handler: Handler) -> None:
        self.__next_handler = next_handler

    def handle_request(self, request: Request) -> None:
        if request.get_type() == RequestType.TYPE_B:
            print("ConcreteHandlerB handled the request.")
        elif self.__next_handler is not None:
            self.__next_handler.handle_request(request)





class Iterator(ABC):

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self):
        pass



class ArrayIterator(Iterator):

    def __init__(self, items: list):
        self.__items = items
        self.__position = 0

    def has_next(self) -> bool:
        return self.__position < len(self.__items)

    def next(self):
        if self.has_next():
            item = self.__items[self.__position]
            self.__position += 1
            return item
        raise IndexError("No more elements in collection")





if __name__ == "__main__":
    print("--- 1. STRATEGY ---")
    sorter = Sorter()

    sorter.set_strategy(BubbleSortStrategy())
    array1 = [5, 3, 8, 4, 2]
    sorter.sort_array(array1)

    sorter.set_strategy(QuickSortStrategy())
    array2 = [5, 3, 8, 4, 2]
    sorter.sort_array(array2)

    print("\n--- 2. RESPONSIBILITY CHAIN ---")
    handler_a = ConcreteHandlerA()
    handler_b = ConcreteHandlerB()

    handler_a.set_next_handler(handler_b)

    req_a = Request(RequestType.TYPE_A)
    req_b = Request(RequestType.TYPE_B)

    handler_a.handle_request(req_a)   
    handler_a.handle_request(req_b)  

    print("\n--- 3. ITERATOR ---")
    my_items = ["Яблоко", "Банан", "Апельсин"]
    iterator = ArrayIterator(my_items)

    while iterator.has_next():
        print(f"Элемент коллекции: {iterator.next()}")