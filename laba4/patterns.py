from abc import ABC, abstractmethod
from enum import Enum

class DeliveryStrategy(ABC):

    @abstractmethod
    def calculate_cost(self, weight: float) -> float:
        pass

class CourierDeliveryStrategy(DeliveryStrategy):

    def calculate_cost(self, weight: float) -> float:
        print("Расчет доставки курьером (фиксированная ставка + за вес)")
        return 300.0 + (weight * 50.0)

class PickupPointDeliveryStrategy(DeliveryStrategy):

    def calculate_cost(self, weight: float) -> float:
        print("Расчет доставки в пункт выдачи (дешевле)")
        return 150.0 + (weight * 20.0)

class OrderCalculator:

    def __init__(self):
        self.__strategy = None

    def set_strategy(self, strategy: DeliveryStrategy) -> None:
        self.__strategy = strategy

    def calculate(self, weight: float) -> float:
        if self.__strategy:
            return self.__strategy.calculate_cost(weight)
        raise ValueError("Стратегия доставки не выбрана!")





class CommentType(Enum):
    PROFANITY = 1  # Мат / грубость
    SPAM = 2  # Реклама / спам
    CLEAN = 3  # Обычный хороший комментарий

class Comment:

    def __init__(self, text: str, comment_type: CommentType):
        self.__text = text
        self.__type = comment_type

    def get_type(self) -> CommentType:
        return self.__type

    def get_text(self) -> str:
        return self.__text

class CommentHandler(ABC):

    @abstractmethod
    def process_comment(self, comment: Comment) -> None:
        pass

    @abstractmethod
    def set_next_handler(self, next_handler: "CommentHandler") -> None:
        pass

class ProfanityFilterHandler(CommentHandler):

    def __init__(self):
        self.__next_handler = None

    def set_next_handler(self, next_handler: CommentHandler) -> None:
        self.__next_handler = next_handler

    def process_comment(self, comment: Comment) -> None:
        if comment.get_type() == CommentType.PROFANITY:
            print(
                f"[Фильтр мата]: Комментарий заблокирован ('{comment.get_text()[:15]}...')"
            )
        elif self.__next_handler is not None:
            self.__next_handler.process_comment(comment)

class SpamFilterHandler(CommentHandler):

    def __init__(self):
        self.__next_handler = None

    def set_next_handler(self, next_handler: CommentHandler) -> None:
        self.__next_handler = next_handler

    def process_comment(self, comment: Comment) -> None:
        if comment.get_type() == CommentType.SPAM:
            print(
                f"[Фильтр спама]: Реклама отклонена ('{comment.get_text()[:15]}...')"
            )
        elif self.__next_handler is not None:
            self.__next_handler.process_comment(comment)
        else:
            print(
                f"[Модерация]: Комментарий успешно опубликован! ('{comment.get_text()}')"
            )





class PlaylistIterator(ABC):

    @abstractmethod
    def has_more_songs(self) -> bool:
        pass

    @abstractmethod
    def get_next_song(self) -> str:
        pass


class MusicPlaylistIterator(PlaylistIterator):

    def __init__(self, songs: list):
        self.__songs = songs
        self.__current_index = 0

    def has_more_songs(self) -> bool:
        return self.__current_index < len(self.__songs)

    def get_next_song(self) -> str:
        if self.has_more_songs():
            song = self.__songs[self.__current_index]
            self.__current_index += 1
            return song
        raise IndexError("Плейлист закончился")





if __name__ == "__main__":
    print("--- 1. STRATEGY (Калькулятор доставки) ---")
    calculator = OrderCalculator()

    calculator.set_strategy(CourierDeliveryStrategy())
    cost1 = calculator.calculate(4.5)  # Вес 4.5 кг
    print(f"Итоговая стоимость: {cost1} руб.\n")

    calculator.set_strategy(PickupPointDeliveryStrategy())
    cost2 = calculator.calculate(4.5)
    print(f"Итоговая стоимость: {cost2} руб.\n")

    print("--- 2. RESPONSIBILITY CHAIN (Модерация комментариев) ---")
    filter_profanity = ProfanityFilterHandler()
    filter_spam = SpamFilterHandler()

    # Выстраиваем цепочку: сначала проверка на мат, потом на спам
    filter_profanity.set_next_handler(filter_spam)

    c1 = Comment("Ужасный сервис, вы все...", CommentType.PROFANITY)
    c2 = Comment("Купите криптовалюту со скидкой!", CommentType.SPAM)
    c3 = Comment("Отличный материал, спасибо за статью!", CommentType.CLEAN)

    filter_profanity.process_comment(c1)  # Заблокирует фильтр мата
    filter_profanity.process_comment(c2)  # Заблокирует фильтр спама
    filter_profanity.process_comment(c3)  # Пройдет оба и опубликуется

    print("\n--- 3. ITERATOR (Музыкальный плейлист) ---")
    my_playlist = ["Трек №1: Rock Anthem", "Трек №2: Jazz Chill", "Трек №3: Pop Hit"]
    player_iterator = MusicPlaylistIterator(my_playlist)

    print("Воспроизведение плейлиста:")
    while player_iterator.has_more_songs():
        print(f"Сейчас играет -> {player_iterator.get_next_song()}")