from typing import Callable, Union

import attr


@attr.s
class FunctionForIntegration:
    function: Callable = attr.ib()
    antiderivative: Union[Callable, None] = attr.ib()
    display: str = attr.ib()
    gap_point: Union[float, None] = attr.ib()

    def __str__(self) -> str:
        return self.display
