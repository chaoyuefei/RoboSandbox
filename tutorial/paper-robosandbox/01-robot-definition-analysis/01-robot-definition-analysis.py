import marimo

__generated_with = "0.11.30"
app = marimo.App(width="full", auto_download=["ipynb"])


@app.cell
def _():
    import robosandbox as rsb
    import numpy as np
    import plotly.graph_objects as go # import new fig env
    import marimo as mo
    return go, mo, np, rsb


@app.cell
def _(mo):
    mo.md(
        r"""
        # Robot Definition and Analysis

        The "models" subpackage offers a variety of robotic manipulator models that use different description methodologies, such as DH parameters and screw theory. Currently, all the models can be classified into three categories:

        - DH: created using Denavit-Hartenberg Parameters, for example: ro⊥=rsb.⊨.DH.Ge≠ric.Ge≠ricFour()robot = rsb.models.DH.Generic.GenericFour(), powered by (roboticstoolbox-python)[https://github.com/petercorke/robotics-toolbox-python]
        - DHLink: created using Denavit-Hartenberg Parameters, taking into consideration the design of the links.
        - MR: created using screw theory, based on (Modern Robotics)[https://hades.mech.northwestern.edu/index.php/Modern_Robotics] and (code)[https://github.com/NxRLab/ModernRobotics]
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## DH Models

        ### Generic Models
        We can easily define a robotic manipulate using DH parameters in RoboSandbox. To give a quick start, several pre-defined models are offered **from 2 Dofs to 7 Dofs**:
        """
    )
    return


@app.cell
def _(go):
    import robosandbox.models.DH.Generic as generic
    robot4 = generic.GenericFour()
    robot4.plotly(robot4.qz, fig=go.Figure(), isShow=False) # In the Marimo notebook, use the "fig" parameter for improved visual effects.
    return generic, robot4


@app.cell
def _(generic, go):
    robot6 = generic.GenericSix()
    robot6.plotly(robot6.qz, fig=go.Figure(), isShow=False)
    return (robot6,)


@app.cell
def _(mo):
    mo.md(
        """
        ### Commercial Models

        In addition to generic models, several commercial robots are available, such as **Panda, Puma 560, and UR5**.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""#### Panda""")
    return


@app.cell
def _(go, rsb):
    Panda = rsb.models.DH.Panda()
    Panda.plotly(Panda.qr, fig=go.Figure(), isShow=False)
    return (Panda,)


@app.cell
def _(mo):
    mo.md(r"""#### Puma 560""")
    return


@app.cell
def _(go, rsb):
    Puma560 = rsb.models.DH.Puma560()
    Puma560.plotly(Puma560.qr, fig=go.Figure(), isShow=False)
    return (Puma560,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Make a change

        Beginning with the default settings, we can easily adjust the robot's link length and actuator directions. These are important design parameters that we will explore further in the optimization chapter.
        """
    )
    return


@app.cell
def _(generic, go, np):
    new_robot = generic.GenericFour(
                    linklengths=[0.5, 0.5, 0.5, 0.5], 
                    alpha=[0, np.pi/2, np.pi/2, 0],
                )

    new_robot.plotly(new_robot.qz, fig=go.Figure(), isShow=False)
    return (new_robot,)


@app.cell
def _(mo):
    mo.md(r"""## Workspace Analysis""")
    return


@app.cell
def _(mo):
    mo.md(r"""### Link Length Influence""")
    return


@app.cell
def _(np, rsb):
    from robosandbox.performance.workspace import WorkSpace
    np.random.seed(42)

    robot_planar = rsb.models.DH.Generic.GenericFour()
    ws = WorkSpace(robot_planar)
    method = "yoshikawa"
    axes = "trans"

    G = ws.global_indice(
        initial_samples=5000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-2,
        method="yoshikawa", 
        axes=axes,
        max_samples=20000, 
        is_normalized=False
    )
    print(f"The Global Manipulability of a planar robot with 4 Dofs is {G}")
    return G, WorkSpace, axes, method, robot_planar, ws


@app.cell
def _(go, method, ws):
    ws.plot(color=method, fig=go.Figure(), isShow=True, isUpdate=True)
    return


@app.cell
def _(mo):
    mo.md(r"""### GUI""")
    return


@app.cell
def _():
    # import threading

    # # Create your Dash app but don't run the server
    # design_app = rsb.visualization.app.RobotArmDesignApp()

    # # Start the Dash server in background
    # dash_thread = threading.Thread(target=design_app.run_server, daemon=True)
    # dash_thread.start()

    # # Create iframe using HTML
    # dash_frame = mo.md("""
    # <iframe src="http://127.0.0.1:8050" width="100%" height="800px" frameborder="0"></iframe>
    # """)

    # # Display the iframe
    # mo.output.append(dash_frame)
    return


@app.cell
def _():
    # app = rsb.visualization.app_standalone.RobotArmDesignAppStandalone()
    # app.run_app()
    return


if __name__ == "__main__":
    app.run()
