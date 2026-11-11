from abc import ABC, abstractmethod

class Door(ABC):

    @abstractmethod
    def open_door(self, key: str) -> None:
        pass


class RealDoor(Door):

    def open_door(self, key: str) -> None:
        print("Щелчок! Дверь физически открыта.")


class SmartLockProxy(Door):

    def __init__(self, correct_key: str):
        self.__real_door = RealDoor()
        self.__correct_key = correct_key

    def open_door(self, key: str) -> None:
        print("[Умный замок]: Считываем электронный ключ...")
        if key == self.__correct_key:
            self.__real_door.open_door(key)
        else:
            print("Неверный ключ! Доступ заблокирован.")





class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, amount: float) -> None:
        pass

class LegacyStripeAPI:

    def make_charge(self, cents: int) -> None:
        print(f"Списание через старый Stripe API: {cents} центов.")

class StripeAdapter(PaymentProcessor):

    def __init__(self, legacy_stripe: LegacyStripeAPI):
        self.__legacy_stripe = legacy_stripe

    def pay(self, amount: float) -> None:
        cents = int(amount * 100)
        print("[Адаптер]: Конвертируем сумму в центы...")
        self.__legacy_stripe.make_charge(cents)





class MessageSender(ABC):

    @abstractmethod
    def send(self, text: str) -> None:
        pass

class TelegramSender(MessageSender):

    def send(self, text: str) -> None:
        print(f"Отправка в Telegram: {text}")


class EmailSender(MessageSender):

    def send(self, text: str) -> None:
        print(f"Отправка на Email: {text}")

class Notification(ABC):

    def __init__(self, sender: MessageSender):
        self._sender = sender  

    @abstractmethod
    def notify(self, title: str, message: str) -> None:
        pass

class UrgentNotification(Notification):

    def notify(self, title: str, message: str) -> None:
        formatted = f"[СРОЧНО!] {title}: {message}"
        self._sender.send(formatted)


class ReminderNotification(Notification):

    def notify(self, title: str, message: str) -> None:
        formatted = f"[Напоминание] {title}: {message}"
        self._sender.send(formatted)





if __name__ == "__main__":
    print("--- 1. PROXY (Умный замок) ---")
    my_lock = SmartLockProxy("my_secret_key_123")

    print("Попытка войти с плохим ключом:")
    my_lock.open_door("wrong_key")

    print("\nПопытка войти с правильным ключом:")
    my_lock.open_door("my_secret_key_123")

    print("\n--- 2. ADAPTER (Оплата) ---")
    old_stripe = LegacyStripeAPI()
    adapter = StripeAdapter(old_stripe)
    adapter.pay(150.50)  

    print("\n--- 3. BRIDGE (Уведомления) ---")
    tg_channel = TelegramSender()
    email_channel = EmailSender()

    urgent_tg = UrgentNotification(tg_channel)
    urgent_tg.notify("Пожарная тревога", "Всем покинуть здание!")

    reminder_email = ReminderNotification(email_channel)
    reminder_email.notify("Вебинар", "Не забудьте подключиться в 19:00.")