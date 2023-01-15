import utils


class BadKey(Exception):
    """"""

    def __init__(self, key):
        super().__init__()
        self._key = key

    def get_key(self):
        return self._key


class AffineCaesarKey(object):
    """Ключ для аффинного шифра. Состоит из множителя multiplier и слагаемого summand"""

    def __init__(self, multiplier: int = 1, summand: int = 0):
        self.multiplier = multiplier
        self.summand = summand


class AphabetMapper(object):
    def __init__(self, letters: str) -> None:
        # Сохраняем буквы
        self._letters = letters
        # Создаем словарь для быстрого поиска номеров букв
        self._letter_places = dict(
            zip(self._letters, range(len(self._letters))))

    def __len__(self):
        return len(self._letters)

    def contains(self, char: str) -> bool:
        """Проверяет, присутствует ли символ char в алфавите"""
        return (char in self._letters)

    def letter_on_place(self, index: int) -> str:
        """Выдает букву, стояющую на месте index в алфавите (например 0 - a, 1 - b...)"""
        return self._letters[index]

    def place_of_letter(self, letter: str) -> int:
        """Выдает число, соотвествующее номеру буквы letter в алфавите"""
        return self._letter_places[letter]


class AffineCaesar(object):
    def __init__(self, alphabet: str):
        # Создаем объект mapper для алфавита
        self._mapper = AphabetMapper(alphabet)

    def _check_key(self, key: AffineCaesarKey):
        """Проверяет допустимость ключа для текущего алфавита (взаимно просты ли множитель и длина алфавита)"""
        if not utils.is_coprime(len(self._mapper), key.multiplier):
            raise BadKey(key)

    def _encrypt_char(self, char: str, key: AffineCaesarKey) -> str:
        """Зашифровать символ афинным шифром с помощью ключа key"""
        # Получаем позицию буквы
        pos = self._mapper.place_of_letter(char)
        # Шифруем (X * a + b) % m
        new_pos = (pos * key.multiplier + key.summand) % len(self._mapper)
        return self._mapper.letter_on_place(new_pos)

    def _decrypt_char(self, char: str, key: AffineCaesarKey) -> str:
        """Расшифровать символ с помощью ключа key"""
        # Вычисляем обратное множилею в ключе
        reverse_mult = utils.reverse_by_module(
            key.multiplier, len(self._mapper))
        # Получаем позицию буквы в алфавите
        pos = self._mapper.place_of_letter(char)
        # Расшифровывываем (a^-1 * (X - b) % m)
        new_pos = (reverse_mult * (pos - key.summand)) % len(self._mapper)
        # Возвращаем букву, находящуюся по новой позиции
        return self._mapper.letter_on_place(new_pos)

    def encrypt(self, string: str, key: AffineCaesarKey) -> str:
        """Зашифровать строку афинным шифром с помощью ключа key"""
        self._check_key(key)
        # Функия для шифрования только символов, которые есть в алфавите

        def enc_helper(char):
            # Если символ есть в алфавите
            if (self._mapper.contains(char)):
                # То шифруем
                return self._encrypt_char(char, key)
            else:
                # иначе выдаем символ напрямую
                return char
        # Применяем функцию ко всей строке
        return "".join(map(enc_helper, string))

    def decrypt(self, string: str, key: AffineCaesarKey) -> str:
        """Расшифровать строку с помощью ключа key"""
        self._check_key(key)
        # Функия для расшифрования только символов, которые есть в алфавите

        def dec_helper(char):
            # Если символ есть в алфавите
            if (self._mapper.contains(char)):
                # То расшифровываем
                return self._decrypt_char(char, key)
            else:
                # иначе выдаем символ напрямую
                return char
        # Применяем ко всей строке
        return "".join(map(dec_helper, string))
