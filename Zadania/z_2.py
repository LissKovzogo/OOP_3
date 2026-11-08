"""
Дополнительно к требуемым в заданиях операциям перегрузить операцию индексирования [].
Максимально возможный размер списка задать константой.
В отдельном поле size должно храниться максимальное для данного объекта количество элементов списка;
реализовать метод size(), возвращающий установленную длину. Если количество элементов списка
изменяется во время работы, определить в классе поле count. Первоначальные значения size
и count устанавливаются конструктором.

В тех задачах, где возможно, реализовать конструктор инициализации строкой.

9. Карточка иностранного слова представляет собой словарю, содержащую иностранное слово и его перевод.
Для моделирования электронного словаря иностранных слов реализовать класс Dictionary.
Данный класс имеет поле-название словаря и содержит список словарей WordCard,
представляющих собой карточки иностранного слова. Название словаря задается при
создании нового словаря, но должна быть предоставлена возможность его изменения
во время работы. Карточки добавляются в словарь и удаляются из него.
Реализовать поиск определенного слова как отдельный метод.
Аргументом операции индексирования должно быть иностранное слово.
В словаре не должно быть карточек-дублей.
Реализовать операции объединения, пересечения и вычитания словарей.
При реализации должен создаваться новый словарь, а исходные словари не должны изменяться.
При объединении новый словарь должен содержать без повторений все слова,
содержащиеся в обоих словарях-операндах. При пересечении новый словарь должен состоять
только из тех слов, которые имеются в обоих словарях-операндах.
При вычитании новый словарь должен содержать слова первого словаря-операнда, отсутствующие во втором.
"""

MAX_SIZE = 100

class WordCard:
    def __init__(self, foreign_word, translation):
        self.foreign_word = foreign_word
        self.translation = translation

    def __eq__(self, other):
        if isinstance(other, WordCard):
            return self.foreign_word == other.foreign_word
        return False

    def __hash__(self):
        return hash(self.foreign_word)

    def __repr__(self):
        return f"WordCard('{self.foreign_word}', '{self.translation}')"


class Dictionary:
    def __init__(self, name="Новый словарь"):
        self.name = name
        self.size = MAX_SIZE
        self.count = 0
        self._cards = []

    @classmethod
    def from_string(cls, name, data_string):
        dictionary = cls(name)
        if data_string.strip():
            pairs = data_string.split(',')
            for pair in pairs:
                if ':' in pair:
                    word, trans = pair.split(':')
                    dictionary.add_card(WordCard(word.strip(), trans.strip()))
        return dictionary

    def change_name(self, new_name):
        self.name = new_name

    def add_card(self, card):
        if self.count >= self.size:
            raise OverflowError("Словарь заполнен (достигнут максимальный размер)")

        if card not in self._cards:
            self._cards.append(card)
            self.count += 1

    def remove_card(self, foreign_word):
        for card in self._cards:
            if card.foreign_word == foreign_word:
                self._cards.remove(card)
                self.count -= 1
                return True
        return False

    def search(self, foreign_word):
        for card in self._cards:
            if card.foreign_word == foreign_word:
                return card.translation
        return None

    def size_method(self):
        return self.size

    def __getitem__(self, foreign_word):
        translation = self.search(foreign_word)
        if translation is not None:
            return translation
        raise KeyError(f"Слово '{foreign_word}' не найдено в словаре")

    def __setitem__(self, foreign_word, translation):
        for card in self._cards:
            if card.foreign_word == foreign_word:
                card.translation = translation
                return
        self.add_card(WordCard(foreign_word, translation))

    def __or__(self, other):
        if not isinstance(other, Dictionary):
            return NotImplemented

        new_dict = Dictionary(f"{self.name} | {other.name}")
        for card in self._cards:
            new_dict.add_card(WordCard(card.foreign_word, card.translation))
        for card in other._cards:
            new_dict.add_card(WordCard(card.foreign_word, card.translation))
        return new_dict

    def __and__(self, other):
        if not isinstance(other, Dictionary):
            return NotImplemented

        new_dict = Dictionary(f"{self.name} & {other.name}")
        other_words = {card.foreign_word for card in other._cards}
        for card in self._cards:
            if card.foreign_word in other_words:
                new_dict.add_card(WordCard(card.foreign_word, card.translation))
        return new_dict

    def __sub__(self, other):
        if not isinstance(other, Dictionary):
            return NotImplemented

        new_dict = Dictionary(f"{self.name} - {other.name}")
        other_words = {card.foreign_word for card in other._cards}
        for card in self._cards:
            if card.foreign_word not in other_words:
                new_dict.add_card(WordCard(card.foreign_word, card.translation))
        return new_dict

    def __str__(self):
        return f"Словарь '{self.name}' (карточек: {self.count}/{self.size})"


if __name__ == "__main__":
    dict1 = Dictionary("Англо-русский")
    dict1.add_card(WordCard("apple", "яблоко"))
    dict1.add_card(WordCard("dog", "собака"))
    dict1.add_card(WordCard("cat", "кошка"))

    dict2 = Dictionary.from_string("Мой словарь", "dog:пес, bird:птица, cat:кот")

    print(dict1)
    print(dict2)

    print(f"Поиск слова 'dog': {dict1.search('dog')}")
    print(f"Индексация dict1['apple']: {dict1['apple']}")

    dict_union = dict1 | dict2
    print(dict_union)
    print(f"Перевод 'dog' в объединенном: {dict_union['dog']}")

    dict_intersection = dict1 & dict2
    print(dict_intersection)

    dict_subtraction = dict1 - dict2
    print(dict_subtraction)

    print(f"Максимальный размер (size): {dict1.size}")
    print(f"Текущее количество (count): {dict1.count}")
    print(f"Вызов метода size(): {dict1.size_method()}")