from dataclasses import dataclass
from typing import Type


@dataclass
class Warrior:
    health: int = 50
    attack: int = 5
    next: 'Warrior' = None

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def attack_unit(self, unit):
        unit.get_damage(self.attack)

    def get_damage(self, damage_level: int) -> int:
        self.health -= damage_level
        return damage_level


@dataclass
class Knight(Warrior):
    attack: int = 7


@dataclass
class Defender(Warrior):
    health: int = 60
    attack: int = 3
    defence: int = 2

    def get_damage(self, attack: int) -> int:
        damage_level = max(attack - self.defence, 0)
        self.health -= damage_level
        return damage_level


@dataclass
class Vampire(Warrior):
    vampirism_pct: int = 50
    health: int = 40
    initial_health = health
    attack: int = 4

    def attack_unit(self, unit: Warrior):
        damage_level = unit.get_damage(self.attack)
        self.health += (damage_level * self.vampirism_pct // 100)
        self.health = min(self.health, self.initial_health)
# Lancer should be the subclass of the Warrior class and should attack in a specific way -
#  when he hits the other unit, he also deals a 50% of the dealt damage to the enemy unit,
# standing behind the firstly assaulted one (enemy defense makes the dealt damage value lower -
# consider this).
# The basic parameters of the Lancer:
# health = 50
# attack = 6


@dataclass
class Lancer(Warrior):
    health: int = 50
    attack: int = 6
    attack_2nd_unit_pct: int = 50

    def attack_unit(self, unit,):
        unit.get_damage(self.attack)
        if unit.next and unit.next.is_alive:
            unit.next.get_damage(self.attack * self.attack_2nd_unit_pct // 100)


class Army:
    def __init__(self) -> None:
        self.head = None
        self.tail = None

    def add_units(self, unit_type: Type, q: int):
        for _ in range(q):
            unit: Warrior = unit_type()
            if not self.head:
                self.head = unit
                self.tail = unit
            else:
                self.tail.next = unit
                self.tail = unit

    @property
    def is_exist(self) -> bool:
        return self.head is not None


class Battle:
    def fight(self, army1: Army, army2: Army):

        while army1.is_exist & army2.is_exist:
            unit1 = army1.head
            unit2 = army2.head
            if fight(unit1, unit2):
                army2.head = unit2.next
            else:
                army1.head = unit1.next
        return army1.is_exist


def fight(fighter1: Warrior, fighter2: Warrior):
    while fighter1.is_alive & fighter2.is_alive:
        fighter1.attack_unit(fighter2)
        if fighter2.is_alive:
            fighter2.attack_unit(fighter1)

    return fighter1.is_alive


if __name__ == '__main__':

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

    assert fight(chuck, bruce)
    assert fight(dave, carl) == False
    assert chuck.is_alive
    assert bruce.is_alive == False
    assert carl.is_alive
    assert dave.is_alive == False
    assert fight(carl, mark) == False
    assert carl.is_alive == False
    assert fight(bob, mike) == False
    assert fight(lancelot, rog)
    assert fight(eric, richard) == False
    assert fight(ogre, adam)
    assert fight(freelancer, vampire)
    assert freelancer.is_alive

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

    assert battle.fight(my_army, enemy_army)
    assert battle.fight(army_3, army_4) == False
    print("Coding complete!")
