"""User interface implementation of PyGame."""
import sys
from typing import Callable, List, Literal
import pygame
from pygame.constants import QUIT
import numpy as np
from cvgui.core.displaying.components import Button, Skeleton


class PyGameUI:
    """User interface implementation of PyGame."""
    BACKGROUND: tuple[Literal[0], Literal[0], Literal[0]] = (0, 0, 0)

    window: pygame.surface.Surface
    fps_clock: pygame.time.Clock

    def __init__(self, height: int, width: int, fps: int) -> None:
        self.width: int = width
        self.height: int = height
        self.fps: int = fps

    def clear(self) -> None:
        """Clears the pygame window by filling it with
        a single color."""
        self.window.fill(self.BACKGROUND)

    def update(self) -> None:
        """Updates the PyGame window."""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        self.fps_clock.tick(self.fps)

    def button(self, x_coord: float, y_coord: float,
               activation_distance: float) -> Button:
        """Creates a PyGame button at the specified location."""
        return PyGameButton(x_coord=x_coord, y_coord=y_coord,
                            activation_distance=activation_distance)

    def skeleton(self, x_coord: float, y_coord: float, scale: int) -> Skeleton:
        """Creates a PyGame skeleton at the specified location."""
        return PyGameSkeleton(x_coord=x_coord, y_coord=y_coord, scale=scale)

    def new_gui(self) -> None:
        """Initializes the PyGame user interface."""
        pygame.init()
        pygame.font.init()

        # Game Setup
        self.fps_clock = pygame.time.Clock()

        self.window: pygame.surface.Surface = pygame.display.set_mode(
            (self.width, self.height))
        pygame.display.set_caption("cvgui")
        self.window.fill(self.BACKGROUND)


class PyGameButton:
    """Button implementation for PyGame."""

    def __init__(self, x_coord: float, y_coord: float,
                 activation_distance: float) -> None:
        """Creates a new PyGameButton at the location specified."""
        self.x_coord: float = x_coord
        self.y_coord: float = y_coord
        self.activation_distance: float = activation_distance
        self.targets: List[int]
        self.callback: Callable

    def is_clicked(self, x_coord: float, y_coord: float, distance: float) -> bool:
        """Checks if the button has been clicked."""
        if abs(self.x_coord - x_coord) > distance or abs(self.y_coord - y_coord) > distance:
            return False
        return True

    def set_targets(self, targets: List[int]):
        """Sets targets."""
        self.targets = targets

    def set_callback(self, callback: Callable):
        """Sets callback function."""
        self.callback = callback

    def render(self, window) -> None:
        """Draws the button on the pygame window."""
        pygame.draw.circle(
            window, pygame.color.Color(255, 0, 0, 255),
            (self.x_coord, self.y_coord),
            100
        )


class PyGameSkeleton:
    """Skeleton implementation in PyGame."""

    # Where to connect limbs. Refer to here
    # https://mediapipe.dev/images/mobile/pose_tracking_full_body_landmarks.png
    # TODO: Move this somewhere else
    CONNECTIONS: np.ndarray = np.array([
        [16, 14], [16, 18], [16, 20], [16, 22],
        [18, 20], [14, 12], [12, 11], [12, 24],
        [11, 23], [11, 13], [15, 13], [15, 17],
        [15, 19], [15, 21], [17, 19], [24, 23],
        [26, 24], [26, 28], [25, 23], [25, 27],
        [10, 9], [8, 6], [5, 6], [5, 4], [0, 4],
        [0, 1], [2, 1], [2, 3], [3, 7], [28, 32],
        [28, 30], [27, 29], [27, 31], [32, 30],
        [29, 31]
    ])

    LIMB_COLOR: tuple[Literal[255], Literal[255],
                      Literal[255]] = (255, 255, 255)
    LIMB_WIDTH: Literal[2] = 2

    LANDMARK_COLOR: tuple[Literal[0], Literal[255], Literal[0]] = (0, 255, 0)
    LANDMARK_RADIUS: Literal[5] = 5
    LANDMARK_OUTLINE_WIDTH: Literal[0] = 0

    NUM_LANDMARKS: Literal[33] = 33
    POINTS_PER_LANDMARK: Literal[4] = 4  # x, y, z, depth?

    def __init__(self, x_coord: float, y_coord: float, scale: int) -> None:
        """Creates a new PyGame skeleton."""
        self.x_coord: float = x_coord
        self.y_coord: float = y_coord
        self.skeleton_points: np.ndarray = np.zeros((33, 4))
        self.scale = scale

    def render(self, window) -> None:
        """Draws the skeleton on the pygame window."""
        for landmark_pair in self.CONNECTIONS:
            start_landmark: int = landmark_pair[0]
            end_landmark: int = landmark_pair[1]
            line_start_x: float = self.skeleton_points[start_landmark][0]
            line_start_y: float = self.skeleton_points[start_landmark][1]
            line_end_x: float = self.skeleton_points[end_landmark][0]
            line_end_y: float = self.skeleton_points[end_landmark][1]
            pygame.draw.line(window, self.LIMB_COLOR, [float(line_start_x), float(line_start_y)],
                             [float(line_end_x), float(line_end_y)], self.LIMB_WIDTH)

        for _, landmark in enumerate(self.skeleton_points):
            point_x: float = landmark[0]
            point_y: float = landmark[1]
            pygame.draw.circle(window, self.LANDMARK_COLOR, [
                               point_x, point_y], self.LANDMARK_RADIUS, self.LANDMARK_OUTLINE_WIDTH)
