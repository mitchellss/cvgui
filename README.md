# cvgui

`cvgui` is a library for creating body-interactive GUIs using computer
vison.

**cvgui is a prototype. No guarantees can
be made about the stability of the API or the library itself.**


## Installation

```shell
pip install cvgui
```

Requires Python 3.10

## Usage

```shell
python ./my_activity.py
```
See the documentation [here](https://mitchellss.github.io/cvgui) for more information
on how to create your own activities.

## Contributing

Pull requests are welcome. Please see the [contributing guide](CONTRIBUTING.md) for more information.


## Example Program

This example creates a simple activity with a skeleton and a button.
When clicked, the button moves and changes color. Other example programs 
can be found in the `bin/examples` directory.

```python
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

    # Create a new scene
    scene_1 = cvgui.Scene()
    activity.add_scene(scene_1)

    # Create a new button
    button_1 = cvgui.button(
        gui=ui,
        pos=(WINDOW_WIDTH//2,
             WINDOW_HEIGHT//2),
        activation_distance=50,
        color=(255, 0, 0, 255),
        radius=50
    )

    def callback() -> None:
        '''
        Define what the button should do when clicked.
        In this case, randomly set a new button position
        and randomly select a new color.
        '''
        button_1.pos = (randrange(600, 1000, 20), randrange(200, 600, 20))
        button_1.color = (randrange(0, 255, 1), randrange(0, 255, 1),
                          randrange(0, 255, 1), 255)

    # Set the button to be clicked using the user's left or right hand
    button_1.targets = [cv_model.LEFT_HAND, cv_model.RIGHT_HAND]

    # Link the callback function to the button
    button_1.callback = callback

    # Create a skeleton to map pose points to
    skeleton = cvgui.skeleton(gui=ui, pos=(
        800, 600), scale=cv_model.DEFAULT_SCALE)

    # Add the skeleton and button to the scene
    scene_1.add_component(button_1)
    scene_1.add_component(skeleton)

    # Start activity
    activity.run()


# Everything must be run under "__name__ == __main__"
# for windows multiprocessing
if __name__ == "__main__":
    main()
```
