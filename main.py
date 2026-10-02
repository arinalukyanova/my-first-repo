from abc import ABC, abstractmethod

class Attacker(ABC):
    @abstractmethod
    def attack(self, unit: 'Unit') -> None:
        """Метод для нанесения урона юниту."""
        pass


class Moveable(ABC):
    @abstractmethod
    def move(self, new_x: int, new_y: int) -> None:
        """Метод для изменения координат объекта."""
        pass

class GameObject(ABC):
    def __init__(self, obj_id: int, name: str, x: int, y: int):
        self._id = obj_id
        self._name = name
        self._x = x
        self._y = y

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y


class Unit(GameObject):
    def __init__(self, obj_id: int, name: str, x: int, y: int, hp: float):
        super().__init__(obj_id, name, x, y)
        self._hp = hp

    def is_alive(self) -> bool:
        return self._hp > 0

    def get_hp(self) -> float:
        return self._hp

    def receive_damage(self, damage: float) -> None:
        self._hp -= damage
        if self._hp < 0:
            self._hp = 0.0


class Building(GameObject):
    def __init__(self, obj_id: int, name: str, x: int, y: int, built: bool):
        super().__init__(obj_id, name, x, y)
        self._built = built

    def is_built(self) -> bool:
        return self._built

class Archer(Unit, Attacker, Moveable):
    def __init__(self, obj_id: int, name: str, x: int, y: int, hp: float):
        super().__init__(obj_id, name, x, y, hp)
        self._damage = 15.0

    def attack(self, unit: Unit) -> None:
        if self.is_alive():
            print(f"Лучник {self.get_name()} атакует {unit.get_name()}!")
            unit.receive_damage(self._damage)

    def move(self, new_x: int, new_y: int) -> None:
        self._x = new_x
        self._y = new_y
        print(f"Лучник {self.get_name()} переместился в координаты ({self._x}, {self._y})")


class Fort(Building, Attacker):
    def __init__(self, obj_id: int, name: str, x: int, y: int, built: bool):
        super().__init__(obj_id, name, x, y, built)
        self._damage = 40.0

    def attack(self, unit: Unit) -> None:
        if self.is_built():
            print(f"Крепость {self.get_name()} стреляет из пушек по {unit.get_name()}!")
            unit.receive_damage(self._damage)
        else:
            print(f"Крепость {self.get_name()} еще не достроена и не может атаковать.")


class MobileHouse(Building, Moveable):
    def __init__(self, obj_id: int, name: str, x: int, y: int, built: bool):
        super().__init__(obj_id, name, x, y, built)

    def move(self, new_x: int, new_y: int) -> None:
        self._x = new_x
        self._y = new_y
        print(f"Дом на колесах {self.get_name()} переехал в координаты ({self._x}, {self._y})")

if __name__ == "__main__":

    archer = Archer(1, "Робин Гуд", 0, 0, 100.0)
    enemy = Archer(2, "Вражеский Лучник", 2, 2, 50.0)
    fort = Fort(3, "Западный Форт", 10, 10, built=True)
    house = MobileHouse(4, "Трейлер", 5, 5, built=True)

    print("=== ТЕСТИРОВАНИЕ ===")
    print(f"{enemy.get_name()} HP до атаки: {enemy.get_hp()}")
    
    archer.attack(enemy)
    print(f"{enemy.get_name()} HP после атаки лучника: {enemy.get_hp()}")
    archer.move(1, 1)

    fort.attack(enemy)
    print(f"{enemy.get_name()} HP после атаки форта: {enemy.get_hp()}")
    print(f"Жив ли {enemy.get_name()}? {'Да' if enemy.is_alive() else 'Нет'}")

    house.move(6, 8)