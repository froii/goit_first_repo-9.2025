# У попередній місії «Воїни» ви дізналися, як влаштувати двобій між двома воїнами.
# Чудова робота! Але давайте перейдемо до чогось більш епічного – армій!
# У цій місії ваше завдання — додавати нові класи та функції до вже існуючих.
# Новий клас повинен бути Army і мати метод add_units() - для додавання вибраної кількості одиниць
# до армії.
#  Перший доданий підрозділ буде першим, хто піде у бій, другий буде другим, ...
# Також потрібно створити клас Battle() з функцією fight(), яка визначатиме найсильнішу армію.
# Бої відбуваються за такими принципами:
# спочатку відбувається двобій між першим воїном першої армії та першим воїном другої армії
# (використовується підрахунок FIFO).
# Як тільки один з них гине - в двобій вступає наступний воїн з армії,
# яка втратила бійця, а воїн, що вижив, продовжує битися з поточним здоров'ям.
#  Так триває до тих пір, поки не загинуть всі солдати однієї з армій. У цьому випадку функція
#  fight() має повернути True,
#   якщо перша армія перемогла, або False, якщо друга була сильнішою.
# Зверніть увагу, що армія 1 має перевагу починати кожен бій!
# """


class Warrior:
    def __init__(self, health=50, attack=5):
        self.health = health
        self.attack = attack

    @property
    def is_alive(self):
        return self.health > 0


class Knight(Warrior):
    def __init__(self):
        super().__init__(health=50, attack=7)


def fight(unit_1: Warrior, unit_2: Warrior) -> bool:
    while unit_1.is_alive and unit_2.is_alive:
        unit_2.health -= unit_1.attack
        if unit_2.is_alive:
            unit_1.health -= unit_2.attack
    return unit_1.is_alive


class Army:
    def __init__(self):
        self.units: list[Warrior] = []

    def add_units(self, unit_class: type[Warrior], number: int):
        for _ in range(number):
            self.units.append(unit_class())

    @property
    def is_units_alive(self) -> bool:
        return bool(self.units)


class Battle:
    def fight(self, army_1: Army, army_2: Army) -> bool:
        while army_1.is_units_alive and army_2.is_units_alive:
            unit_1 = army_1.units[0]
            unit_2 = army_2.units[0]
            if fight(unit_1, unit_2):
                army_2.units.pop(0)
            else:
                army_1.units.pop(0)
        return army_1.is_units_alive


# from __future__ import annotations
# from collections import deque
# from dataclasses import dataclass
# from typing import Callable

# @dataclass
# class Warrior:
#     health: int = 50
#     attack: int = 5

#     @property
#     def is_alive(self) -> bool:
#         return self.health > 0

#     def attack_unit(self, unit: Warrior):
#         unit.health -= self.attack

# @dataclass
# class Knight(Warrior):
#     attack: int = 7

# def fight(attacker: Warrior, defender: Warrior):
#     while attacker.is_alive:
#         attacker.attack_unit(defender)
#         if not defender.is_alive:
#             return True
#         defender.attack_unit(attacker)
#     return False

# class Army:
#     units: deque[Warrior]

#     def __init__(self) -> None:
#         self.units = deque()

#     def add_units(self, unit_type: Callable[[], Warrior], count: int):
#         for _ in range(count):
#             unit: Warrior = unit_type()
#             self.units.append(unit)

#     @property
#     def is_anyone_alive(self) -> bool:
#         return bool(self.units)

# class Battle:
#     def fight(self, army1: Army, army2: Army):
#         unit1 = army1.units.popleft()
#         unit2 = army2.units.popleft()
#         while army1.is_anyone_alive and army2.is_anyone_alive:
#             unit1_won = fight(unit1, unit2)
#             if unit1_won:
#                 unit2 = army2.units.popleft()
#             else:
#                 unit1 = army1.units.popleft()

#         return army1.is_anyone_alive


if __name__ == "__main__":
    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()

    assert fight(chuck, bruce) == True
    assert fight(dave, carl) == False
    assert chuck.is_alive == True
    assert bruce.is_alive == False
    assert carl.is_alive == True
    assert dave.is_alive == False
    assert fight(carl, mark) == False
    assert carl.is_alive == False
    army_1 = Army()
    army_2 = Army()
    army_1.add_units(Warrior, 20)
    army_2.add_units(Warrior, 21)
    battle = Battle()
    battle.fight(army_1, army_2)
    # battle tests
    my_army = Army()
    my_army.add_units(Knight, 3)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 3)

    army_3 = Army()
    army_3.add_units(Warrior, 20)
    army_3.add_units(Knight, 5)

    army_4 = Army()
    army_4.add_units(Warrior, 30)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == True
    assert battle.fight(army_3, army_4) == False
    print("Coding complete")
