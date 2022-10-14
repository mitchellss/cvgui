"""
Example program that shows a basic usage of the library.
A button and skeleton component are added to a scene that
takes input from a webcam and gets pose data from Google's
Blazepose
"""
import cvgui

# Specify input as a webcam and computer vision model as blazepose
frame_input: cvgui.FrameInput = cvgui.Webcam(device_num=0, fps=30)
cv_model: cvgui.CVModel = cvgui.BlazePose()

# Create a pose generator based on a webcam + blazepose
pose_input: cvgui.PoseGenerator = cvgui.ComputerVisionPose(
    frame_input=frame_input, model=cv_model)

# Specify GUI to be pygame
ui: cvgui.UserInterface = cvgui.PyGameUI(width=1920//2, height=1080//2, fps=60)

# Create activity
activity = cvgui.Activity(pose_input=pose_input, frontend=ui)

# Create a new scene
scene_1 = cvgui.Scene()
activity.add_scene(scene_1)


def callback(button: cvgui.Button):
    button.x_coord = 0
    button.y_coord = 0


# Create a button that prints "Hello world!" when clicked
button_1: cvgui.Button = cvgui.button(gui=ui,
                                      x_coord=1920//2, y_coord=1080//2,
                                      activation_distance=100)
button_1.set_targets([cv_model.LEFT_HAND, cv_model.RIGHT_HAND])
button_1.set_callback(callback=lambda: callback(button_1))


# Create a skeleton to map pose points to
skeleton: cvgui.Skeleton = cvgui.skeleton(gui=ui, x_coord=200, y_coord=200)

# Add the skeleton and button to the scene
scene_1.add_component(button_1)
scene_1.add_component(skeleton)

# Start activity
activity.run()
