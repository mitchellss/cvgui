import unittest

from cvgui.user_interface.pygame_ui.pygame import PyGameButton


class TestUserInterface(unittest.TestCase):

    def setUp(self) -> None:
        self.button = PyGameButton(0, 0, 50)

    def test_is_clicked_valid(self):
        self.assertTrue(self.button.is_clicked(50, 0, 50))

    def test_is_clicked_too_far(self):
        self.assertFalse(self.button.is_clicked(100, 0, 50))
