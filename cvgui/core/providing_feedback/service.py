"""Interfaces describing methods of providing feedback."""

from typing_extensions import Protocol

class FeedbackDevice(Protocol):
    """An abstract device that provides feedback."""

    def provide_feedback(self) -> None:
        """Activates the feedback mechanism on the device."""