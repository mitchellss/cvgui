"""This module contains interfaces for common UI objects."""
from typing import Any, Callable, List, Tuple
from typing_extensions import Protocol, runtime_checkable
import numpy as np


class Component(Protocol):
    """
    The base interface that defines what a component is.

    Components comprise the basic building blocks of an \
    activity's user interface.
    """

    pos: Tuple[float, float]
    """The position to render the component at."""

    def render(self, window: Any) -> None:
        """
        Render the component onto the specified window.

        Args:
            window (Any): Reference to the screen that the \
            selected component should be displayed upon.
        """


@runtime_checkable
class Button(Protocol):
    """Interface describing what a button must do."""

    pos: Tuple[float, float]
    """The position to render the component at."""

    activation_distance: float
    """The distance between an action and the button for the \
        button to be considered "clicked"."""

    targets: List[int]
    """The indices of the skeleton component that can \
        "click" the button."""

    callback: Callable
    """The function to execute when the button is clicked."""

    color: Tuple[int, int, int, int]
    """The color to make the button."""

    radius: int
    """The radius to make the button."""

    def is_clicked(self, pos: Tuple[float, float]) -> bool:  # type: ignore
        """Check whether or not the button is clicked given \
        the coordinates of an action.

        Args:
            pos (Tuple[float, float]): The position of the button as an \
            x,y tuple

        Returns:
            bool: True if the button is considered "clicked" for the given \
            conditions, False otherwise.
        """

    def render(self, window: Any) -> None:
        """Render the component on the given window.

        Args:
            window (Any): The space to render the component in.
        """


class HasButton(Protocol):
    """Interface describing what methods a gui must implement to \
        be used in the creation of a button."""

    def button(self, pos: Tuple[float, float],
               activation_distance: float,
               color: Tuple[int, int, int, int],
               radius: int
               ) -> Button:  # type: ignore
        """Create a button component.

        Args:
            pos (Tuple[float, float]): The position of the \
                button as an x,y tuple
            activation_distance (float): The minimum distance \
                between the target and the button to be considered \
                clicked
            color (Tuple[int, int, int, int]): rgba color value of \
                the button
            radius (int): Radius of the button

        Returns:
            Button: Component that implements the Button interface.
        """


@runtime_checkable
class TrackingBubble(Protocol):
    """Interface describing what methods a tracking bubble needs."""

    color: Tuple[int, int, int, int]
    """The color to make the tracking bubble."""

    radius: int
    """The radius to make the tracking bubble."""

    target: int
    """The index of the skeleton component that the \
        tracking bubble should follow."""

    pos: Tuple[float, float]
    """The position the tracking bubble should render at."""

    def render(self, window: Any) -> None:
        """Render the tracking bubble to the given window.

        Args:
            window (Any): The space to render the component in.
        """


class HasTrackingBubble(Protocol):
    """Interface describing what methods a gui must \
        implement to be used in the \
        creation of a tracking bubble."""

    def tracking_bubble(self,
                        target: int,
                        color: Tuple[int, int, int, int],
                        radius: int
                        ) -> TrackingBubble:  # type: ignore
        """Create an abstract tracking bubble."""


@runtime_checkable
class Skeleton(Protocol):
    """Interface describing how a component must act to be considered \
    a Skeleton."""

    pos: Tuple[float, float]
    scale: int
    skeleton_points: np.ndarray

    def render(self, window: Any) -> None:
        """Render the skeleton component on the given window."""


class HasSkeleton(Protocol):
    """Interface describing what methods a gui must implement to \
        be used in the creation of a skeleton."""

    def skeleton(self, pos: Tuple[float, float],
                 scale: int) -> Skeleton:  # type: ignore
        """Create an abstract skeleton.

        Args:
            pos (Tuple[float, float]): The position of the skeleton \
                as an x,y tuple
            scale (int): The scale to size the skeleton at.

        Returns:
            Skeleton: Object that implements the Skeleton interface.
        """


def button(gui: HasButton, pos: Tuple[float, float],
           activation_distance: float,
           radius: int,
           color: Tuple[int, int, int, int] = (100, 100, 100, 255)
           ) -> Button:
    """Create a button for any gui \
    that implements the HasButton interface. This method is used \
    instead of instantiating concrete types of ui components to \
    reduce the coupling between activity files and the gui being \
    used.

    Args:
        gui (HasButton): A gui that can create a button.
        pos (Tuple[float, float]): The position of the \
            button as an x,y tuple
        activation_distance (float): The minimum distance \
            between the target and the button to be considered \
            clicked
        color (Tuple[int, int, int, int]): rgba color value of \
            the button
        radius (int): Radius of the button

    Returns:
        Button: The button implementation for the respective gui.
    """
    return gui.button(pos=pos,
                      activation_distance=activation_distance,
                      color=color, radius=radius)


def skeleton(gui: HasSkeleton, pos: Tuple[float, float],
             scale: int) -> Skeleton:
    """Create a skeleton for any gui \
    that implements the HasSkeleton interface. This method is used \
    instead of instantiating concrete types of ui components to \
    reduce the coupling between activity files and the gui being \
    used.

    Args:
        gui (HasButton): A gui that can create a skeleton.
        pos (Tuple[float, float]): The position of the skeleton as an \
            x,y tuple

    Returns:
        Skeleton: The skeleton implementation for the respective gui.
    """
    return gui.skeleton(pos=pos, scale=scale)


def tracking_bubble(gui: HasTrackingBubble,
                    radius: int,
                    target: int,
                    color: Tuple[int, int, int, int] = (100, 100, 100, 255)
                    ) -> TrackingBubble:
    """Create a tracking bubble.

    Args:
        gui (HasTrackingBubble): A gui that can create a tracking bubble.
        radius (int): The radius of the bubble.
        target (int): The target for the bubble to track.
        color (Tuple[int, int, int, int], optional): The color of the bubble.
                Defaults to (100, 100, 100, 255).

    Returns:
        TrackingBubble: The tracking bubble implementation for the \
            respective gui.
    """
    return gui.tracking_bubble(color=color, radius=radius, target=target)
