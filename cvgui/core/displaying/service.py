"""The interface to implement to be considered a user interface."""
from typing import Any, Callable, List
from typing_extensions import Protocol

from cvgui.core.displaying.components import Button, Skeleton


class UserInterface(Protocol):
    """An abstract user interface capable of rendering components."""
    window: Any

    def clear(self) -> None:
        """Resets the user interface display."""

    def new_gui(self) -> None:
        """Sets up the user interface."""

    def button(self, x_coord: float, y_coord: float,
               activation_distance: float) -> Button:  # type: ignore
        """Creates a new button on the user interface at the location specfied."""

    def skeleton(self, x_coord: float, y_coord: float) -> Skeleton:  # type: ignore
        """Creates a new skeleton on the user interface at the location specfied."""

    def update(self) -> None:
        """Refreshes the user interface display."""
