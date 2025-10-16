"""
Core PyTracker modules

This package contains the core functionality for OpenVR device tracking.
"""

from .tracker import Tracker
from .device import TrackedDevice, TrackingReference
from .pose_buffer import PoseSampleBuffer
from .utils import convert_to_euler, convert_to_quaternion

__all__ = [
    "Tracker",
    "TrackedDevice",
    "TrackingReference", 
    "PoseSampleBuffer",
    "convert_to_euler",
    "convert_to_quaternion",
]
