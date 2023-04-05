"""
Operates on a collection of related scenes to create a specific experience.

The activity module orchestrates the interfaces of `core` packages
to run concurrently and create a coherent flow of information.
"""
import sys
from typing import Iterable

import numpy as np
import multiprocessing as mp

from cvgui.activity.scene import Scene
from cvgui.core.displaying import UserInterface
from cvgui.core.displaying.components import Button, Skeleton, TrackingBubble
from cvgui.core.recieving import PoseGenerator

X = 0
Y = 1


class Activity:
    """A collection of scenes and the abstract logic
    for their interaction."""

    # Private variables
    _scenes: Iterable[Scene] = []

    _active_scene: int = 0
    """The index of the scene to render."""

    pose_loggers: Iterable[cvgui.PoseLogger] = []

    def __init__(self, pose_input: PoseGenerator,
                 frontend: UserInterface) -> None:
        """
        Args:
            pose_input (PoseGenerator): An object that can generate poses.
            frontend (UserInterface): An object that can create a
                user interface.
        """
        self.pose_input: PoseGenerator = pose_input
        self.frontend: UserInterface = frontend

    def add_scene(self, scene: Scene) -> None:
        """Adds a scene to the activity.

        Args:
            scene (Scene): The scene to add
            to the activity.
        """
        self._scenes.append(scene)
    
    def add_logger(self, logger: cvgui.PoseLogger) -> None:
        self.pose_loggers.append(logger)

    def next_scene(self) -> None:
        """
        Sets the active scene to the next scene in the scene array.
        Circles back to the first scene if current active scene is the
        last in the array.
        """
        self._active_scene += 1
        if self._active_scene > len(self._scenes) - 1:
            self._active_scene = 0

    def previous_scene(self) -> None:
        """
        Sets the active scene to the previous scene in the scene array.
        Circles back to the last scene if current active scene is the
        first in the array.
        """
        self._active_scene -= 1
        if self._active_scene < 0:
            self._active_scene = len(self._scenes) - 1

    def set_scene(self, scene_num: int) -> bool:
        """
        Sets the active scene to the one specified by the given index.
        Returns true if the scene switch was successful, false otherwise.

        Args:
            scene_num (int): Index of the scene to switch to.
        """
        if scene_num < 0 or scene_num > len(self._scenes) - 1:
            return False
        self._active_scene = scene_num
        return True

    def run(self) -> None:
        """
        Infinitely retrieves pose data and
        renders the components of added scenes.
        """
        processes: Iterable[mp.Process] = []

        # Create a queue to allow the UI to 
        # recieve pose data.
        ui_pose_queue = mp.Queue()
        pose_queues: Iterable[mp.Queue] = [ui_pose_queue]

        # Create a queue for each of the pose loggers
        # to recieve pose data.
        for logger in self.pose_loggers:
            queue = mp.Queue()
            pose_queues.append(queue)
            processes += logger.start(queue)

        # Start the pose input process. This will start sending pose data
        # to all the queues specified above.
        processes += self.pose_input.start(pose_queues)

        try:
            self.update_ui(ui_pose_queue)
        except KeyboardInterrupt:
            print("Ctrl-C pressed. Exiting...")
            for process in processes:
                process.kill()
            sys.exit(0)
        except Exception as excpt:
            for process in processes:
                process.kill()
            raise excpt

        print("Pygame closed. Exiting...")
        for process in processes:
            process.kill()

    def update_ui(self, pose_queue: mp.Queue):
        """Infinitely attempts to render the most current
        version of the active scene of the user interface.
        Intended to run in a sub-process to update the ui
        concurrently while retrieving new data.

        Args:
            frontend (UserInterface): The user interface to update.
            scenes (List[Scene]): The scenes for the activity being rendered.
        """
        self.frontend.new_gui()
        pose_points: np.ndarray = np.zeros((33, 4))
        while self.frontend.running:
            self.frontend.clear()

            # Make sure the skeleton is updated first if it exists.
            # That way button clicks aren't a frame late
            for component in self._scenes[self._active_scene].components:
                if isinstance(component, Skeleton):
                    if pose_queue.empty():
                        continue
                    pose_points = pose_queue.get()
                    # Scale the skeleton points and offset them
                    pose_points[:, X] = pose_points[:, X] * \
                        component.scale + component.pos[X]
                    pose_points[:, Y] = pose_points[:, Y] * \
                        component.scale + component.pos[Y]
                    component.skeleton_points = pose_points
                    break

            for component in self._scenes[self._active_scene].components:
                if isinstance(component, Button):
                    for target in component.targets:
                        if component.is_clicked(
                                pos=(pose_points[target][X],
                                     pose_points[target][Y])):
                            component.callback()
                if isinstance(component, TrackingBubble):
                    component.pos = (pose_points[component.target][X],
                                     pose_points[component.target][Y])

                component.render(self.frontend.window)

            self._scenes[self._active_scene].frame_callback()

            self.frontend.update()
