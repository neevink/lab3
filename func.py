from typing import Callable, Union

import attr


@attr.s
class FunctionForIntegration:
    function: Callable = attr.ib()
    antiderivative: Union[Callable, None] = attr.ib()  # Первообразная
    display: str = attr.ib()
    infinity_point: Union[float, None] = attr.ib()  # Точка разрыва

    def __str__(self):
        return self.display
