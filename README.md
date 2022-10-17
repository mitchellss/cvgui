# cvgui

`cvgui` is a library for creating body-interactive GUIs using computer
vison.

Documentation can be [found here](https://mitchellss.github.io/cvgui).


**cvgui is a prototype. No guarantees can
be made about the stability of the API or the library itself.**


## Installation

> pip install cvgui

Requires Python 3.9 or later

## Contributing

Pull requests are welcome. Please see the [contributing guide](CONTRIBUTING.md) for more information.

## Example Program

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
ui: cvgui.UserInterface = cvgui.PyGameUI(width=1920//2, height=1080//2, fps=60)

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
```
