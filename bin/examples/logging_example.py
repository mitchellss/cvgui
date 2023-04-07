"""
Example program that shows how to create an activity
with multiple scenes.
"""
from pathlib import Path
from random import randrange
import cvgui

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_FPS = 60


def main():
    # Specify input as a webcam and computer vision model as blazepose
    frame_input = cvgui.Webcam(device_num=0, fps=30)
    cv_model = cvgui.BlazePose()

    # Create a pose generator based on a webcam + blazepose
    pose_input = cvgui.ComputerVisionPose(
        frame_input=frame_input, model=cv_model)

    # Specify GUI to be pygame
    ui = cvgui.PyGameUI(width=WINDOW_WIDTH,
                        height=WINDOW_HEIGHT, fps=WINDOW_FPS)

    # Create activity
    activity = cvgui.Activity(pose_input=pose_input, frontend=ui)

    csv_logger = cvgui.CSVPoseLogger(Path("test.csv"))
    activity.add_logger(csv_logger)

    # Create two scenes
    scene_1 = cvgui.Scene()
    scene_2 = cvgui.Scene()
    activity.add_scene(scene_1)
    activity.add_scene(scene_2)

    # Create a new button
    button_1 = cvgui.button(
        gui=ui,
        pos=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2),
        activation_distance=50,
        color=(255, 0, 0, 255),
        radius=50
    )

    hand_bubble_1 = cvgui.tracking_bubble(
        gui=ui,
        color=(255, 0, 0, 255),
        target=cv_model.LEFT_HAND,
        radius=40,
    )

    button_2 = cvgui.button(
        gui=ui,
        pos=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2),
        activation_distance=50,
        color=(0, 0, 255, 255),
        radius=50
    )

    hand_bubble_2 = cvgui.tracking_bubble(
        gui=ui,
        radius=40,
        target=cv_model.RIGHT_HAND,
        color=(0, 0, 255, 255),
    )

    def callback(button) -> None:
        """Move the button to a random spot and
        switch to the next scene

        Args:
            button (cvgui.Button): The button to move
        """
        button.pos = (randrange(600, 1000, 20), randrange(200, 600, 20))
        activity.next_scene()

    # Set the button to be clicked using the user's left or right hand
    button_1.targets = [cv_model.LEFT_HAND]
    button_2.targets = [cv_model.RIGHT_HAND]

    # Link the callback function to the button.
    # You only need the lambda part if the callback
    # functions take an argument.
    button_1.callback = lambda: callback(button_2)
    button_2.callback = lambda: callback(button_1)

    # Create a skeleton to map pose points to
    skeleton = cvgui.skeleton(gui=ui, pos=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2),
                              scale=cv_model.DEFAULT_SCALE)

    # Add the skeleton and button to the scene
    scene_1.add_component(button_1)
    scene_1.add_component(hand_bubble_1)
    scene_1.add_component(skeleton)
    scene_2.add_component(button_2)
    scene_2.add_component(hand_bubble_2)
    scene_2.add_component(skeleton)

    # Start activity
    activity.run()


if __name__ == "__main__":
    main()
