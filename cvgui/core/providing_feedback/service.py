"""
Core classes that define the requirements
to be considered a feedback device.
"""

from typing_extensions import Protocol

class FeedbackDevice(Protocol):
    """Interface describing a device that provides feedback."""

    def provide_feedback(self) -> None:
        """Provides feedback to the user in an abstract way."""