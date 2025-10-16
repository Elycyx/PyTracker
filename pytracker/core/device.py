"""
Tracked device classes for OpenVR devices
"""

import time
import openvr
from functools import lru_cache
from .utils import get_pose, convert_to_euler, convert_to_quaternion


class TrackedDevice:
    """
    Base class for all tracked OpenVR devices (HMD, Controller, Tracker).
    """
    
    def __init__(self, vr_obj, index, device_class):
        """
        Initialize a tracked device.
        
        Args:
            vr_obj: OpenVR system object
            index (int): Device index
            device_class (str): Type of device
        """
        self.device_class = device_class
        self.index = index
        self.vr = vr_obj

    @lru_cache(maxsize=None)
    def get_serial(self):
        """Get the device serial number."""
        return self.vr.getStringTrackedDeviceProperty(self.index, openvr.Prop_SerialNumber_String)

    def get_model(self):
        """Get the device model number."""
        return self.vr.getStringTrackedDeviceProperty(self.index, openvr.Prop_ModelNumber_String)

    def get_battery_percent(self):
        """Get the device battery percentage."""
        return self.vr.getFloatTrackedDeviceProperty(self.index, openvr.Prop_DeviceBatteryPercentage_Float)

    def is_charging(self):
        """Check if the device is currently charging."""
        return self.vr.getBoolTrackedDeviceProperty(self.index, openvr.Prop_DeviceIsCharging_Bool)

    def sample(self, num_samples, sample_rate):
        """
        Sample device pose data at specified rate.
        
        Args:
            num_samples (int): Number of samples to collect
            sample_rate (float): Sampling rate in Hz
            
        Returns:
            PoseSampleBuffer: Buffer containing sampled data
        """
        from .pose_buffer import PoseSampleBuffer
        
        interval = 1 / sample_rate
        rtn = PoseSampleBuffer()
        sample_start = time.time()
        
        for i in range(num_samples):
            start = time.time()
            pose = get_pose(self.vr)
            rtn.append(pose[self.index].mDeviceToAbsoluteTracking, 
                      time.time() - sample_start)
            sleep_time = interval - (time.time() - start)
            if sleep_time > 0:
                time.sleep(sleep_time)
        return rtn

    def get_pose_euler(self, pose=None):
        """
        Get device pose as Euler angles.
        
        Args:
            pose: Optional pose data (if None, will fetch current pose)
            
        Returns:
            list or None: [x, y, z, yaw, pitch, roll] or None if invalid
        """
        if pose is None:
            pose = get_pose(self.vr)
        if pose[self.index].bPoseIsValid:
            return convert_to_euler(pose[self.index].mDeviceToAbsoluteTracking)
        else:
            return None

    def get_pose_matrix(self, pose=None):
        """
        Get device pose as transformation matrix.
        
        Args:
            pose: Optional pose data (if None, will fetch current pose)
            
        Returns:
            list or None: 3x4 transformation matrix or None if invalid
        """
        if pose is None:
            pose = get_pose(self.vr)
        if pose[self.index].bPoseIsValid:
            return pose[self.index].mDeviceToAbsoluteTracking
        else:
            return None

    def get_velocity(self, pose=None):
        """
        Get device linear velocity.
        
        Args:
            pose: Optional pose data (if None, will fetch current pose)
            
        Returns:
            list or None: [vx, vy, vz] or None if invalid
        """
        if pose is None:
            pose = get_pose(self.vr)
        if pose[self.index].bPoseIsValid:
            return pose[self.index].vVelocity
        else:
            return None

    def get_angular_velocity(self, pose=None):
        """
        Get device angular velocity.
        
        Args:
            pose: Optional pose data (if None, will fetch current pose)
            
        Returns:
            list or None: [wx, wy, wz] or None if invalid
        """
        if pose is None:
            pose = get_pose(self.vr)
        if pose[self.index].bPoseIsValid:
            return pose[self.index].vAngularVelocity
        else:
            return None

    def get_pose_quaternion(self, pose=None):
        """
        Get device pose as quaternion.
        
        Args:
            pose: Optional pose data (if None, will fetch current pose)
            
        Returns:
            list or None: [x, y, z, r_w, r_x, r_y, r_z] or None if invalid
        """
        if pose is None:
            pose = get_pose(self.vr)
        if pose[self.index].bPoseIsValid:
            return convert_to_quaternion(pose[self.index].mDeviceToAbsoluteTracking)
        else:
            return None

    def controller_state_to_dict(self, pControllerState):
        """
        Convert controller state to dictionary.
        This function is graciously borrowed from:
        https://gist.github.com/awesomebytes/75daab3adb62b331f21ecf3a03b3ab46
        
        Args:
            pControllerState: OpenVR controller state object
            
        Returns:
            dict: Dictionary containing controller state information
        """
        d = {}
        d['unPacketNum'] = pControllerState.unPacketNum
        # on trigger .y is always 0.0 says the docs
        d['trigger'] = pControllerState.rAxis[1].x
        # 0.0 on trigger is fully released
        # -1.0 to 1.0 on joystick and trackpads
        d['trackpad_x'] = pControllerState.rAxis[0].x
        d['trackpad_y'] = pControllerState.rAxis[0].y
        # These are published and always 0.0
        # for i in range(2, 5):
        #     d['unknowns_' + str(i) + '_x'] = pControllerState.rAxis[i].x
        #     d['unknowns_' + str(i) + '_y'] = pControllerState.rAxis[i].y
        d['ulButtonPressed'] = pControllerState.ulButtonPressed
        d['ulButtonTouched'] = pControllerState.ulButtonTouched
        # To make easier to understand what is going on
        # Second bit marks menu button
        d['menu_button'] = bool(pControllerState.ulButtonPressed >> 1 & 1)
        # 32 bit marks trackpad
        d['trackpad_pressed'] = bool(pControllerState.ulButtonPressed >> 32 & 1)
        d['trackpad_touched'] = bool(pControllerState.ulButtonTouched >> 32 & 1)
        # third bit marks grip button
        d['grip_button'] = bool(pControllerState.ulButtonPressed >> 2 & 1)
        # System button can't be read, if you press it
        # the controllers stop reporting
        return d

    def get_controller_inputs(self):
        """
        Get controller input state.
        
        Returns:
            dict: Controller input state dictionary
        """
        result, state = self.vr.getControllerState(self.index)
        return self.controller_state_to_dict(state)

    def trigger_haptic_pulse(self, duration_micros=1000, axis_id=0):
        """
        Causes devices with haptic feedback to vibrate for a short time.
        
        Args:
            duration_micros (int): Duration of haptic pulse in microseconds
            axis_id (int): Axis ID for haptic feedback
        """
        self.vr.triggerHapticPulse(self.index, axis_id, duration_micros)


class TrackingReference(TrackedDevice):
    """
    Specialized class for tracking reference devices (base stations).
    """
    
    def get_mode(self):
        """Get the tracking reference mode."""
        return self.vr.getStringTrackedDeviceProperty(
            self.index, openvr.Prop_ModeLabel_String
        ).decode('utf-8').upper()
    
    def sample(self, num_samples, sample_rate):
        """
        Override sample method for tracking references.
        Tracking references don't move, so sampling isn't much use.
        """
        print("Warning: Tracking References do not move, sample isn't much use...")
        return super().sample(num_samples, sample_rate)
