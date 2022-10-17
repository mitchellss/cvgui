"""
Example program that shows a basic usage of the library.
A button and skeleton component are added to a scene that
takes input from a webcam and gets pose data from Google's
Blazepose.
"""
import cvgui

# Specify input as a webcam and computer vision model as blazepose
frame_input: cvgui.FrameInput = cvgui.Webcam(device_num=0, fps=30)
cv_model: cvgui.CVModel = cvgui.BlazePose()

# Create a pose generator based on a webcam + blazepose
pose_input: cvgui.PoseGenerator = cvgui.ComputerVisionPose(
    frame_input=frame_input, model=cv_model)

# Specify GUI to be pygame
ui: cvgui.UserInterface = cvgui.PyGameUI(width=1920, height=1080, fps=60)

# Create activity
activity = cvgui.Activity(pose_input=pose_input, frontend=ui)

# Create a new scene
scene_1 = cvgui.Scene()
activity.add_scene(scene_1)

# Create a new button
button_1: cvgui.Button = cvgui.button(gui=ui,
                                      x_coord=1920//2, y_coord=1080//2,
                                      activation_distance=100)


def callback(button: cvgui.Button):
    """Define what the button should do when clicked"""
    button.x_coord = 0
    button.y_coord = 0


# Set the button to be clicked using the user's left or right hand
button_1.targets = [cv_model.LEFT_HAND, cv_model.RIGHT_HAND]

# Link the callback function to the button
button_1.callback = lambda: callback(button_1)

# Create a skeleton to map pose points to
skeleton: cvgui.Skeleton = cvgui.skeleton(
    gui=ui, x_coord=800, y_coord=600, scale=cv_model.DEFAULT_SCALE)

# Add the skeleton and button to the scene
scene_1.add_component(button_1)
scene_1.add_component(skeleton)

# Start activity
activity.run()
