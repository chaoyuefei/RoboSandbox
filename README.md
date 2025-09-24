# RoboSandbox for Manipulator Design and Analysis

[![Powered by the Robotics Toolbox](https://raw.githubusercontent.com/petercorke/robotics-toolbox-python/master/.github/svg/rtb_powered.min.svg)](https://github.com/petercorke/robotics-toolbox-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/chaoyuefei/RoboSandbox/workflows/CI/badge.svg)](https://github.com/chaoyuefei/RoboSandbox/actions?query=workflow%3Aci)
<table style="border:0px">
<tr style="border:0px">
<td style="border:0px">
<img src="docs/figs/robosandbox_icon.jpeg" width="200"></td>
<td style="border:0px">
An Open-Source Python Toolbox for Manipulator Design and Analysis
</td>
</tr>
</table>

<!-- <br> -->

## Contents

- [Synopsis](#1)
- [Tutorials](#3)
- [Code Examples](#4)


<br>

<a id='1'></a>
## Synopsis

RoboSandbox (rsb), an open-source Python package, invented for robotic manipulator design and analysis. The design goals are:
- **user-friendly**: it is easy to install, use, and interact with. A nicely designed interative application is provided for robot design and analysis.
- **accessible**: it is open-source, well-documented, and well-tested, and can be accessed on various operating systems such as Windows, Linux, and MacOS.
- **extensible**: the code structure is extensible, allowing for the easy integration of new features and functionalities, such as the incorporation of additional indices to measure robotic performance.

## Installation

### Local Installation

To install RoboSandbox, it is recommended to use uv, a lightweight and fast package manager. You can install it by following the instructions on the [official website](https://uvpkg.com/).

```bash
git clone git@github.com:chaoyuefei/RoboSandbox.git
cd RoboSandbox
uv sync
uv run src/robosandbox/visualization/app_standalone.py
```

To run the tests, use the following command:

```bash
uv run pytest tests/
```

## Tutorials
