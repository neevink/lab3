import math

from func import FunctionForIntegration
from methods import SimpsonsMethod, TrapezoidalMethod, Method, DX, Result

FUNCTIONS = [
    FunctionForIntegration(
        lambda x: 2*x**3 - 9*x**2 - 7*x + 11,
        lambda x: 0.5*x**4 - 3*x**3 - 3.5*x**2 + 11*x,
        '2x^3 - 9x^2 - 7x + 11',
        None,
    ),
    FunctionForIntegration(
        lambda x: x ** 3 - x,
        lambda x: 0.25 * x**4 - 0.5*x**2,
        'x^3 -x',
        None,
    ),
    FunctionForIntegration(
        lambda x: x*math.exp(x),
        lambda x: x*math.exp(x) - math.exp(x),
        'x * e^x',
        None,
    ),
    FunctionForIntegration(
        lambda x: math.sin(2 * x) / x,
        None,
        'sin(2x)/x',
        0,
    ),
    FunctionForIntegration(
        lambda x: 1/x + x,
        lambda x: math.log(abs(x)) + 0.5*x**2,
        '1/x + x',
        0,
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

    try:
        if func.gap_point is not None and left == func.gap_point:
            res = method.solve(func, left + DX, right, epsilon)
        elif func.gap_point is not None and func.gap_point == right:
            res = method.solve(func, left, right - DX, epsilon)
        elif func.gap_point is not None and left < func.gap_point < right:
            results_left = method.solve(func, left, func.gap_point - DX, epsilon)
            results_right = method.solve(func, func.gap_point + DX, right, epsilon)

            if results_left is None or results_right is None:
                res = None
            else:
                res = Result(
                    results_left.value + results_right.value,
                    max(results_left.partitions, results_right.partitions),
                )
        else:
            res = method.solve(func, left, right, epsilon)
    except Exception as exc:
        raise exc

    if res is None:
        print('Ошибка вычисления интеграла - функция не определена на всем интервале')
    else:
        print(res)

    if func.antiderivative is not None and res is not None:
        val = func.antiderivative(right) - func.antiderivative(left)
        print(f'Значение интеграла, вычисленное по формуле Ньютона-лейбница: {val}')

        if val != 0:
            print(f'Относительная погрешность равна: {abs((res.value - val)/val) * 100:.4f}%')


def _handle_input_method() -> Method:
    print('Метод на выбор:')
    for i in range(0, len(METHODS)):
        print(f'{i+1}. {METHODS[i]}')

    n = int(input('Введите номер метода: '))
    return METHODS[n-1]


def _handle_input_intreval_epsilon() -> map:
    return map(float, input('Введити диапазон и погрешность (-1 1 0.01): ').split())


def _handle_input_func() -> FunctionForIntegration:
    print('Функция на выбор:')
    for i in range(0, len(FUNCTIONS)):
        print(f'{i+1}. {FUNCTIONS[i]}')

    n = int(input('Введите номер функции: '))
    return FUNCTIONS[n-1]


if __name__ == '__main__':
    main()
