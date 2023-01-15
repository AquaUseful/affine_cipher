import math


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Расширенный алгоритм Евклида, возврашает коэффициенты Безу и НОД"""
    if (b == 0):
        return (1, 0, a)
    y, x, gcd = extended_gcd(b, a % b)
    return (x, y - (a // b) * x, gcd)


def reverse_by_module(a: int, module: int):
    """Возвращает число b обратное a по модулю module, т.е. (a * b) % mod == 1"""
    return extended_gcd(a, module)[0]


def is_coprime(a: int, b: int):
    """Возвращает true, если a и b - взамно простые"""
    return (math.gcd(a, b) == 1)
