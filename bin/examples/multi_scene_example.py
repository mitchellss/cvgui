"""
Example program that shows a basic usage of the library.
A button and skeleton component are added to a scene that
takes input from a webcam and gets pose data from Google's
Blazepose.
"""
from random import randrange
import cvgui

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_FPS = 60

# This name == main line is required for windows multiprocessing
if __name__ == "__main__":

    # Specify input as a webcam and computer vision model as blazepose
    frame_input: cvgui.FrameInput = cvgui.Webcam(device_num=0, fps=30)
    cv_model: cvgui.CVModel = cvgui.BlazePose()

    # Create a pose generator based on a webcam + blazepose
    pose_input: cvgui.PoseGenerator = cvgui.ComputerVisionPose(
        frame_input=frame_input, model=cv_model)

    # Specify GUI to be pygame
    ui: cvgui.UserInterface = cvgui.PyGameUI(
        width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=WINDOW_FPS)

    # Create activity
    activity = cvgui.Activity(pose_input=pose_input, frontend=ui)

    # Create two scenes
    scene_1 = cvgui.Scene()
    scene_2 = cvgui.Scene()
    activity.add_scene(scene_1)
    activity.add_scene(scene_2)

    # Create a new button
    button_1: cvgui.Button = cvgui.button(gui=ui,
                                          pos=(WINDOW_WIDTH//2,
                                               WINDOW_HEIGHT//2),
                                          activation_distance=50,
                                          color=(255, 0, 0, 255),
                                          radius=50)

    button_2: cvgui.Button = cvgui.button(gui=ui,
                                          pos=(WINDOW_WIDTH//2,
                                               WINDOW_HEIGHT//2),
                                          activation_distance=50,
                                          color=(0, 0, 255, 255),
                                          radius=50)

    def callback(button: cvgui.Button) -> None:
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

    # Link the callback function to the button
    button_1.callback = lambda: callback(button_2)
    button_2.callback = lambda: callback(button_1)

    # Create a skeleton to map pose points to
    skeleton: cvgui.Skeleton = cvgui.skeleton(
        gui=ui, pos=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2),
        scale=cv_model.DEFAULT_SCALE)

    # Add the skeleton and button to the scene
    scene_1.add_component(button_1)
    scene_1.add_component(skeleton)
    scene_2.add_component(button_2)
    scene_2.add_component(skeleton)

    # Start activity
    activity.run()
