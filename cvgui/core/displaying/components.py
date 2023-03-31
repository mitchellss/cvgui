"""
Interfaces for common UI objects.

Abstract components to be implemented by concrete
GUI classes and interafaces that require the implementation
of said classes.
"""
from typing import Any, Callable, List, Tuple
from typing_extensions import Protocol, runtime_checkable
import numpy as np


class Component(Protocol):
    """The base interface that defines what a component is.
    In order to be a component, an object must have x and
    y coordinates and be able to be rendered."""
    pos: Tuple[float, float]

    def render(self, window: Any) -> None:
        """Renders the component onto the specified window.

        Args:
            window (Any): Reference to the screen that the
            selected component should be displayed upon.
        """


@runtime_checkable
class Button(Protocol):
    """Interface describing what a button must do."""
    pos: Tuple[float, float]
    activation_distance: float
    targets: List[int]
    callback: Callable
    color: Tuple[int, int, int, int]
    radius: int

    def is_clicked(self, pos: Tuple[float, float]) -> bool:  # type: ignore
        """Method to check whether or not the button is clicked given
        the coordinates of an action

        Args:
            pos (Tuple[float, float]): The position of the button as an
            x,y tuple

        Returns:
            bool: True if the button is considered "clicked" for the given
            conditions, False otherwise.
        """

    def render(self, window: Any) -> None:
        """Required method to fulfill the requirements of the
        Component interface."""


class HasButton(Protocol):
    """
    Interface describing what methods a gui must implement to be used in the
    creation of a button.
    """

    def button(self, pos: Tuple[float, float],
               activation_distance: float,
               color: Tuple[int, int, int, int],
               radius: int
               ) -> Button:  # type: ignore
        """Creates an abstract button.

        Args:
            pos (Tuple[float, float]): The position of the
                button as an x,y tuple
            activation_distance (float): The minimum distance
                between the target and the button to be considered
                clicked
            color (Tuple[int, int, int, int]): rgba color value of
                the button
            radius (int): Radius of the button

        Returns:
            Button: Object that implements the Button interface.
        """


@runtime_checkable
class TrackingBubble(Protocol):
    """
    Interface describing what methods a tracking bubble needs.
    """
    color: Tuple[int, int, int, int]
    radius: int
    target: int
    pos: Tuple[float, float]

    def render(self, window: Any) -> None:
        """Required method to fulfill the requirements of the
        Component interface."""


class HasTrackingBubble(Protocol):
    """
    Interface describing what methods a gui must implement to be used in the
    creation of a tracking bubble.
    """

    def tracking_bubble(self,
                        target: int,
                        color: Tuple[int, int, int, int],
                        radius: int
                        ) -> TrackingBubble:  # type: ignore
        """Creates an abstract tracking bubble"""


@runtime_checkable
class Skeleton(Protocol):
    """
    Interface describing how a component must act to be considered
    a Skeleton.
    """
    pos: Tuple[float, float]
    scale: int
    skeleton_points: np.ndarray

    def render(self, window: Any):
        """Required method to fulfill the requirements of the
        Component interface."""


class HasSkeleton(Protocol):
    """
    Interface describing what methods a gui must implement to be used in the
    creation of a skeleton.
    """

    def skeleton(self, pos: Tuple[float, float],
                 scale: int) -> Skeleton:  # type: ignore
        """Creates an abstract skeleton

        Args:
            pos (Tuple[float, float]): The position of the skeleton as an
            x,y tuple

        Returns:
            Skeleton: Object that implements the Skeleton interface.
        """


def button(gui: HasButton, pos: Tuple[float, float],
           activation_distance: float,
           radius: int,
           color: Tuple[int, int, int, int] = (100, 100, 100, 255)
           ) -> Button:
    """Function that can be called to create a button for any gui
    that implements the HasButton interface. This method is used
    instead of instantiating concrete types of ui components to
    reduce the coupling between activity files and the gui being
    used.

    Args:
        gui (HasButton): A gui that can create a button.
        pos (Tuple[float, float]): The position of the
            button as an x,y tuple
        activation_distance (float): The minimum distance
            between the target and the button to be considered
            clicked
        color (Tuple[int, int, int, int]): rgba color value of
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
    """Function that can be called to create a skeleton for any gui
    that implements the HasSkeleton interface. This method is used
    instead of instantiating concrete types of ui components to
    reduce the coupling between activity files and the gui being
    used.

    Args:
        gui (HasButton): A gui that can create a skeleton.
        pos (Tuple[float, float]): The position of the skeleton as an
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
    """Function that can be called to create a tracking bubble.

    Args:
        gui (HasTrackingBubble): A gui that can create a tracking bubble.
        radius (int): The radius of the bubble.
        target (int): The target for the bubble to track.
        color (Tuple[int, int, int, int], optional): The color of the bubble.
                Defaults to (100, 100, 100, 255).

    Returns:
        _type_: _description_
    """
    return gui.tracking_bubble(color=color, radius=radius, target=target)
