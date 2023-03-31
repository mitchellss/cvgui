"""User interface implementation of PyGame."""
from cvgui.core.displaying.components import Button, Skeleton, TrackingBubble
import numpy as np
from pygame.constants import QUIT
import pygame
import math
from typing import Any, Callable, List, Literal, Tuple

X = 0
Y = 1


class PyGameUI:
    """User interface implementation of PyGame."""
    BACKGROUND: tuple[Literal[0], Literal[0], Literal[0]] = (0, 0, 0)

    window: pygame.surface.Surface
    fps_clock: pygame.time.Clock
    running: bool

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
        pygame.display.update()
        self.fps_clock.tick(self.fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                self.running = False

    def button(self, pos: Tuple[float, float],
               activation_distance: float,
               color: Tuple[int, int, int, int],
               radius: int = 100) -> Button:
        """Creates a PyGame button at the specified location."""
        return PyGameButton(pos=pos, activation_distance=activation_distance,
                            color=color, radius=radius)

    def skeleton(self, pos: Tuple[float, float], scale: int) -> Skeleton:
        """Creates a PyGame skeleton at the specified location."""
        return PyGameSkeleton(pos=pos, scale=scale)

    def tracking_bubble(self,
                        target: int,
                        color: Tuple[int, int, int, int],
                        radius: int = 100
                        ) -> TrackingBubble:
        return PyGameTrackingBubble(color=color, target=target, radius=radius)

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
        self.running = True


class PyGameTrackingBubble:

    def __init__(self,
                 color: Tuple[int, int, int, int],
                 radius: int,
                 target: int) -> None:
        self.color = color
        self.radius = radius
        self.target = target
        self.pos: Tuple[float, float] = (0, 0)

    def render(self, window: Any) -> None:
        color = pygame.color.Color(
            self.color[0], self.color[1],
            self.color[2], self.color[3])
        pygame.draw.circle(
            window, color,
            (self.pos[X], self.pos[Y]),
            self.radius
        )


class PyGameButton:
    """Button implementation for PyGame."""

    def __init__(self, pos: Tuple[float, float],
                 activation_distance: float,
                 color: Tuple[int, int, int, int],
                 radius: int) -> None:
        """Creates a new PyGameButton at the location specified."""
        self.pos = pos
        self.activation_distance: float = activation_distance
        self.targets: List[int]
        self.callback: Callable
        self.color: Tuple[int, int, int, int] = color
        self.radius: int = radius

    def is_clicked(self, pos: Tuple[float, float]) -> bool:
        """Checks if the button has been clicked."""
        if abs(self.pos[X] - pos[X]) > self.activation_distance \
                or abs(self.pos[Y] - pos[Y]) > self.activation_distance:
            return False
        if math.sqrt((self.pos[X] - pos[X])**2 + (self.pos[Y] - pos[Y])**2) \
                > self.activation_distance:
            return False
        return True

    def render(self, window) -> None:
        """Draws the button on the pygame window."""
        color = pygame.color.Color(
            self.color[0], self.color[1],
            self.color[2], self.color[3])
        pygame.draw.circle(
            window, color,
            (self.pos[X], self.pos[Y]),
            self.radius
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

    def __init__(self, pos: Tuple[float, float], scale: int) -> None:
        """Creates a new PyGame skeleton."""
        self.pos = pos
        self.skeleton_points: np.ndarray = np.zeros((33, 4))
        self.scale = scale

    def render(self, window) -> None:
        """Draws the skeleton on the pygame window."""
        for landmark_pair in self.CONNECTIONS:
            start_landmark: int = landmark_pair[X]
            end_landmark: int = landmark_pair[Y]
            line_start_x: float = self.skeleton_points[start_landmark][X]
            line_start_y: float = self.skeleton_points[start_landmark][Y]
            line_end_x: float = self.skeleton_points[end_landmark][X]
            line_end_y: float = self.skeleton_points[end_landmark][Y]
            pygame.draw.line(window, self.LIMB_COLOR,
                             [float(line_start_x), float(line_start_y)],
                             [float(line_end_x), float(line_end_y)],
                             self.LIMB_WIDTH)

        for _, landmark in enumerate(self.skeleton_points):
            point_x: float = landmark[X]
            point_y: float = landmark[Y]
            pygame.draw.circle(window, self.LANDMARK_COLOR,
                               [point_x, point_y],
                               self.LANDMARK_RADIUS,
                               self.LANDMARK_OUTLINE_WIDTH)
