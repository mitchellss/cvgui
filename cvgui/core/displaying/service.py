"""This module defines the interface for a class to be considered \
a user interface by `cvgui`. This ensures that all user-created \
activities work reguardless of what user interface is used."""
from typing import Any, Tuple
from typing_extensions import Protocol

from cvgui.core.displaying.components import Button, Skeleton, TrackingBubble


class UserInterface(Protocol):
    """An abstract user interface capable of rendering components."""

    window: Any
    """The window to render componets onto."""

    running: bool
    """Whether the user interface should continue rendering."""

    def clear(self) -> None:
        """Reset the user interface display."""

    def new_gui(self) -> None:
        """Set up the user interface."""

    def button(self, pos: Tuple[float, float],
               activation_distance: float,
               color: Tuple[int, int, int, int],
               radius: int) -> Button:  # type: ignore
        """Create a circular button on the user \
        interface.

        Args:
            pos (Tuple[float, float]): The coordinates \
                to render the button at.
            activation_distance (float): The distance \
                from the target to the button to be \
                    considered a click.
            color (Tuple[int, int, int, int]): The color \
                of the button.
            radius (int): The radius of the button \

        Returns:
            Button: Button component with the specified settings.
        """

    def skeleton(self, pos: Tuple[float, float],
                 scale: int) -> Skeleton:  # type: ignore
        """Create a new skeleton on the user \
        interface at the location specfied.

        Args:
            pos (Tuple[float, float]): The coordinates \
                to center the skeleton at.
            scale (int): How much to scale the skeleton \
                points by.

        Returns:
            Skeleton: Skeleton component with the specified settings.
        """

    def tracking_bubble(
        self,
        target: int,
        color: Tuple[int, int, int, int],
        radius: int
    ) -> TrackingBubble:  # type: ignore
        """Create a new tracking bubble on the user \
        interface that tracks the given point.

        Args:
            target (int): Index of the skeleton point that the \
                tracking bubble should follow.
            color (Tuple[int, int, int, int]): The color of the \
                tracking bubble.
            radius (int): The radius of the tracking bubble.

        Returns:
            TrackingBubble: TrackingBubble component with the \
                specified settings.
        """

    def update(self) -> None:
        """Refresh the user interface display."""
