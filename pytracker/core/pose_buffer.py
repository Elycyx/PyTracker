"""
Pose sample buffer for collecting and storing tracking data
"""

import math
import time


class PoseSampleBuffer:
    """
    A class to make it easy to append pose matrices and convert to both 
    Euler and Quaternion for plotting and analysis.
    """
    
    def __init__(self):
        """Initialize an empty pose sample buffer."""
        self.i = 0
        self.index = []
        self.time = []
        self.x = []
        self.y = []
        self.z = []
        self.yaw = []
        self.pitch = []
        self.roll = []
        self.r_w = []
        self.r_x = []
        self.r_y = []
        self.r_z = []

    def append(self, pose_mat, t):
        """
        Append a pose matrix and timestamp to the buffer.
        
        Args:
            pose_mat: 3x4 transformation matrix
            t (float): Timestamp in seconds
        """
        self.time.append(t)
        self.x.append(pose_mat[0][3])
        self.y.append(pose_mat[1][3])
        self.z.append(pose_mat[2][3])
        
        # Calculate Euler angles
        self.yaw.append(180 / math.pi * math.atan(pose_mat[1][0] / pose_mat[0][0]))
        self.pitch.append(180 / math.pi * math.atan(-1 * pose_mat[2][0] / 
                          math.sqrt(pow(pose_mat[2][1], 2) + math.pow(pose_mat[2][2], 2))))
        self.roll.append(180 / math.pi * math.atan(pose_mat[2][1] / pose_mat[2][2]))
        
        # Calculate quaternion components
        r_w = math.sqrt(abs(1 + pose_mat[0][0] + pose_mat[1][1] + pose_mat[2][2])) / 2
        self.r_w.append(r_w)
        self.r_x.append((pose_mat[2][1] - pose_mat[1][2]) / (4 * r_w))
        self.r_y.append((pose_mat[0][2] - pose_mat[2][0]) / (4 * r_w))
        self.r_z.append((pose_mat[1][0] - pose_mat[0][1]) / (4 * r_w))

    def get_data_dict(self):
        """
        Get all data as a dictionary for easy access.
        
        Returns:
            dict: Dictionary containing all pose data
        """
        return {
            'time': self.time,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'yaw': self.yaw,
            'pitch': self.pitch,
            'roll': self.roll,
            'r_w': self.r_w,
            'r_x': self.r_x,
            'r_y': self.r_y,
            'r_z': self.r_z
        }

    def clear(self):
        """Clear all data from the buffer."""
        self.i = 0
        self.index.clear()
        self.time.clear()
        self.x.clear()
        self.y.clear()
        self.z.clear()
        self.yaw.clear()
        self.pitch.clear()
        self.roll.clear()
        self.r_w.clear()
        self.r_x.clear()
        self.r_y.clear()
        self.r_z.clear()

    def __len__(self):
        """Return the number of samples in the buffer."""
        return len(self.time)
