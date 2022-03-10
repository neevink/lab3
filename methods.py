import math
from typing import Callable, Optional

import attr

from func import FunctionForIntegration


MAX_PARTITIONS_COUNT = 65536
DX = 1e-10


def value_or_none(function, x) -> Optional[float]:
    try:
        value = function(x)
        if math.isfinite(value):
            return value
    except ZeroDivisionError:
        pass


def calculate_value(function, x):
    value = value_or_none(function, x)
    if value is not None:
        return value
    left_limit = value_or_none(function, x - DX)
    right_limit = value_or_none(function, x + DX)
    if (left_limit is None) or (right_limit is None):
        return None
    else:
        return (left_limit + right_limit) / 2


@attr.s
class Result:
    value: float = attr.ib()
    partitions: int = attr.ib()

    def __str__(self):
        return f'''Значение интеграла: {self.value}\nКоличество интервалов: {self.partitions}'''


@attr.s
class Method:  # TODO make abstract
    name: str = attr.ib()
    k: int = attr.ib()  # порядок точности квадратурной формулы для рассчёта погрешности по правилу Рунге

    def _integrate(self, f: Callable, a: float, b: float, partitions: int) -> float:
        pass

    def _iterate(self, func: Callable, a: float, b: float, epsilon: float):
        partitions = 2  # 2 на предыдущем, 4 на этом
        last = self._integrate(func, a, b, partitions)
        while True:
            partitions *= 2
            current = self._integrate(func, a, b, partitions)
            diff = abs(current - last) / (2**self.k - 1)
            if diff < epsilon:
                break
            if partitions >= MAX_PARTITIONS_COUNT:
                break
            last = current
        return current, partitions

    def solve(self, function: FunctionForIntegration, a: float, b: float, epsilon: float) -> Result:
        res, partitions = self._iterate(function.function, a, b, epsilon)
        if partitions == MAX_PARTITIONS_COUNT:
            return None
        return Result(res, partitions)

    def __str__(self):
        return self.name


class TrapezoidalMethod(Method):
    def __init__(self):
        self.name = 'Метод Трапеций'
        self.k = 2

    def _integrate(self, f: Callable, a: float, b: float, partitions: int) -> float:
        step = (b - a) / partitions
        result = (calculate_value(f, a) + calculate_value(f, b)) / 2
        x = a + step
        while x < b:
            result += calculate_value(f, x)
            x += step
        return result * step


class SimpsonsMethod(Method):
    def __init__(self):
        self.name = 'Метод Симпсона'
        self.k = 4

    def _integrate(self, f: Callable, a: float, b: float, partitions: int) -> float:
        step = (b - a) / partitions
        result = calculate_value(f, a) + calculate_value(f, b)
        x = a + step
        i = 1
        while x < b:
            result += (4 * calculate_value(f, x) if (i % 2 != 0) else 2 * calculate_value(f, x))
            x += step
            i += 1
        return result * step / 3
