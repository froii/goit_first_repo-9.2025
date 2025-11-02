"""
Демонстрація інкапсуляції в Python: Pokemon Edition
Public, Protected, Private атрибути
"""


class Pokemon:
    def __init__(
        self, name: str, type: str, health: int, level: int, is_legendary: bool
    ):
        # PUBLIC - базова інформація, доступна всім
        self.name = name
        self.type = type

        # PROTECTED - здоров'я (не варто змінювати напряму)
        self._health = health
        self._max_health = health

        # PRIVATE - рівень та легендарний статус (тільки через методи)
        self.__level = level
        self.__is_legendary = is_legendary

    def attack(self, other_pokemon):
        damage = 10 + self.__level * 5
        print(f"{self.name} attacks {other_pokemon.name} for {damage} damage!")
        other_pokemon.take_damage(damage)

    def dodge(self):
        print(f"{self.name} dodged the attack!")

    def evolve(self, new_form: str):
        if self.__level >= 16:
            print(f"✨ {self.name} is evolving into {new_form}!")
            self.name = new_form
            self.__level += 5
            self._health = self._max_health
            print(f"Evolution complete! New level: {self.__level}")
        else:
            print(f"❌ {self.name} needs level 16+ to evolve (current: {self.__level})")

    # Getter/Setter для PROTECTED (_health)
    def get_health(self) -> int:
        return self._health

    def take_damage(self, damage: int):
        """Метод для безпечного зменшення здоров'я"""
        self._health = max(0, self._health - damage)
        if self._health == 0:
            print(f"💀 {self.name} fainted!")
        else:
            print(f"   {self.name}'s health: {self._health}/{self._max_health}")

    def heal(self, amount: int):
        """Метод для безпечного лікування"""
        self._health = min(self._max_health, self._health + amount)
        print(f"💚 {self.name} healed! Health: {self._health}/{self._max_health}")

    # Getter/Setter для PRIVATE (__level)
    def get_level(self) -> int:
        return self.__level

    def level_up(self):
        """Безпечний метод підвищення рівня"""
        self.__level += 1
        self._max_health += 10
        self._health = self._max_health
        print(f"⭐ {self.name} leveled up to {self.__level}!")

    # Getter для PRIVATE (__is_legendary)
    def is_legendary(self) -> bool:
        return self.__is_legendary

    def show_stats(self):
        """Показує всю статистику покемона"""
        legendary_mark = "🌟" if self.__is_legendary else ""
        print(f"\n📊 {self.name} {legendary_mark}")
        print(f"   Type: {self.type}")
        print(f"   Health: {self._health}/{self._max_health}")
        print(f"   Level: {self.__level}")
        print(f"   Legendary: {'Yes' if self.__is_legendary else 'No'}")


# ============================================
# ДЕМОНСТРАЦІЯ
# ============================================

print("=" * 60)
print("🎮 СТВОРЕННЯ ПОКЕМОНІВ")
print("=" * 60)

pikachu = Pokemon("Pikachu", "Electric", 100, 10, False)
mewtwo = Pokemon("Mewtwo", "Psychic", 150, 70, True)

print(f"✅ Створено: {pikachu.name} і {mewtwo.name}")


print("\n" + "=" * 60)
print("1. PUBLIC АТРИБУТИ - прямий доступ")
print("=" * 60)

print(f"Ім'я: {pikachu.name}")
print(f"Тип: {pikachu.type}")

# Можна змінювати напряму
pikachu.name = "Pikachu-Thunderbolt"
print(f"Змінено ім'я: {pikachu.name}")
pikachu.name = "Pikachu"  # Повертаємо назад


print("\n" + "=" * 60)
print("2. PROTECTED АТРИБУТИ (_health)")
print("=" * 60)

# ❌ ПОГАНА ПРАКТИКА - прямий доступ
print(f"Прямий доступ (погано): pikachu._health = {pikachu._health}")

# ✅ ПРАВИЛЬНО - через getter
print(f"Через getter (добре): {pikachu.get_health()}")

# ✅ ПРАВИЛЬНО - зміна через методи
pikachu.take_damage(30)
pikachu.heal(20)


print("\n" + "=" * 60)
print("3. PRIVATE АТРИБУТИ (__level, __is_legendary)")
print("=" * 60)

# ❌ НЕ ПРАЦЮЄ - прямий доступ заборонений
try:
    print(pikachu.__level)
except AttributeError as e:
    print("❌ ПОМИЛКА при pikachu.__level:")
    print(f"   {e}")

# ✅ ПРАВИЛЬНО - через getter/методи
print(f"\n✅ Через getter: Level = {pikachu.get_level()}")
print(f"✅ Через getter: Legendary = {pikachu.is_legendary()}")

# ✅ ПРАВИЛЬНО - зміна через метод
pikachu.level_up()

# ⚠️ ОБХІД через name mangling (НЕ РЕКОМЕНДУЄТЬСЯ)
# print(f"\n⚠️ Обхід через _Pokemon__level: {pikachu._Pokemon__level}")
# print(f"⚠️ Обхід через _Pokemon__is_legendary: {pikachu._Pokemon__is_legendary}")


print("\n" + "=" * 60)
print("4. МЕТОДИ В ДІЇ")
print("=" * 60)

pikachu.show_stats()
mewtwo.show_stats()

print("\n⚔️ БІЙ:")
pikachu.attack(mewtwo)
mewtwo.dodge()
mewtwo.attack(pikachu)


print("\n" + "=" * 60)
print("5. ЕВОЛЮЦІЯ")
print("=" * 60)

# Спроба еволюції на низькому рівні
print("\nСпроба 1 (рівень 11):")
pikachu.evolve("Raichu")

# Підвищуємо рівень
print("\nПідвищуємо рівень:")
for _ in range(6):
    pikachu.level_up()

# Успішна еволюція
print("\nСпроба 2 (рівень 17):")
pikachu.evolve("Raichu")


print("\n" + "=" * 60)
print("6. ФІНАЛЬНА СТАТИСТИКА")
print("=" * 60)

pikachu.show_stats()
mewtwo.show_stats()
