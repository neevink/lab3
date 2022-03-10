import math

from func import FunctionForIntegration
from methods import SimpsonsMethod, TrapezoidalMethod, Method, DX, Result

FUNCTIONS = [
    FunctionForIntegration(
        lambda x: 2*x**3 - 9*x**2 - 7*x + 11,
        lambda x: 0.5*x**4 - 3*x**3 - 3.5*x**2 + 11*x,
        '2x^3 - 9x^2 - 7x + 11',
        None
    ),
    FunctionForIntegration(
        lambda x: 1/x + x,
        lambda x: math.log(abs(x)) + 0.5*x**2,
        '1/x + x',
        0
    ),
    FunctionForIntegration(
        lambda x: math.sin(2*x) / x,
        None,
        'sin(2x)/x',
        None,
    ),
]

METHODS = [
    TrapezoidalMethod(),
    SimpsonsMethod(),
]


def main():
    func = _handle_input_func()
    left, right, epsilon = _handle_input_intreval_epsilon()
    method = _handle_input_method()

    res = None
    try:
        if func.infinity_point is not None and left == func.infinity_point:
            res = method.solve(func, left + DX, right, epsilon)
        if func.infinity_point is not None and func.infinity_point == right:
            res = method.solve(func, left, right - DX, epsilon)
        elif func.infinity_point is not None and left < func.infinity_point < right:
            results_left = method.solve(func, left, func.infinity_point - DX, epsilon)
            results_right = method.solve(func, func.infinity_point + DX, right, epsilon)
            res = Result(results_left.value + results_right.value, max(results_left.partitions, results_right.partitions))
        else:
            res = method.solve(func, left, right, epsilon)
    except Exception:
        pass

    if res is None:
        print('Ошибка вычисления интеграла - функция не определена на всем интервале')
    else:
        print(res)

    if func.antiderivative is not None and res is not None:
        val = func.antiderivative(right) - func.antiderivative(left)
        print(f'Значение интеграла, вычисленное по формуле Ньютона-лейбница: {val}')

        print(f'Относительная погрешность равна: {abs(res.value - val)/val * 100:.2}%')


def _handle_input_method() -> Method:
    print('Метод на выбор:')
    for i in range(0, len(METHODS)):
        print(f'{i+1}. {METHODS[i]}')

    n = int(input('Введите номер метода: '))
    return METHODS[n-1]


def _handle_input_intreval_epsilon() -> map:
    return map(float, input('Введити диапазон и погрешность (0 1 0.01): ').split())


def _handle_input_func() -> FunctionForIntegration:
    print('Функция на выбор:')
    for i in range(0, len(FUNCTIONS)):
        print(f'{i+1}. {FUNCTIONS[i]}')

    n = int(input('Введите номер функции: '))
    return FUNCTIONS[n-1]


if __name__ == '__main__':
    main()
