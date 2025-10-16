#!/usr/bin/env python3
"""
3D Tracker Visualizer Example

This example provides a real-time 3D visualization of tracker pose data,
including position, orientation, and motion trail.

Usage:
    python -m pytracker.examples.visualizer [device_name] [update_rate] [trail_length]
    
    device_name: Name of the device to visualize (default: "tracker_1")
    update_rate: Update frequency in Hz (default: 60)
    trail_length: Number of trail points (default: 1000)
"""

import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform

import pytracker


class Arrow3D(FancyArrowPatch):
    """Custom 3D arrow class for orientation visualization."""
    
    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)


def euler_to_rotation_matrix(yaw, pitch, roll):
    """Convert Euler angles to rotation matrix."""
    yaw_rad = np.radians(yaw)
    pitch_rad = np.radians(pitch)
    roll_rad = np.radians(roll)
    
    # Rotation matrix for yaw (around Z axis)
    R_z = np.array([
        [np.cos(yaw_rad), -np.sin(yaw_rad), 0],
        [np.sin(yaw_rad), np.cos(yaw_rad), 0],
        [0, 0, 1]
    ])
    
    # Rotation matrix for pitch (around Y axis)
    R_y = np.array([
        [np.cos(pitch_rad), 0, np.sin(pitch_rad)],
        [0, 1, 0],
        [-np.sin(pitch_rad), 0, np.cos(pitch_rad)]
    ])
    
    # Rotation matrix for roll (around X axis)
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(roll_rad), -np.sin(roll_rad)],
        [0, np.sin(roll_rad), np.cos(roll_rad)]
    ])
    
    # Combined rotation matrix
    R = R_z @ R_y @ R_x
    return R


