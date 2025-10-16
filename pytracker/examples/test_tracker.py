#!/usr/bin/env python3
"""
Tracker Test Example

This example demonstrates how to use PyTracker to track tracker pose data
in real-time. It shows the tracker's position and orientation as Euler angles.

Usage:
    python -m pytracker.examples.test_tracker [sample_rate]
    
    sample_rate: Optional sampling rate in Hz (default: 250 Hz)
"""

import sys
import time
import pytracker


def main():
    """Main function for tracker testing."""
    print("PyTracker Tracker Test")
    print("=" * 40)
    
    # Initialize tracker
    try:
        tracker = pytracker.Tracker()
        tracker.print_discovered_objects()
    except Exception as e:
        print(f"Error initializing tracker: {e}")
        return 1

    # Check if tracker is available
    if "tracker_1" not in tracker.devices:
        print("Error: No tracker found. Make sure your VR system is running.")
        return 1

    # Parse command line arguments
    if len(sys.argv) == 1:
        interval = 1 / 250  # Default 250 Hz
    elif len(sys.argv) == 2:
        try:
            interval = 1 / float(sys.argv[1])
        except ValueError:
            print("Invalid sample rate. Using default 250 Hz.")
            interval = 1 / 250
    else:
        print("Usage: python -m pytracker.examples.test_tracker [sample_rate]")
        return 1

    print(f"Sampling at {1/interval:.1f} Hz")
    print("Press Ctrl+C to exit")
    print("=" * 40)

    try:
        while True:
            start = time.time()
            txt = ""
            
            # Get tracker pose
            pose = tracker.devices["tracker_1"].get_pose_euler()
            if pose is not None:
                for value in pose:
                    txt += f"{value:.4f} "
                print(f"\r{txt}", end="", flush=True)
            else:
                print("\rNo valid pose data", end="", flush=True)
            
            # Maintain sampling rate
            sleep_time = interval - (time.time() - start)
            if sleep_time > 0:
                time.sleep(sleep_time)
                
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        return 0
    except Exception as e:
        print(f"\nError during tracking: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
