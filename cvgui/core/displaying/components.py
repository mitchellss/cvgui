"""
Interfaces for common UI objects.

Abstract components to be implemented by concrete
GUI classes and interafaces that require the implementation
of said classes.
"""
from typing import Any, Callable, List
from typing_extensions import Protocol, runtime_checkable
import numpy as np


class Component(Protocol):
    """The base interface that defines what a component is.
    In order to be a component, an object must have x and
    y coordinates and be able to be rendered."""
    x_coord: float
    y_coord: float

    def render(self, window: Any) -> None:
        """Renders the component onto the specified window.

        Args:
            window (Any): Reference to the screen that the
            selected component should be displayed upon.
        """


@runtime_checkable
class Button(Protocol):
    """Interface describing what a button must do."""
    x_coord: float
    y_coord: float
    activation_distance: float
    targets: List[int]
    callback: Callable

    def is_clicked(self, x_coord: float, y_coord: float) -> bool:  # type: ignore
        """Method to check whether or not the button is clicked given
        the coordinates of an action

        Args:
            x_coord (float): The x coordinate of an action.
            y_coord (float): The y coordinate of an action.

        Returns:
            bool: True if the button is considered "clicked" for the given
            conditions, False otherwise.
        """

    def set_targets(self, targets: List[int]):
        """Sets the targets for the button."""

    def set_callback(self, callback: Callable):
        """Sets the callback function for the button."""

    def render(self, window: Any) -> None:
        """Required method to fulfill the requirements of the
        Component interface."""


class HasButton(Protocol):
    """
    Interface describing what methods a gui must implement to be used in the
    creation of a button.
    """

    def button(self, x_coord: float, y_coord: float,
               activation_distance: float) -> Button:  # type: ignore
        """Creates an abstract button.

        Args:
            x_coord (float): x coordinate of the button.
            y_coord (float): y coordinate of the button.

        Returns:
            Button: Object that implements the Button interface.
        """


@runtime_checkable
class Skeleton(Protocol):
    """
    Interface describing how a component must act to be considered
    a Skeleton.
    """
    x_coord: float
    y_coord: float
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

    def skeleton(self, x_coord: float, y_coord: float, scale: int) -> Skeleton:  # type: ignore
        """Creates an abstract skeleton

        Args:
            x_coord (float): x coordinate of the skeleton center point
            y_coord (float): y coordinate of the skeleton center point

        Returns:
            Skeleton: Object that implements the Skeleton interface.
        """


def button(gui: HasButton, x_coord: float, y_coord: float,
           activation_distance: float) -> Button:
    """Function that can be called to create a button for any gui
    that implements the HasButton interface. This method is used
    instead of instantiating concrete types of ui components to
    reduce the coupling between activity files and the gui being
    used.

    Args:
        gui (HasButton): A gui that can create a button.
        x_coord (float): The x coordinate of the button to be created.
        y_coord (float): The y coordinate of the button to be created.

    Returns:
        Button: The button implementation for the respective gui.
    """
    return gui.button(x_coord=x_coord, y_coord=y_coord,
                      activation_distance=activation_distance)


def skeleton(gui: HasSkeleton, x_coord: float, y_coord: float, scale: int) -> Skeleton:
    """Function that can be called to create a skeleton for any gui
    that implements the HasSkeleton interface. This method is used
    instead of instantiating concrete types of ui components to
    reduce the coupling between activity files and the gui being
    used.

    Args:
        gui (HasButton): A gui that can create a skeleton.
        x_coord (float): The x coordinate of the skeleton to be created.
        y_coord (float): The y coordinate of the skeleton to be created.

    Returns:
        Skeleton: The skeleton implementation for the respective gui.
    """
    return gui.skeleton(x_coord=x_coord, y_coord=y_coord, scale=scale)
