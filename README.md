# RoboSandbox for Manipulator Design and Analysis

[![Powered by the Robotics Toolbox](https://raw.githubusercontent.com/petercorke/robotics-toolbox-python/master/.github/svg/rtb_powered.min.svg)](https://github.com/petercorke/robotics-toolbox-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/chaoyuefei/RoboSandbox/workflows/CI/badge.svg)](https://github.com/chaoyuefei/RoboSandbox/actions?query=workflow%3Aci)
<table style="border:0px">
<tr style="border:0px">
<td style="border:0px">
<img src="docs/figs/robosandbox_icon.jpeg" width="200"></td>
<td style="border:0px">
An Open-Source Python Framework for Manipulator Design and Analysis
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

RoboSandbox, an open-source Python framework designed for robotic manipulator design and analysis. Different robot models and their workspaces can be evaluated, providing a unified environment for reach, global index, and other performance metrics.

The design goals are:

- **accessibility**: being open-source, documented, and widely tested to ensure reliability and reproducibility, while also providing crossplatform compatibility across Windows, Linux, and MacOS environments.
- **extensibility**: It emphasizes extensibility through a modular structure that facilitates seamless integration of new features and functionalities, such as the addition of extra indices for measuring robotic performance.
- **optimization-driven**: the system supports optimization-driven manipulator design processes through its modular architecture, where submodules can integrate into optimization loops to enable iterative design refinement and evaluation.

<img src="docs/figs/optimization_driven_loop.png" width="650">

## Installation

### Local Installation

To install RoboSandbox, it is recommended to use uv, a lightweight and fast package manager. You can install it by following the [instructions](https://docs.astral.sh/uv/guides/install-python/)

After installing uv, you can install RoboSandbox with the following command:

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
