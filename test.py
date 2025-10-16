import pytracker

# Initialize the tracker
tracker = pytracker.Tracker()

# Print discovered devices
tracker.print_discovered_objects()

# Get pose data from a tracker
pose = tracker.devices["tracker_1"].get_pose_euler()
print(f"Position: {pose[:3]}, Orientation: {pose[3:]}")