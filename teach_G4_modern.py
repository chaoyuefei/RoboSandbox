#!/usr/bin/env python
"""
@author Jesse Haviland
Modified to use the new teach() method from GenericDH class
"""

import robosandbox as rsb

# Create a GenericFour robot
G4 = rsb.models.URDF.GenericFour()

# Launch the interactive teaching interface
# This replaces all the manual Swift setup and slider creation
G4.teach_gui()