# Interactive Teaching Functionality for GenericDH Robots

## Overview

The `GenericDH` class now includes built-in interactive teaching functionality that allows you to control robot joints in real-time using a graphical interface with sliders. This functionality is similar to the MATLAB Robotics Toolbox `teach()` function.

## Methods Available

### `teach_gui(realtime=True, config='qr')`

The main method for launching the interactive teaching interface.

**Parameters:**
- `realtime` (bool, optional): Whether to run the simulation in real-time (default: True)
- `config` (str, optional): Initial configuration to use:
  - `'qr'`: Ready configuration (default)
  - `'qz'`: Zero configuration 
  - `None`: Use current joint configuration

**Returns:** None

### `interactive_teach(**kwargs)`

Convenience method that calls `teach_gui()` with the same parameters.

## Usage Examples

### Basic Usage with GenericFour

```python
import robosandbox as rsb

# Create a GenericFour robot
G4 = rsb.models.URDF.GenericFour()

# Launch interactive teaching interface
G4.teach_gui()
```

### Custom Robot with Specific Configuration

```python
import numpy as np
import robosandbox as rsb

# Create a custom 6-DOF robot
robot = rsb.models.URDF.GenericDH(
    dofs=6,
    a=[0, 0.5, 0.4, 0, 0, 0],
    d=[0.3, 0, 0, 0.4, 0, 0.1],
    alpha=[np.pi/2, 0, np.pi/2, -np.pi/2, np.pi/2, 0],
    name="Custom6DOF"
)

# Start from zero configuration
robot.teach_gui(config='qz')
```

### Alternative Method Names

```python
# These are equivalent:
robot.teach_gui()
robot.interactive_teach()
```

## Features

### Automatic Slider Generation
- Automatically creates sliders for all movable joints
- Sets appropriate joint limits based on robot specifications
- Displays joint angles in degrees for user convenience
- Labels sliders with robot name and joint numbers

### Real-time Control
- Joint angles update in real-time as you move sliders
- Smooth animation in the Swift simulator
- Immediate visual feedback

### Configuration Options
- Start from different initial poses (ready, zero, or current)
- Choose between real-time and non-real-time simulation modes

### User-friendly Interface
- Clear joint limit information displayed in console
- Intuitive degree-based slider controls
- Graceful exit handling (Ctrl+C or window close)
- Final joint configuration printed on exit

## Requirements

The teaching functionality requires the Swift simulator package:

```bash
pip install swift-sim
```

## Migration from Manual Swift Setup

### Old Approach (Manual)
```python
import swift
import robosandbox as rsb
import numpy as np
import time

env = swift.Swift()
env.launch()

G4 = rsb.models.URDF.GenericFour()
G4.q = G4.qr
env.add(G4)

def set_joint(j, value):
    G4.q[j] = np.deg2rad(float(value))

j = 0
for link in G4.links:
    if link.isjoint:
        env.add(swift.Slider(
            lambda x, j=j: set_joint(j, x),
            min=np.round(np.rad2deg(link.qlim[0]), 2),
            max=np.round(np.rad2deg(link.qlim[1]), 2),
            step=1,
            value=np.round(np.rad2deg(G4.q[j]), 2),
            desc="G4 Joint " + str(j),
            unit="&#176;",
        ))
        j += 1

while True:
    env.step(0.0)
    time.sleep(0.01)
```

### New Approach (Built-in)
```python
import robosandbox as rsb

G4 = rsb.models.URDF.GenericFour()
G4.teach_gui()
```

## Benefits

1. **Simplicity**: Reduces 30+ lines of boilerplate code to a single method call
2. **Consistency**: Standardized interface across all GenericDH robots
3. **Robustness**: Built-in error handling and cleanup
4. **User Experience**: Better feedback and information display
5. **Maintainability**: Centralized implementation reduces code duplication

## Error Handling

The method includes comprehensive error handling for:
- Missing Swift simulator package
- Window closure events
- Keyboard interrupts (Ctrl+C)
- General exceptions during simulation

## Console Output Example

```
Teaching interface launched for GenericFour
Robot has 4 joints with the following limits:
  Joint 0: [-180.0°, 180.0°]
  Joint 1: [-180.0°, 180.0°]
  Joint 2: [-180.0°, 180.0°]
  Joint 3: [-180.0°, 180.0°]
Use the sliders to control joint angles. Press Ctrl+C or close the Swift window to exit.

Teaching session ended by user.
Final joint configuration: [12.5 -45.7  30.2  67.8]
```

## Implementation Notes

- The method automatically handles URDF file paths and robot initialization
- Joint limits are properly enforced through slider constraints
- The interface is non-blocking and can be terminated cleanly
- All temporary resources are properly cleaned up on exit