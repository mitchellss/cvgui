import unittest
import cvgui

class TestActivity(unittest.TestCase):

    def setUp(self) -> None:
        self.activity = cvgui.Activity(pose_input=None, frontend=None)
        self.scene_1 = cvgui.Scene()
        self.scene_2 = cvgui.Scene()
    
    def tearDown(self) -> None:
        self.activity._scenes = []
        self.activity._active_scene = 0

    def test_add_scene(self):
        self.activity.add_scene(self.scene_1)
        self.activity.add_scene(self.scene_2)
        self.assertEquals(len(self.activity._scenes), 2)

    def test_next_scene(self):
        self.activity.add_scene(self.scene_1)
        self.activity.add_scene(self.scene_2)
        self.assertEquals(self.activity._active_scene, 0)
        self.activity.next_scene()
        self.assertEquals(self.activity._active_scene, 1)

    def test_next_scene_circular(self):
        """
        Test to make sure the next scene method loops back
        to the beginning of the array if it reaches the end.
        """
        self.activity.add_scene(self.scene_1)
        self.activity.add_scene(self.scene_2)
        self.assertEquals(self.activity._active_scene, 0)
        self.activity.next_scene()
        self.assertEquals(self.activity._active_scene, 1)
        self.activity.next_scene()
        self.assertEquals(self.activity._active_scene, 0)
    
    def test_previous_scene(self):
        self.activity.add_scene(self.scene_1)
        self.activity.add_scene(self.scene_2)
        self.assertEquals(self.activity._active_scene, 0)
        self.activity.next_scene()
        self.assertEquals(self.activity._active_scene, 1)
        self.activity.previous_scene()
        self.assertEquals(self.activity._active_scene, 0)

    def test_previous_scene_circular(self):
        """
        Test to make sure the previous scene method loops back
        to the end of the array if it reaches the beginnning.
        """
        self.activity.add_scene(self.scene_1)
        self.activity.add_scene(self.scene_2)
        self.assertEquals(self.activity._active_scene, 0)
        self.activity.previous_scene()
        self.assertEquals(self.activity._active_scene, 1)
    
    def test_set_scene_valid_index(self):
        self.activity.add_scene(self.scene_1)
        self.activity.add_scene(self.scene_2)
        self.assertEquals(self.activity._active_scene, 0)
        self.activity.set_scene(1)
        self.assertEquals(self.activity._active_scene, 1)

    def test_set_scene_invalid_index(self):
        """
        Make sure the active scene does not change if an invalid
        index is passed to set_scene method.
        """
        self.activity.add_scene(self.scene_1)
        self.activity.add_scene(self.scene_2)
        self.assertEquals(self.activity._active_scene, 0)
        index_too_big = 5
        self.assertFalse(self.activity.set_scene(index_too_big))
        self.assertEquals(self.activity._active_scene, 0)
