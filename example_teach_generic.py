#!/usr/bin/env python
"""
Example script demonstrating the teach() method for GenericDH robots

This script shows how to use the new teach() functionality to interactively
control robot joints using sliders in the Swift simulator.
"""

import sys
from pathlib import Path
import numpy as np

# Add robosandbox to path
sys.path.insert(0, str(Path(__file__).parent / "robosandbox"))

import robosandbox as rsb


def demo_generic_four_teach():
    """Demonstrate teach functionality with GenericFour robot"""
    print("Creating GenericFour robot...")
    robot = rsb.models.URDF.GenericFour()

    print(f"Robot: {robot.name}")
    print(f"DOF: {robot.n}")
    print("\nLaunching teach interface...")
    print("Note: This will open a Swift simulator window with sliders")

    # Launch teaching interface
    robot.teach()


def demo_custom_generic_teach():
    """Demonstrate teach functionality with custom GenericDH robot"""
    print("\nCreating custom 6-DOF robot...")

    # Create a 6-DOF robot with custom DH parameters
    robot = rsb.models.URDF.GenericDH(
        dofs=6,
        a=[0, 0.5, 0.4, 0, 0, 0],
        d=[0.3, 0, 0, 0.4, 0, 0.1],
        alpha=[np.pi / 2, 0, np.pi / 2, -np.pi / 2, np.pi / 2, 0],
        name="Custom6DOF",
    )

    print(f"Robot: {robot.name}")
    print(f"DOF: {robot.n}")
    print("\nLaunching teach interface starting from zero configuration...")

    # Launch teaching interface starting from zero position
    robot.teach(config="qz")


def demo_simple_3dof():
    """Demonstrate with a simple 3-DOF robot"""
    print("\nCreating simple 3-DOF robot...")

    robot = rsb.models.URDF.GenericDH(
        dofs=3,
        a=[0.3, 0.3, 0.2],
        d=[0.2, 0, 0],
        alpha=[np.pi / 2, 0, 0],
        name="Simple3DOF",
    )

    print(f"Robot: {robot.name}")
    print(f"DOF: {robot.n}")
    print("\nLaunching teach interface...")

    robot.teach()


if __name__ == "__main__":
    print("GenericDH Robot Teaching Interface Demo")
    print("=" * 40)

    # Uncomment the demo you want to run:

    # Demo 1: GenericFour robot (4-DOF)
    demo_generic_four_teach()

    # Demo 2: Custom 6-DOF robot
    # demo_custom_generic_teach()

    # Demo 3: Simple 3-DOF robot
    # demo_simple_3dof()
