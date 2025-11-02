# ... вампіри билися люто. Судячи з перебігу бою, сер Рональд прийняв правильне рішення, хоча й не дуже етично двозначне.
# Раптом до лав Умберта приєдналися нові солдати — невже в нього є туз у рукаві? Улани представили свіжі сили, що ускладнювало
#  становище сера Рональда, улани могли атакувати своїми довгими списами відразу двох солдатів. Треба було з цим щось робити…
# Здається, що Warrior, Knight, Defender і Vampire недостатньо, щоб виграти битву. Додамо ще один потужний тип юнітів - Lancer.
# Lancer має бути підкласом класу Warrior і повинен атакувати певним чином - коли він влучає в іншу одиницю,
#  він також завдає 50% завданої шкоди ворожій одиниці, стоячи позаду першої атакуваної (ворожий захист робить значення завданої шкоди нижче - врахуйте це).

# Основні параметри Lancer:
# health = 50
# attack = 6

from abc import ABC, abstractmethod


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
        self.attack = attack

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


def fight(unit_1: Warrior, unit_2: Warrior, unit_1_next=None, unit_2_next=None) -> bool:
    while unit_1.is_alive and unit_2.is_alive:
        unit_1.attack_unit(unit_2, unit_2_next)
        if unit_2.is_alive:
            unit_2.attack_unit(unit_1, unit_1_next)
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
            unit_1_next = army_1.units[1] if len(army_1.units) > 1 else None
            unit_2_next = army_2.units[1] if len(army_2.units) > 1 else None

            if fight(unit_1, unit_2, unit_1_next, unit_2_next):
                army_2.units.pop(0)
            else:
                army_1.units.pop(0)
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