class TrackerVisualizer:
    """Real-time 3D tracker visualizer."""
    
    def __init__(self, device_name="tracker_1", update_rate=60, trail_length=100):
        """
        Initialize tracker visualizer.
        
        Args:
            device_name: Name of the device to visualize
            update_rate: Update frequency (Hz)
            trail_length: Number of trail points
        """
        self.tracker = pytracker.Tracker()
        self.device_name = device_name
        self.update_interval = 1000 / update_rate  # milliseconds
        self.trail_length = trail_length
        
        # Store trail data
        self.trail_x = []
        self.trail_y = []
        self.trail_z = []
        
        # Store pose data for error calculation
        self.pose_history = []
        self.max_history = 50  # Keep last 50 poses for error calculation
        
        # Print discovered devices
        print("Discovered devices:")
        self.tracker.print_discovered_objects()
        print(f"\nVisualizing device: {device_name}")
        print("Close window to exit...")
        
        # Create figure with space for info panel
        self.fig = plt.figure(figsize=(16, 9), dpi=100)
        # Adjust subplot to leave space on the right for info panel
        self.ax = self.fig.add_subplot(111, projection='3d', position=[0.05, 0.05, 0.65, 0.9])
        
        # Initialize plot elements
        self.scatter = None
        self.trail_line = None
        self.arrows = []
        
        # Set initial view angle
        self.ax.view_init(elev=20, azim=45)
        
    def update(self, frame):
        """Update function for animation."""
        try:
            # Get current pose
            pose = self.tracker.devices[self.device_name].get_pose_euler()
            
            if pose is None:
                return
            
            x, y, z, yaw, pitch, roll = pose
            
            # Add to pose history for error calculation
            self.pose_history.append([x, y, z, yaw, pitch, roll])
            if len(self.pose_history) > self.max_history:
                self.pose_history.pop(0)
            
            # Calculate errors (standard deviation over recent poses)
            if len(self.pose_history) > 1:
                history_array = np.array(self.pose_history)
                pos_std = np.std(history_array[:, :3], axis=0)  # Position std
                ang_std = np.std(history_array[:, 3:], axis=0)  # Angle std
                
                # Calculate velocity (change from last frame)
                last_pose = self.pose_history[-2]
                dx = x - last_pose[0]
                dy = y - last_pose[1]
                dz = z - last_pose[2]
                velocity = np.sqrt(dx**2 + dy**2 + dz**2) / (self.update_interval / 1000)
            else:
                pos_std = np.zeros(3)
                ang_std = np.zeros(3)
                velocity = 0.0
            
            # Add to trail
            self.trail_x.append(x)
            self.trail_y.append(y)
            self.trail_z.append(z)
            
            # Limit trail length
            if len(self.trail_x) > self.trail_length:
                self.trail_x.pop(0)
                self.trail_y.pop(0)
                self.trail_z.pop(0)
            
            # Clear current plot
            self.ax.clear()
            
            # Draw trail
            if len(self.trail_x) > 1:
                self.ax.plot(self.trail_x, self.trail_y, self.trail_z, 
                           'b-', alpha=0.3, linewidth=1, label='Trail')
            
            # Draw current position
            self.ax.scatter([x], [y], [z], c='red', marker='o', s=100, label='Current Position')
            
            # Calculate rotation matrix
            R = euler_to_rotation_matrix(yaw, pitch, roll)
            
            # Draw coordinate axes (representing orientation)
            axis_length = 0.1
            
            # X-axis (red)
            x_axis = R @ np.array([axis_length, 0, 0])
            self.ax.plot([x, x + x_axis[0]], 
                        [y, y + x_axis[1]], 
                        [z, z + x_axis[2]], 
                        'r-', linewidth=3, label='X-axis')
            
            # Y-axis (green)
            y_axis = R @ np.array([0, axis_length, 0])
            self.ax.plot([x, x + y_axis[0]], 
                        [y, y + y_axis[1]], 
                        [z, z + y_axis[2]], 
                        'g-', linewidth=3, label='Y-axis')
            
            # Z-axis (blue)
            z_axis = R @ np.array([0, 0, axis_length])
            self.ax.plot([x, x + z_axis[0]], 
                        [y, y + z_axis[1]], 
                        [z, z + z_axis[2]], 
                        'b-', linewidth=3, label='Z-axis')
            
            # Set axis ranges (adaptive)
            if len(self.trail_x) > 0:
                # Calculate appropriate range
                margin = 0.5
                x_center = np.mean(self.trail_x[-min(50, len(self.trail_x)):])
                y_center = np.mean(self.trail_y[-min(50, len(self.trail_y)):])
                z_center = np.mean(self.trail_z[-min(50, len(self.trail_z)):])
                
                self.ax.set_xlim([x_center - margin, x_center + margin])
                self.ax.set_ylim([y_center - margin, y_center + margin])
                self.ax.set_zlim([z_center - margin, z_center + margin])
            
            # Set labels
            self.ax.set_xlabel('X (meters)', fontsize=10)
            self.ax.set_ylabel('Y (meters)', fontsize=10)
            self.ax.set_zlabel('Z (meters)', fontsize=10)
            
            # Set title
            title = f'{self.device_name} Real-time Pose Tracking'
            self.ax.set_title(title, fontsize=12, pad=10, fontweight='bold')
            
            # Add grid
            self.ax.grid(True, alpha=0.3)
            
            # Add legend
            self.ax.legend(loc='upper left', fontsize=8)
            
            # Create detailed info text box
            info_text = (
                f'╔═══ POSITION ═══╗\n'
                f'X: {x:>8.4f} m  (σ: {pos_std[0]*1000:.2f} mm)\n'
                f'Y: {y:>8.4f} m  (σ: {pos_std[1]*1000:.2f} mm)\n'
                f'Z: {z:>8.4f} m  (σ: {pos_std[2]*1000:.2f} mm)\n'
                f'\n'
                f'╔═══ ORIENTATION ═══╗\n'
                f'Yaw:   {yaw:>7.2f}°  (σ: {ang_std[0]:.2f}°)\n'
                f'Pitch: {pitch:>7.2f}°  (σ: {ang_std[1]:.2f}°)\n'
                f'Roll:  {roll:>7.2f}°  (σ: {ang_std[2]:.2f}°)\n'
                f'\n'
                f'╔═══ MOTION ═══╗\n'
                f'Velocity: {velocity:.3f} m/s\n'
                f'Samples: {len(self.pose_history)}/{self.max_history}'
            )
            
            # Add text box on the right side
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
            self.fig.text(0.98, 0.5, info_text, transform=self.fig.transFigure,
                         fontsize=9, verticalalignment='center', horizontalalignment='right',
                         bbox=props, family='monospace')
            
        except KeyError:
            print(f"Error: Device '{self.device_name}' not found")
            plt.close()
        except Exception as e:
            print(f"Update error: {e}")
    
    def run(self):
        """Run the visualizer."""
        # Create animation
        ani = FuncAnimation(self.fig, self.update, interval=self.update_interval, 
                          cache_frame_data=False, blit=False)
        
        plt.show()


def main():
    """Main function for the visualizer."""
    # Parse command line arguments
    device_name = "tracker_1"
    update_rate = 60  # Hz
    trail_length = 1000  # trail points
    
    if len(sys.argv) > 1:
        device_name = sys.argv[1]
    if len(sys.argv) > 2:
        update_rate = int(sys.argv[2])
    if len(sys.argv) > 3:
        trail_length = int(sys.argv[3])
    
    print("=" * 60)
    print("PyTracker 3D Visualization")
    print("=" * 60)
    print(f"Device name: {device_name}")
    print(f"Update rate: {update_rate} Hz")
    print(f"Trail length: {trail_length} points")
    print("=" * 60)
    
    try:
        visualizer = TrackerVisualizer(device_name, update_rate, trail_length)
        visualizer.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
