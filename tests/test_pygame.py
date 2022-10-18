import unittest

from cvgui.user_interface.pygame_ui.pygame import PyGameButton


class TestPygameButton(unittest.TestCase):

    def setUp(self) -> None:
        self.button = PyGameButton(pos=(0, 0), activation_distance=50,
                                   color=(0, 0, 0, 0), radius=50)

    def test_is_clicked_valid(self):
        self.assertTrue(self.button.is_clicked((50, 0)))

    def test_is_clicked_too_far(self):
        self.assertFalse(self.button.is_clicked((100, 0)))
