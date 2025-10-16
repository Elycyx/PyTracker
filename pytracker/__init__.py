"""
PyTracker - A comprehensive Python wrapper for OpenVR tracking systems

This package provides easy-to-use Python functions for any SteamVR tracked system,
including HMDs, controllers, trackers, and tracking references.

Example:
    >>> import pytracker
    >>> tracker = pytracker.Tracker()
    >>> pose = tracker.devices["controller_1"].get_pose_euler()
    >>> print(f"Position: {pose[:3]}, Orientation: {pose[3:]}")
"""

__version__ = "1.0.0"
__author__ = "PyTracker Development Team"
__email__ = "pytracker@example.com"

# Import main classes for easy access
from .core.tracker import Tracker
from .core.device import TrackedDevice, TrackingReference
from .core.pose_buffer import PoseSampleBuffer

# Import utility functions
from .core.utils import convert_to_euler, convert_to_quaternion

# Make main classes available at package level
__all__ = [
    "Tracker",
    "TrackedDevice", 
    "TrackingReference",
    "PoseSampleBuffer",
    "convert_to_euler",
    "convert_to_quaternion",
]
