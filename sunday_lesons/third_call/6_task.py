# ...рівновага сил знову була не на боці лицарів.
# Сер Рональд ще раз використав ріг, щоб викликати останню надію для своєї армії - цілителів. Храм, у якому вони жили, був навіть ближчим, ніж замок, звідки прибула перша хвиля підкріплення. Якщо цілителі прибудуть сюди досить швидко, вони врятують багато життів, а лицарі матимуть шанс перемогти.
# Битва триває, і кожна армія втрачає хороших воїнів. Давайте спробуємо це виправити та додамо новий тип юніта – Healer.

# Healer не буде битися (його attack = 0, тому він не може завдати шкоди).
# Але його роль також дуже важлива — щоразу, коли союзний солдат вдаряє ворога,
# Healer зцілює союзника, який стоїть прямо перед ним, на +2 бали здоров’я за допомогою методу heal().
# Зауважте, що здоров’я після зцілення не може перевищувати максимальне здоров’я одиниці.
# Наприклад, якщо Цілитель вилікує Воїна на 49 очок здоров'я, у Воїна буде 50 хп, тому що це для нього максимум.

# Основні параметри цілителя:
# health = 60
# attack = 0

from abc import ABC, abstractmethod
from collections import deque


def log_damage(func, unit_type="ALL"):
    def wrapper(self, damage):
        had_health = self.health

        func(self, damage)

        if unit_type == "ALL" or unit_type == self.__class__.__name__:
            message = f"{self.__class__.__name__}: had hp={had_health}, dmg={damage}, hp={self.health}"

            print(message)

    return wrapper


class Unit(ABC):
    def __init__(self, health: int, attack: int):
        self.health = health
        self.max_health = health
        self.attack = attack

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @abstractmethod
    def attack_unit(self, *args):
        pass

    @abstractmethod
    def receive_damage(self, damage: int):
        pass


class Warrior(Unit):
    def __init__(self, health=50, attack=5):
        self.health = health
        self.max_health = health
        self.attack: int = attack

    @property
    def is_alive(self):
        return self.health > 0

    def attack_unit(self, *args):
        args[0].receive_damage(self.attack)

    @log_damage
    def receive_damage(self, damage: int):
        self.health -= damage


class Knight(Warrior):
    def __init__(self):
        super().__init__(health=50, attack=7)


class Defender(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=3)
        self.defense = 2

    def receive_damage(self, damage: int):
        self.health -= max(0, damage - self.defense)


class Vampire(Warrior):
    def __init__(self):
        super().__init__(health=40, attack=4)
        self.vampirism = 50

    def attack_unit(self, *args):
        vamp = args[0]
        hp_before = vamp.health
        vamp.receive_damage(self.attack)
        self.health += int((hp_before - vamp.health) * self.vampirism // 100)
        self.health = min(self.health, self.max_health)


class Lancer(Warrior):
    def __init__(self):
        super().__init__(health=50, attack=6)
        self.attack_next_unit = 50  # percent

    def attack_unit(self, unit: Unit, next_unit=None):
        hp_before = unit.health
        unit.receive_damage(self.attack)
        damage_dealt = hp_before - unit.health

        if next_unit and next_unit.is_alive:
            next_unit.receive_damage(int(damage_dealt * self.attack_next_unit // 100))


class Healer(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=0)
        self.heal = 2

    def heal_unit(self, unit: Unit):
        if unit.is_alive:
            unit.health = min(unit.health + self.heal, unit.max_health)


def fight(
    u_1: Warrior,
    u_2: Warrior,
    u_1_behind=None,
    u_2_behind=None,
    u_1_next=None,
    u_2_next=None,
) -> bool:
    while u_1.is_alive and u_2.is_alive:
        u_1.attack_unit(u_2, u_2_next)

        if u_1_behind and isinstance(u_1_behind, Healer):
            u_1_behind.heal_unit(u_1)

        if u_2.is_alive:
            u_2.attack_unit(u_1, u_1_next)

            if u_2_behind and isinstance(u_2_behind, Healer):
                u_2_behind.heal_unit(u_2)

    return u_1.is_alive


class Army:
    def __init__(self):
        self.units: deque[Warrior] = deque()

    def add_units(self, unit_class: type[Warrior], number: int):
        for _ in range(number):
            self.units.append(unit_class())

    @property
    def is_units_alive(self) -> bool:
        return bool(self.units)


class Battle:
    def fight(self, army_1: Army, army_2: Army) -> bool:
        while army_1.is_units_alive and army_2.is_units_alive:
            u_1 = army_1.units[0]
            u_2 = army_2.units[0]

            u_1_behind = army_1.units[1] if len(army_1.units) > 1 else None
            u_2_behind = army_2.units[1] if len(army_2.units) > 1 else None

            u_1_next = army_2.units[1] if len(army_2.units) > 1 else None
            u_2_next = army_1.units[1] if len(army_1.units) > 1 else None

            if fight(u_1, u_2, u_1_behind, u_2_behind, u_1_next, u_2_next):
                army_2.units.popleft()
            else:
                army_1.units.popleft()

        return army_1.is_units_alive


if __name__ == "__main__":
    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()
    bob = Defender()
    mike = Knight()
    rog = Warrior()
    lancelot = Defender()
    eric = Vampire()
    adam = Vampire()
    richard = Defender()
    ogre = Warrior()
    freelancer = Lancer()
    vampire = Vampire()

    assert fight(chuck, bruce) == True
    assert fight(dave, carl) == False
    assert chuck.is_alive == True
    assert bruce.is_alive == False
    assert carl.is_alive == True
    assert dave.is_alive == False
    assert fight(carl, mark) == False
    assert carl.is_alive == False
    assert fight(bob, mike) == False
    assert fight(lancelot, rog) == True
    assert fight(eric, richard) == False
    assert fight(ogre, adam) == True
    assert fight(freelancer, vampire) == True
    assert freelancer.is_alive == True

    # healer tests
    healer = Healer()
    assert healer.health == 60
    assert healer.attack == 0

    warrior = Warrior()
    warrior.health = 30
    healer.heal_unit(warrior)
    assert warrior.health == 32

    warrior.health = 49
    healer.heal_unit(warrior)
    assert warrior.health == 50  # не перевищує max_health

    dead_warrior = Warrior()
    dead_warrior.health = 0
    healer.heal_unit(dead_warrior)
    assert dead_warrior.health == 0  # не лікує мертвих

    # battle tests
    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Lancer, 4)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Lancer, 2)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Lancer, 1)
    army_3.add_units(Defender, 2)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 1)
    army_4.add_units(Lancer, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == True
    assert battle.fight(army_3, army_4) == False
    print("Coding complete!")
