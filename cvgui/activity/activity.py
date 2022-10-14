"""Orchestrates core packages to run concurrently"""
from typing import List

import multiprocessing as mp
import logging
import numpy as np


from cvgui.activity.scene import Scene
from cvgui.core.displaying import UserInterface
from cvgui.core.displaying.components import Button, Skeleton
from cvgui.core.recieving import PoseGenerator


class Activity:
    """A collection of scenes and the abstract logic
    for their interaction."""

    _scenes: List[Scene] = []
    active_scene: int = 0
    pose = mp.Array("d", 33*4)

    def __init__(self, pose_input: PoseGenerator, frontend: UserInterface) -> None:
        """Creates a new activity.

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

    def run(self) -> None:
        """
        Infinitely retrieves pose data and
        renders the components of added scenes.
        """
        logger = mp.log_to_stderr()
        logger.setLevel(mp.SUBDEBUG)  # type: ignore

        p: mp.Process = mp.Process(target=self.update_ui,
                                   args=[self.frontend, self._scenes])
        p.start()

        try:
            self.update_pose()
        except KeyboardInterrupt:
            p.kill()
        except Exception as excpt:
            logging.error(excpt)
            p.kill()
            raise excpt

        p.join()

    def update_pose(self):
        """Infinitely attempts to get pose data from the
        global pose input. Does not run well in a sub-process."""
        while True:
            pose: np.ndarray = self.pose_input.get_pose()
            pose_list: List[float] = pose.flatten().tolist()
            for index, _ in enumerate(pose_list):
                self.pose[index] = pose_list[index] * 450 + 600

    def update_ui(self, frontend: UserInterface, scenes: List[Scene]):
        """Infinitely attempts to render the most current
        version of the active scene of the user interface.
        Intended to run in a sub-process to update the ui
        concurrently with retrieving new data.

        Args:
            frontend (UserInterface): The user interface to update.
            scenes (List[Scene]): The scenes for the activity being rendered.
        """
        frontend.new_gui()
        while True:
            frontend.clear()
            skeleton_points = np.array(self.pose.get_obj()).reshape((33, 4))

            for component in scenes[0].components:
                if isinstance(component, Skeleton):
                    component.skeleton_points = skeleton_points
                elif isinstance(component, Button):
                    for target in component.targets:
                        if component.is_clicked(
                                skeleton_points[target][0], skeleton_points[target][1],
                                component.activation_distance):
                            component.callback()

                component.render(frontend.window)

            frontend.update()
