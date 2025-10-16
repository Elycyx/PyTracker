# PyTracker

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pytracker.svg)](https://pypi.org/project/pytracker/)

A comprehensive Python wrapper for OpenVR tracking systems. PyTracker provides easy-to-use Python functions for any SteamVR tracked system, including HMDs, controllers, trackers, and tracking references.

## Features

- **Easy Device Management**: Simple API for discovering and managing VR devices
- **Real-time Tracking**: High-frequency pose tracking with configurable sampling rates
- **Multiple Data Formats**: Support for Euler angles, quaternions, and transformation matrices
- **3D Visualization**: Built-in real-time 3D visualization tools
- **Device Configuration**: JSON-based device configuration for consistent device naming
- **Comprehensive Examples**: Ready-to-use example scripts for common use cases

## Installation

### Prerequisites

- Python 3.7 or higher
- SteamVR installed and running
- OpenVR-compatible VR hardware

### Install from Source

```bash
# Clone the repository
git clone https://github.com/Elycyx/PyTracker.git
cd PyTracker

# Install in development mode
pip install -e .
```

## Quick Start

### Basic Usage

```python
import pytracker

# Initialize the tracker
tracker = pytracker.Tracker()

# Print discovered devices
tracker.print_discovered_objects()

# Get pose data from a controller
pose = tracker.devices["controller_1"].get_pose_euler()
print(f"Position: {pose[:3]}, Orientation: {pose[3:]}")

# Sample data at 250 Hz for 5 seconds
data = tracker.devices["controller_1"].sample(1250, 250)
```

### Configuration

Create a `config.json` file to assign custom names to your devices:

```json
{
    "devices": [
        {
            "name": "hmd",
            "type": "HMD",
            "serial": "XXX-XXXXXXXX"
        },
        {
            "name": "tracking_reference_1",
            "type": "Tracking Reference",
            "serial": "LHB-XXXXXXXX"
        },
        {
            "name": "controller_1",
            "type": "Controller",
            "serial": "XXX-XXXXXXXX"
        },
        {
            "name": "tracker_1",
            "type": "Tracker",
            "serial": "LHR-XXXXXXXX"
        }
    ]
}
```

Then initialize with configuration:

```python
tracker = pytracker.Tracker("config.json")
```

## Examples

### Real-time Controller Tracking

```python
import pytracker
import time

tracker = pytracker.Tracker()
tracker.print_discovered_objects()

while True:
    pose = tracker.devices["controller_1"].get_pose_euler()
    if pose:
        print(f"Position: {pose[:3]}, Orientation: {pose[3:]}")
    time.sleep(0.01)  # 100 Hz
```

### Data Collection and Plotting

```python
import pytracker
import matplotlib.pyplot as plt

tracker = pytracker.Tracker()

# Collect 1000 samples at 250 Hz
data = tracker.devices["controller_1"].sample(1000, 250)

# Plot X coordinate over time
plt.plot(data.time, data.x)
plt.title('Controller X Coordinate')
plt.xlabel('Time (seconds)')
plt.ylabel('X Coordinate (meters)')
plt.show()
```

### 3D Visualization

```python
# Run the built-in 3D visualizer
python -m pytracker.examples.visualizer tracker_1 60 1000
```

## Command Line Tools

PyTracker includes several command-line tools:

```bash
# Test controller tracking
python -m pytracker.examples.test_controller [sample_rate]

# Test tracker tracking  
python -m pytracker.examples.test_tracker [sample_rate]

# 3D visualization
python -m pytracker.examples.visualizer [device_name] [update_rate] [trail_length]

# Simple plotting example
python -m pytracker.examples.simple_plot
```

## API Reference

### Tracker Class

The main `Tracker` class provides access to all tracked devices:

```python
tracker = pytracker.Tracker(configfile_path=None)
```

**Methods:**
- `print_discovered_objects()`: Print information about all discovered devices
- `poll_vr_events()`: Poll for VR events (device connections/disconnections)
- `get_pose()`: Get pose data for all devices
- `get_device_by_serial(serial)`: Get device by serial number
- `get_devices_by_type(device_type)`: Get all devices of a specific type
- `is_device_connected(device_name)`: Check if a device is connected

### TrackedDevice Class

Individual devices are represented by `TrackedDevice` objects:

```python
device = tracker.devices["controller_1"]
```

**Methods:**
- `get_pose_euler()`: Get pose as [x, y, z, yaw, pitch, roll]
- `get_pose_quaternion()`: Get pose as [x, y, z, r_w, r_x, r_y, r_z]
- `get_pose_matrix()`: Get pose as 3x4 transformation matrix
- `get_velocity()`: Get linear velocity [vx, vy, vz]
- `get_angular_velocity()`: Get angular velocity [wx, wy, wz]
- `sample(num_samples, sample_rate)`: Collect pose data samples
- `get_controller_inputs()`: Get controller input state (controllers only)
- `trigger_haptic_pulse()`: Trigger haptic feedback (controllers only)

### PoseSampleBuffer Class

The `PoseSampleBuffer` class stores collected pose data:

```python
data = device.sample(1000, 250)
print(data.x)      # X coordinates
print(data.y)      # Y coordinates  
print(data.z)      # Z coordinates
print(data.yaw)    # Yaw angles
print(data.pitch)  # Pitch angles
print(data.roll)   # Roll angles
print(data.time)   # Timestamps
```

## Device Types

PyTracker supports the following device types:

- **HMD**: Head-mounted displays
- **Controller**: VR controllers
- **Tracker**: Generic tracking devices
- **Tracking Reference**: Base stations/lighthouses

## Configuration

### Device Configuration

Create a JSON configuration file to assign custom names to devices:

```json
{
    "devices": [
        {
            "name": "my_controller",
            "type": "Controller", 
            "serial": "LHR-XXXXXXXX"
        }
    ]
}
```

### SteamVR Settings

For optimal performance, you may need to configure SteamVR settings. See `example_default.vrsettings` for reference.

## Troubleshooting

### Common Issues

1. **"No devices found"**: Ensure SteamVR is running and devices are connected
2. **"Device not found"**: Check device serial numbers in configuration
3. **Low tracking quality**: Ensure good lighting and base station positioning
4. **Import errors**: Make sure all dependencies are installed

### Getting Device Serial Numbers

To find device serial numbers for configuration:

```python
tracker = pytracker.Tracker()
for device_name, device in tracker.devices.items():
    print(f"{device_name}: {device.get_serial()}")
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on the excellent [pyopenvr library](https://github.com/cmbruns/pyopenvr) by [cmbruns](https://github.com/cmbruns) and [triad_openvr](https://github.com/TriadSemi/triad_openvr.git).
- Built for the OpenVR community
- Inspired by the need for easy-to-use VR tracking in Python

