"""
Выполнить это задание, максимально
задействуя перегрузки операторов:
Используя замыкания функций,
объявите внутреннюю функцию,
которая принимает в качестве
аргумента коллекцию (список или кортеж)
и возвращает или минимальное значение,
или максимальное, в зависимости
от значения параметра type внешней функции.
Если type равен «max»,
то возвращается максимальное значение,
иначе – минимальное.
По умолчанию type должно
принимать значение «max».
Вызовите внутреннюю функцию
замыкания и отобразите на
экране результат ее работы.
"""
class SmartNumber:
    def __init__(self, value):
        self.value = value

    def __gt__(self, other):
        print(f"  [Перегрузка >]: Сравниваем {self.value} > {other.value}")
        return self.value > other.value

    def __lt__(self, other):
        print(f"  [Перегрузка <]: Сравниваем {self.value} < {other.value}")
        return self.value < other.value

    def __eq__(self, other):
        print(f"  [Перегрузка ==]: Проверяем {self.value} == {other.value}")
        return self.value == other.value

    def __repr__(self):
        return str(self.value)


def create_finder(type="max"):

    def find(collection):
        if not collection:
            return None

        if type == "max":
            return max(collection)

        else:
            return min(collection)

    return find

numbers = [SmartNumber(5), SmartNumber(12), SmartNumber(3), SmartNumber(8)]

max_finder = create_finder()
result_max = max_finder(numbers)
print(f"Результат max: {result_max}\n")

min_finder = create_finder(type="min")
result_min = min_finder(numbers)
print(f"Результат min: {result_min}")