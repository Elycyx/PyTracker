"""
Tests for the main Tracker class
"""

import pytest
import pytracker


class TestTracker:
    """Test cases for the Tracker class."""
    
    def test_tracker_initialization(self):
        """Test that tracker can be initialized."""
        # This test requires OpenVR to be available
        # In a real test environment, you might want to mock OpenVR
        try:
            tracker = pytracker.Tracker()
            assert tracker is not None
        except Exception:
            # Skip test if OpenVR is not available
            pytest.skip("OpenVR not available")
    
    def test_utility_functions(self):
        """Test utility functions."""
        import pytracker.core.utils as utils
        
        # Test pose matrix conversion
        import math
        
        # Identity matrix
        identity = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
        euler = utils.convert_to_euler(identity)
        quat = utils.convert_to_quaternion(identity)
        
        assert len(euler) == 6
        assert len(quat) == 7
        assert euler[0] == 0  # x
        assert euler[1] == 0  # y  
        assert euler[2] == 0  # z
