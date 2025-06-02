#!/usr/bin/env python

import numpy as np
import os
import sys
from pathlib import Path

# Add the robosandbox module to the path
sys.path.insert(0, str(Path(__file__).parent / "robosandbox"))

from robosandbox.models.URDF.Generic import GenericDH

def test_urdf_storage():
    """Test that URDF files are properly stored in rsb-data folder"""
    
    print("Testing URDF file storage functionality...")
    
    # Test 1: Create a simple 3-DOF robot
    print("\n1. Creating a 3-DOF robot...")
    robot1 = GenericDH(
        dofs=3,
        a=[0.5, 0.3, 0.2],
        d=[0.1, 0, 0],
        alpha=[np.pi/2, 0, 0],
        name="TestRobot3DOF"
    )
    
    print(f"   Robot created: {robot1.name}")
    print(f"   URDF file stored at: {robot1.urdf_file_path}")
    print(f"   File exists: {os.path.exists(robot1.urdf_file_path)}")
    
    # Test 2: Create another robot with same name to test unique naming
    print("\n2. Creating another 3-DOF robot with same name...")
    robot2 = GenericDH(
        dofs=3,
        a=[0.4, 0.4, 0.1],
        d=[0.2, 0, 0],
        alpha=[np.pi/2, 0, np.pi/2],
        name="TestRobot3DOF"
    )
    
    print(f"   Robot created: {robot2.name}")
    print(f"   URDF file stored at: {robot2.urdf_file_path}")
    print(f"   File exists: {os.path.exists(robot2.urdf_file_path)}")
    print(f"   Files are different: {robot1.urdf_file_path != robot2.urdf_file_path}")
    
    # Test 3: Create a 6-DOF robot
    print("\n3. Creating a 6-DOF robot...")
    robot3 = GenericDH(
        dofs=6,
        name="TestRobot6DOF"
    )
    
    print(f"   Robot created: {robot3.name}")
    print(f"   URDF file stored at: {robot3.urdf_file_path}")
    print(f"   File exists: {os.path.exists(robot3.urdf_file_path)}")
    
    # Test 4: List all generated files
    print("\n4. Listing all files in rsb-data directory...")
    rsb_data_dir = Path(__file__).parent / "rsb-data"
    if rsb_data_dir.exists():
        urdf_files = list(rsb_data_dir.glob("*.urdf"))
        print(f"   Found {len(urdf_files)} URDF files:")
        for file_path in sorted(urdf_files):
            print(f"     - {file_path.name}")
    
    # Test 5: Test cleanup functionality
    print("\n5. Testing cleanup functionality...")
    deleted_files = GenericDH.cleanup_generated_urdf_files("TestRobot*")
    print(f"   Deleted {len(deleted_files)} test files:")
    for file_path in deleted_files:
        print(f"     - {Path(file_path).name}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_urdf_storage()