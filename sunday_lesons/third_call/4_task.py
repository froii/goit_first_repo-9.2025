# Зграї ворон кружляли над полем бою.
# Багато відважних воїнів полягло в цій битві, багато хто продовжував битися.

# «Якщо так піде далі, ми просто переб’ємо один одного, і переможців не буде – ми всі програємо». -
# розмірковував сер Рональд, спостерігаючи перед собою похмуру картину.

# «Мені потрібно прийняти важливе рішення. Я знаю, чого це буде коштувати,
# але зараз це єдине, що може нас усіх врятувати…»
# Давним-давно, коли він часто шукав неприємностей і пригод, він пішов полювати на відьму,
#  яка мала величезну нагороду за голову. Кривава істота змогла врятувати їй життя,
#  умовивши лицаря взяти від неї подарунок - флакон з кров'ю вампіра.
#  Ця кров, влита в рот вмираючого, могла повернути його до життя у вигляді вампіра.
# Невже настав той день, коли він повинен цим скористатися?..
# Здавалося, це єдиний спосіб виграти цю битву.
# Сер Рональд почав схилятися над ледь живими тілами своїх лицарів, які лежали поруч. Кожному з них він сказав:
# - «Пий, тобі дадуть нове життя...»


# Отже, у нас є 3 типи юнітів: Warrior, Knight і Defender. Давайте зробимо битви ще
# більш епічними і додамо ще один тип - Vampire!
# Vampire повинен бути підкласом класу Warrior і мати додатковий параметр vampirism,
# який допомагає йому самолікуватися. Коли Vampire вражає іншу одиницю,
# він відновлює своє здоров’я на +50% від завданої шкоди (ворожий захист знижує значення завданої шкоди).
# Основні параметри Вампіра:
# health = 40
# attack = 4
# vampirism = 50%
# Ви повинні зберігати атрибут вампіризму як ціле число (50 на 50%). Це знадобиться,
# щоб це рішення розвивалося, щоб відповідати одному з наступних викликів цієї саги.


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


class Vampire(Warrior):
    def __init__(self):
        super().__init__(health=40, attack=4)
        self.vampirism = 50  # percent

    def health_regeneration(self, damage_dealt: int):
        self.health += int(damage_dealt * self.vampirism / 100)


def fight(unit_1: Warrior, unit_2: Warrior) -> bool:
    while unit_1.is_alive and unit_2.is_alive:
        attack_number = (
            min(getattr(unit_2, "defense", 0), unit_1.attack) - unit_1.attack
        )
        unit_2.health += attack_number
        unit_1.health += (
            int(attack_number * unit_2.vampirism / 100)
            if isinstance(unit_2, Vampire)
            else 0
        )

        if unit_2.is_alive:
            attack_number = (
                min(getattr(unit_1, "defense", 0), unit_2.attack) - unit_2.attack
            )
            unit_1.health += attack_number
            unit_2.health += (
                int(attack_number * unit_1.vampirism / 100)
                if isinstance(unit_1, Vampire)
                else 0
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

    # battle tests
    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Defender, 4)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == False
    assert battle.fight(army_3, army_4) == True
    print("Coding complete!")
