"""The interface to implement to be considered a user interface."""
from typing import Any, Tuple
from typing_extensions import Protocol

from cvgui.core.displaying.components import Button, Skeleton


class UserInterface(Protocol):
    """An abstract user interface capable of rendering components."""
    window: Any

    def clear(self) -> None:
        """Resets the user interface display."""

    def new_gui(self) -> None:
        """Sets up the user interface."""

    def button(self, pos: Tuple[float, float],
               activation_distance: float,
               color: Tuple[int, int, int, int],
               radius: int) -> Button:  # type: ignore
        """
        Creates a new button on the user
        interface at the location specfied.
        """

    def skeleton(self, pos: Tuple[float, float],
                 scale: int) -> Skeleton:  # type: ignore
        """
        Creates a new skeleton on the user
        interface at the location specfied.
        """

    def update(self) -> None:
        """Refreshes the user interface display."""
