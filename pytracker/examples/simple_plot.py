#!/usr/bin/env python3
"""
Simple Plot Example

This example demonstrates how to use PyTracker to collect pose data
and create simple plots using matplotlib.

Usage:
    python -m pytracker.examples.simple_plot
"""

import matplotlib.pyplot as plt
import pytracker


def main():
    """Main function for simple plotting example."""
    print("PyTracker Simple Plot Example")
    print("=" * 40)
    
    # Initialize tracker
    try:
        tracker = pytracker.Tracker()
        tracker.print_discovered_objects()
    except Exception as e:
        print(f"Error initializing tracker: {e}")
        return 1

    # Check if controller is available
    if "controller_1" not in tracker.devices:
        print("Error: No controller found. Make sure your VR system is running.")
        return 1

    print("Collecting 1000 samples at 250 Hz...")
    
    # Sample data from controller
    data = tracker.devices["controller_1"].sample(1000, 250)
    
    # Create plot
    plt.figure(figsize=(12, 8))
    
    # Plot X coordinate over time
    plt.subplot(2, 2, 1)
    plt.plot(data.time, data.x)
    plt.title('Controller X Coordinate')
    plt.xlabel('Time (seconds)')
    plt.ylabel('X Coordinate (meters)')
    plt.grid(True)
    
    # Plot Y coordinate over time
    plt.subplot(2, 2, 2)
    plt.plot(data.time, data.y)
    plt.title('Controller Y Coordinate')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Y Coordinate (meters)')
    plt.grid(True)
    
    # Plot Z coordinate over time
    plt.subplot(2, 2, 3)
    plt.plot(data.time, data.z)
    plt.title('Controller Z Coordinate')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Z Coordinate (meters)')
    plt.grid(True)
    
    # Plot 3D trajectory
    ax = plt.subplot(2, 2, 4, projection='3d')
    ax.plot(data.x, data.y, data.z)
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (meters)')
    ax.set_title('3D Trajectory')
    
    plt.tight_layout()
    plt.show()
    
    print("Plot completed!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
