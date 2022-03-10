from abc import ABC, abstractmethod
from typing import Callable, Union

import attr

from func import FunctionForIntegration


MAX_PARTITIONS_COUNT = 65536
DX = 1e-10


@attr.s
class Result:
    value: float = attr.ib()
    partitions: int = attr.ib()

    def __str__(self) -> str:
        return f'''Значение интеграла: {self.value}\nКоличество интервалов: {self.partitions}'''


@attr.s
class Method(ABC):
    _name: str = attr.ib()
    _k: int = attr.ib()  # порядок точности квадратурной формулы для рассчёта погрешности по правилу Рунге

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def _integrate(self, f: Callable, a: float, b: float, partitions: int) -> float:
        raise NotImplementedError()

    def _iterate(self, func: Callable, a: float, b: float, epsilon: float) -> tuple:
        partitions = 4
        last = self._integrate(func, a, b, partitions)
        while True:
            partitions *= 2
            current = self._integrate(func, a, b, partitions)
            diff = abs(current - last) / (2**self._k - 1)
            if diff < epsilon:
                break
            if partitions >= MAX_PARTITIONS_COUNT:
                break
            last = current
        return current, partitions

    def solve(self, function: FunctionForIntegration, a: float, b: float, epsilon: float) -> Union[Result, None]:
        res, partitions = self._iterate(function.function, a, b, epsilon)
        if partitions == MAX_PARTITIONS_COUNT:
            return None
        return Result(res, partitions)

    def __str__(self):
        return self._name


class TrapezoidalMethod(Method):
    def __init__(self):
        self._name = 'Метод Трапеций'
        self._k = 2

    def _integrate(self, f: Callable, a: float, b: float, partitions: int) -> float:
        step = (b - a) / partitions
        result = (f(a) + f(b)) / 2
        x = a + step
        while x < b:
            result += f(x)
            x += step
        return result * step


class SimpsonsMethod(Method):
    def __init__(self):
        self._name = 'Метод Симпсона'
        self._k = 4

    def _integrate(self, f: Callable, a: float, b: float, partitions: int) -> float:
        step = (b - a) / partitions
        result = f(a) + f(b)
        x = a + step
        i = 1
        while x < b:
            result += (4 * f(x) if (i % 2 != 0) else 2 * f(x))
            x += step
            i += 1
        return result * step / 3
