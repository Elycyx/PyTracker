"""
Utility functions for pose conversion and OpenVR operations
"""

import math
import sys
import openvr
from functools import lru_cache


def update_text(txt):
    """
    Print text but overwrite the existing line instead of starting a new line.
    
    Args:
        txt (str): Text to display
    """
    sys.stdout.write('\r' + txt)
    sys.stdout.flush()


def convert_to_euler(pose_mat):
    """
    Convert the standard 3x4 position/rotation matrix to x,y,z location 
    and the appropriate Euler angles (in degrees).
    
    Args:
        pose_mat: 3x4 transformation matrix
        
    Returns:
        list: [x, y, z, yaw, pitch, roll] in meters and degrees
    """
    yaw = 180 / math.pi * math.atan2(pose_mat[1][0], pose_mat[0][0])
    pitch = 180 / math.pi * math.atan2(-pose_mat[2][0], math.sqrt(pose_mat[2][1]**2 + pose_mat[2][2]**2))
    roll = 180 / math.pi * math.atan2(pose_mat[2][1], pose_mat[2][2])
    x = pose_mat[0][3]
    y = pose_mat[1][3]
    z = pose_mat[2][3]
    return [x, y, z, yaw, pitch, roll]


def convert_to_quaternion(pose_mat):
    """
    Convert the standard 3x4 position/rotation matrix to x,y,z location 
    and the appropriate quaternion.
    
    Args:
        pose_mat: 3x4 transformation matrix
        
    Returns:
        list: [x, y, z, r_w, r_x, r_y, r_z] in meters and quaternion components
    """
    # Per issue #2, adding abs() so that sqrt only results in real numbers
    r_w = math.sqrt(abs(1 + pose_mat[0][0] + pose_mat[1][1] + pose_mat[2][2])) / 2
    r_x = (pose_mat[2][1] - pose_mat[1][2]) / (4 * r_w)
    r_y = (pose_mat[0][2] - pose_mat[2][0]) / (4 * r_w)
    r_z = (pose_mat[1][0] - pose_mat[0][1]) / (4 * r_w)

    x = pose_mat[0][3]
    y = pose_mat[1][3]
    z = pose_mat[2][3]
    return [x, y, z, r_w, r_x, r_y, r_z]


def get_pose(vr_obj):
    """
    Get pose data for all tracked devices.
    
    Args:
        vr_obj: OpenVR system object
        
    Returns:
        Pose data for all devices
    """
    return vr_obj.getDeviceToAbsoluteTrackingPose(
        openvr.TrackingUniverseStanding, 0, openvr.k_unMaxTrackedDeviceCount
    )
