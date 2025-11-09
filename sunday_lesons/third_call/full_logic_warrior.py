from abc import ABC, abstractmethod


def log_damage(func, unit_type="ALL"):
    def wrapper(self, damage):
        had_health = self.health
        func(self, damage)
        if unit_type == "ALL" or unit_type == self.__class__.__name__:
            print(f"{self.__class__.__name__}: had hp={had_health}, dmg={damage}, hp={self.health}")
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
    def attack_unit(self, enemy: "Unit", next_enemy: "Unit | None" = None) -> None:
        pass

    @abstractmethod
    def receive_damage(self, damage: int) -> None:
        pass


class Warrior(Unit):
    def __init__(self, health: int = 50, attack: int = 5):
        super().__init__(health, attack)
        self.next: "Warrior | None" = None

    def attack_unit(self, enemy: Unit, next_enemy: Unit | None = None) -> None:
        enemy.receive_damage(self.attack)

    @log_damage
    def receive_damage(self, damage: int) -> None:
        self.health -= damage


class Knight(Warrior):
    def __init__(self):
        super().__init__(health=50, attack=7)


class Defender(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=3)
        self.defense = 2

    def receive_damage(self, damage: int) -> None:
        self.health -= max(0, damage - self.defense)


class Vampire(Warrior):
    def __init__(self):
        super().__init__(health=40, attack=4)
        self.vampirism = 50

    def attack_unit(self, enemy: Unit, next_enemy: Unit | None = None) -> None:
        hp_before = enemy.health
        enemy.receive_damage(self.attack)
        damage_dealt = hp_before - enemy.health
        self.health = min(self.health + damage_dealt * self.vampirism // 100, self.max_health)


class Lancer(Warrior):
    def __init__(self):
        super().__init__(health=50, attack=6)
        self.pierce_power = 50

    def attack_unit(self, enemy: Unit, next_enemy: Unit | None = None) -> None:
        hp_before = enemy.health
        enemy.receive_damage(self.attack)

        if next_enemy and next_enemy.is_alive:
            damage_dealt = hp_before - enemy.health
            next_enemy.receive_damage(damage_dealt * self.pierce_power // 100)


class Healer(Warrior):
    def __init__(self):
        super().__init__(health=60, attack=0)
        self.heal_power = 2

    def heal_unit(self, unit: Unit) -> None:
        if unit.is_alive:
            unit.health = min(unit.health + self.heal_power, unit.max_health)


def _heal_ally(unit: Warrior) -> None:
    if unit.next and isinstance(unit.next, Healer):
        unit.next.heal_unit(unit)


def fight(u_1: Warrior, u_2: Warrior) -> bool:
    while u_1.is_alive and u_2.is_alive:
        u_1.attack_unit(u_2, u_2.next)
        _heal_ally(u_1)

        if u_2.is_alive:
            u_2.attack_unit(u_1, u_1.next)
            _heal_ally(u_2)

    return u_1.is_alive


class Army:
    def __init__(self):
        self.head: Warrior | None = None
        self.tail: Warrior | None = None

    def add_units(self, unit_class: type[Warrior], number: int) -> None:
        for _ in range(number):
            new_unit = unit_class()
            if not self.head:
                self.head = self.tail = new_unit
            else:
                assert self.tail is not None
                self.tail.next = new_unit
                self.tail = new_unit

    @property
    def is_units_alive(self) -> bool:
        return self.head is not None and self.head.is_alive


class Battle:
    @staticmethod
    def fight(army_1: Army, army_2: Army) -> bool:
        while army_1.is_units_alive and army_2.is_units_alive:
            assert army_1.head is not None and army_2.head is not None

            if fight(army_1.head, army_2.head):
                army_2.head = army_2.head.next
            else:
                army_1.head = army_1.head.next

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

    assert fight(chuck, bruce)
    assert not fight(dave, carl)
    assert chuck.is_alive
    assert not bruce.is_alive
    assert carl.is_alive
    assert not dave.is_alive
    assert not fight(carl, mark)
    assert not carl.is_alive
    assert not fight(bob, mike)
    assert fight(lancelot, rog)
    assert not fight(eric, richard)
    assert fight(ogre, adam)
    assert fight(freelancer, vampire)
    assert freelancer.is_alive

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
    assert warrior.health == 50

    dead_warrior = Warrior()
    dead_warrior.health = 0
    healer.heal_unit(dead_warrior)
    assert dead_warrior.health == 0

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
    assert not battle.fight(army_3, army_4)
    print("Coding complete!")
