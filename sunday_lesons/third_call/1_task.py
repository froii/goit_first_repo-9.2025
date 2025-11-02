# Вам потрібно створити клас Warrior,
#  екземпляри якого матимуть 2 параметри – health (дорівнює 50 балам) і attack (дорівнює 5 балам),
#   а також 1 властивість – is_alive, яка може бути True (якщо здоров’я воїна > 0). )
#   або False (в іншому випадку).
#   Крім того, ви повинні створити другий тип одиниць – Knight, який має бути підкласом Warrior,
#    але мати підвищену атаку – 7. Також вам потрібно створити функцію fight(),
#    яка ініціюватиме двобій між 2 бійцями та визначатиме найсильніший з них.
#    Поєдинок відбувається за таким принципом:
# Кожного ходу перший воїн буде вдаряти по другому, і цей другий втрачатиме своє здоров'я
# в тій самій величині, що і атака першого воїна. Після цього, якщо він ще живий,
# другий воїн зробить те ж саме з першим.
# Поєдинок закінчується смертю одного з них.
# Якщо перший воїн ще живий (і, отже, іншого більше немає), функція має повернути True,
# False в іншому випадку.


# class Warrior:
#     def __init__(self, health=50, attack=5):
#         self.health = health
#         self.attack = attack

#     @property
#     def is_alive(self):
#         return self.health > 0


# class Knight(Warrior):
#     def __init__(self):
#         super().__init__(health=50, attack=7)

# def fight(unit_1: Warrior, unit_2: Warrior) -> bool:
#     while unit_1.is_alive and unit_2.is_alive:
#         print("unit_2", unit_2.health)
#         unit_2.health -= unit_1.attack
#         if unit_2.is_alive:
#             print("unit_1", unit_1.health)
#             unit_1.health -= unit_2.attack
#     return unit_1.is_alive


class Warrior:
    _health: int
    _attack: int

    def __init__(self, health: int = 50, attack: int = 5):
        self._health = health
        self._attack = attack

    @property
    def is_alive(self) -> bool:
        return self._health > 0

    def receive_damage_from(self, attacker: Warrior):
        self._health -= attacker._attack


class Knight(Warrior):
    def __init__(self):
        super().__init__(attack=7)


def fight(attacker: Warrior, defender: Warrior):
    while attacker.is_alive:
        defender.receive_damage_from(attacker)
        if not defender.is_alive:
            return True
        attacker.receive_damage_from(defender)
    return False






if __name__ == "__main__":
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

    print("Coding complete!")


