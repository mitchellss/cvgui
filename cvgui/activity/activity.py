"""
Operates on a collection of related scenes to create a specific experience.

The activity module orchestrates the interfaces of `core` packages
to run concurrently and create a coherent flow of information.
"""
from multiprocessing.sharedctypes import SynchronizedArray
from typing import List

import multiprocessing as mp
import logging
import numpy as np


from cvgui.activity.scene import Scene
from cvgui.core.displaying import UserInterface
from cvgui.core.displaying.components import Button, Skeleton
from cvgui.core.recieving import PoseGenerator

X = 0
Y = 1

class Activity:
    """A collection of scenes and the abstract logic
    for their interaction."""

    # Private variables
    _scenes: List[Scene] = []

    _active_scene: int = 0
    """The index of the scene to render."""

    pose: SynchronizedArray = mp.Array("d", 33*4)
    """The collection of points that represent a human figure."""

    def __init__(self, pose_input: PoseGenerator, frontend: UserInterface) -> None:
        """
        Args:
            pose_input (PoseGenerator): An object that can generate poses.
            frontend (UserInterface): An object that can create a user interface.
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
    
    def next_scene(self) -> None:
        """
        Sets the active scene to the next scene in the scene array. Circles
        back to the first scene if current active scene is the last in the array.
        """
        self._active_scene += 1
        if self._active_scene > len(self._scenes) - 1:
            self._active_scene = 0
    
    def previous_scene(self) -> None:
        """
        Sets the active scene to the previous scene in the scene array. Circles
        back to the last scene if current active scene is the first in the array.
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
        logger = mp.log_to_stderr()
        logger.setLevel(mp.SUBDEBUG)  # type: ignore

        proc: mp.Process = mp.Process(target=self.update_ui,
                                      args=[self.frontend, self._scenes])
        proc.start()

        try:
            self.update_pose()
        except KeyboardInterrupt:
            proc.kill()
        except Exception as excpt:
            logging.error(excpt)
            proc.kill()
            raise excpt

        proc.join()

    def update_pose(self):
        """Infinitely attempts to get pose data from the
        global pose input. Does not run well in a sub-process."""
        while True:
            pose: np.ndarray = self.pose_input.get_pose()
            pose_list: List[float] = pose.flatten().tolist()
            for index, value in enumerate(pose_list):
                self.pose[index] = value

    def update_ui(self, frontend: UserInterface, scenes: List[Scene]):
        """Infinitely attempts to render the most current
        version of the active scene of the user interface.
        Intended to run in a sub-process to update the ui
        concurrently while retrieving new data.

        Args:
            frontend (UserInterface): The user interface to update.
            scenes (List[Scene]): The scenes for the activity being rendered.
        """
        frontend.new_gui()
        skeleton_points = np.zeros((33, 4))
        while True:
            frontend.clear()

            # Make sure the skeleton is updated first if it exists.
            # That way button clicks aren't a frame late
            for component in scenes[self._active_scene].components:
                if isinstance(component, Skeleton):
                    skeleton_points = np.array(
                        self.pose.get_obj()).reshape((33, 4))
                    # Scale the skeleton points and offset them
                    skeleton_points[:, X] = skeleton_points[:, X] * \
                        component.scale + component.x_coord
                    skeleton_points[:, Y] = skeleton_points[:, Y] * \
                        component.scale + component.y_coord
                    component.skeleton_points = skeleton_points
                    break

            for component in scenes[self._active_scene].components:
                if isinstance(component, Button):
                    for target in component.targets:
                        if component.is_clicked(
                                skeleton_points[target][X], skeleton_points[target][Y],
                                component.activation_distance):
                            component.callback()

                component.render(frontend.window)

            frontend.update()
