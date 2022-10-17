"""
`cvgui` is a library for creating body-interactive GUIs using computer
vison.

Please see the sidebar for documentation on the packages
that make up `cvgui`.

# Installation

> pip install cvgui

# About

The inspiration for this project came from work completed under
the James Madison University department of engineering Wearable
Computing Research Group to quickly prototype novel methods of user
feedback. Since then, the project has been re-written to be more useful
in any general case requiring user interfaces that can be "clicked" with
one's body.

The general goal of the library is to accept a group of points from an
abstract input that can then be interpreted as a human form and displayed
graphically. Common components are provided such as buttons and labels
to decorate the interface and make it interactive. Operability outside of
the library is provided by callback functions that can be used to trigger
any Python code the developer desires.

# Example Program

This example creates a simple activity with a skeleton and a button.
When clicked, the button moves. Example programs can be found in the
`bin/examples` directory.

```python
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
                                      pos=(1920//2, 1080//2),
                                      activation_distance=100,
                                      color=(255,0,0,255))


def callback(button: cvgui.Button):
    \"\"\"Define what the button should do when clicked\"\"\"
    button.pos = (0, 0)


# Set the button to be clicked using the user's left or right hand
button_1.targets = [cv_model.LEFT_HAND, cv_model.RIGHT_HAND]

# Link the callback function to the button
button_1.callback = lambda: callback(button_1)

# Create a skeleton to map pose points to
skeleton: cvgui.Skeleton = cvgui.skeleton(
    gui=ui, pos=(800, 600), scale=cv_model.DEFAULT_SCALE)

# Add the skeleton and button to the scene
scene_1.add_component(button_1)
scene_1.add_component(skeleton)

# Start activity
activity.run()
```
"""

from .core import *
from .inputs.computer_vision import *
from .user_interface import *
from .activity import *
