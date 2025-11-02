# """...тут і там відбувалися сутички між різними солдатами, а нові війська продовжували надходити. Конфлікт поступово став більше нагадувати маленьку війну.
# «Лицарі, послухайте мій наказ! Забирайте свої щити! Зміцнюйте обладунки! Ми беремо занадто багато ударів», - кричав сер Рональд.
# Ніхто не очікував, що воїни Умберта зможуть конкурувати з добре навченими лицарями, тому на початку битви лицарі використовували виключно дворучні мечі – нікому навіть на думку не спало на оборону. Але, схоже, пора відступити і взятися за одноручні мечі та щити замість колишньої смертоносної зброї. Це трохи знизить штурмові можливості лицарів, але дозволить їм краще захищатися від небезпечних атак ворожих воїнів.
# У попередній місії - Army battles, ви навчилися вести битву між 2 арміями. Але у нас є тільки 2 види юнітів - Warriors і Knights. Додамо ще один – Defender. Він повинен бути підкласом класу Warriors і мати додатковий параметр defense, який допомагає йому довше виживати. Коли інший юніт влучає в захисника, він втрачає певну кількість свого здоров'я за наступною формулою: enemy attack - self defense (якщо enemy attack > self defense). В іншому випадку defender не втрачає здоров'я.

# Основні параметри Defender:
# health = 60
# attack = 3
# defense = 2
# """


from typing import override


class Warrior:
    def __init__(self, health=50, attack=5):
        self.health = health
        self.attack = attack

    @property
    def is_alive(self):
        return self.health > 0

    def attack_unit(self, unit):
        unit.receive_damage(self.attack)

    def receive_damage(self, damage: int):
        self.health -= damage


class Knight(Warrior):
    def __init__(self):
        super().__init__(health=50, attack=7)


class Defender(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=3)
        self.defense = 2

    @override
    def receive_damage(self, damage: int):
        self.health -= damage - self.defense if damage > self.defense else 0


def fight(unit_1: Warrior, unit_2: Warrior) -> bool:
    while unit_1.is_alive and unit_2.is_alive:
        unit_2.health += (
            min(getattr(unit_2, "defense", 0), unit_1.attack) - unit_1.attack
        )
        if unit_2.is_alive:
            unit_1.health += (
                min(getattr(unit_1, "defense", 0), unit_2.attack) - unit_2.attack
            )
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


#  @dataclass
# class Warrior:
#     health: int = 50
#     attack: int = 5

#     @property
#     def is_alive(self) -> bool:
#         return self.health > 0

#     def attack_unit(self, unit: Warrior):
#         unit.receive_damage(self.attack)

#     def receive_damage(self, damage: int):
#         self.health -= damage

# @dataclass
# class Defender(Warrior):
#     health: int = 60
#     attack: int = 3
#     defense: int = 2

#     @override
#     def receive_damage(self, damage: int):
#         self.health -= damage - self.defense if damage > self.defense else 0


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

    # battle tests
    my_army = Army()
    my_army.add_units(Defender, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Defender, 1)

    army_4 = Army()
    army_4.add_units(Warrior, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == False
    assert battle.fight(army_3, army_4) == True
    print("Coding complete")


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
#         unit.get_damage(self.attack)

#     def get_damage(self, damage_level: int) -> None:
#         self.health -= damage_level

# @dataclass
# class Knight(Warrior):
#     attack: int = 7

# @dataclass
# class Defender(Warrior):
#     health: int = 60
#     attack: int = 3
#     defense: int = 2

#     def get_damage(self, damage_level: int) -> None:
#         self.health -= max(damage_level - self.defense, 0)


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


# def fight(attacker: Warrior, defender: Warrior):
#     while attacker.is_alive:
#         attacker.attack_unit(defender)
#         if not defender.is_alive:
#             return True
#         defender.attack_unit(attacker)
#     return False
