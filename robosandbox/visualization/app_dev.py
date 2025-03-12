import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import robosandbox as rsb
import numpy as np
from robosandbox.performance.WorkSpace import WorkSpace

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H2("Robot Arm Design App"),
                html.H5("@Chaoyue Fei"),
                html.Div(style={"height": "30px"}),
                html.Hr(),
                dbc.Col(
                    [
                        # Key Parameters Section
                        dbc.Button(
                            "Key Parameters",
                            id="parameters_button",
                            color="info",
                            className="mb-3",
                        ),
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.P("Degrees of Freedom (DOFs):"),
                                        dcc.Slider(
                                            id="dofs_slider",
                                            min=2,
                                            max=7,
                                            step=1,
                                            value=2,
                                            marks={i: str(i) for i in range(2, 8)},
                                            tooltip={
                                                "always_visible": True,
                                                "placement": "bottom",
                                            },
                                        ),
                                        html.Div(
                                            id="dofs_display",
                                            style={"margin": "10px 0"},
                                        ),
                                        html.P(
                                            "Link Lengths [m] (comma-separated, e.g., 1,1.5,2):"
                                        ),
                                        dcc.Input(
                                            id="link_lengths",
                                            value="0.4,0.4,0.4,0.4",
                                            type="text",
                                            style={"width": "100%"},
                                        ),
                                        html.P(
                                            "Alpha Angles [deg] (comma-separated, e.g., 0,30,45):"
                                        ),
                                        dcc.Input(
                                            id="alpha",
                                            value="90,0,0,0",
                                            type="text",
                                            style={"width": "100%"},
                                        ),
                                        html.P(
                                            "qs [deg] (comma-separated, e.g., 0,30,45):"
                                        ),
                                        dcc.Input(
                                            id="qs",
                                            value="90,0,0,0",
                                            type="text",
                                            style={"width": "100%"},
                                        ),
                                    ]
                                )
                            ),
                            id="parameters_collapse",
                            is_open=False,
                        ),
                        # html.Hr(),
                        # Advanced Settings Section (if needed)
                        dbc.Button(
                            "Advanced Settings",
                            id="advanced_button",
                            color="info",
                            className="mb-3",
                        ),
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.P("Workspace Settings:"),
                                        html.P("Initial Samples:"),
                                        dcc.Input(
                                            id="initial_samples",
                                            value="5000",
                                            type="number",
                                            style={"width": "100%"},
                                        ),
                                        html.P("Batch Ratio:"),
                                        dcc.Input(
                                            id="batch_ratio",
                                            value="0.1",
                                            type="number",
                                            step=0.01,
                                            style={"width": "100%"},
                                        ),
                                        html.P("Error Tolerance (%):"),
                                        dcc.Input(
                                            id="error_tolerance",
                                            value="0.001",
                                            type="number",
                                            step=0.0001,
                                            style={"width": "100%"},
                                        ),
                                    ]
                                )
                            ),
                            id="advanced_collapse",
                            is_open=False,
                        ),
                        html.Hr(),
                        # Command Section
                        html.Div(
                            [
                                html.H5("Command"),
                                dbc.Button(
                                    "Generate Robot Arm",
                                    id="generate_button",
                                    color="primary",
                                    style={"margin": "5px"},
                                ),
                                dbc.Button(
                                    "Workspace Analysis",
                                    id="workspace_button",
                                    color="primary",
                                    style={"margin": "5px"},
                                ),
                            ]
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.H5("Visualization"),
                        dbc.Spinner(
                            dcc.Graph(
                                id="main_display",
                                style={"height": "75vh"},
                            ),
                            color="primary",
                        ),
                        html.Div(id="output", style={"margin-top": "20px"}),
                    ],
                    width=8,
                ),
            ]
        ),
    ],
    fluid=True,
)


def initialize_robot(dofs, link_lengths, alpha):
    """Helper function to initialize the robot based on DOFs."""
    alpha_rad = [np.deg2rad(a) for a in alpha]
    robot_classes = {
        2: rsb.models.DH.Generic.GenericTwo,
        3: rsb.models.DH.Generic.GenericThree,
        4: rsb.models.DH.Generic.GenericFour,
        5: rsb.models.DH.Generic.GenericFive,
        6: rsb.models.DH.Generic.GenericSix,
        7: rsb.models.DH.Generic.GenericSeven,
    }
    robot_class = robot_classes.get(dofs)
    if not robot_class:
        raise ValueError(f"DOFs of {dofs} not supported.")
    return robot_class(linklengths=link_lengths, alpha=alpha_rad)


@app.callback(
    Output("parameters_collapse", "is_open"),
    [Input("parameters_button", "n_clicks")],
    [State("parameters_collapse", "is_open")],
)
def toggle_parameters_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@app.callback(
    Output("advanced_collapse", "is_open"),
    [Input("advanced_button", "n_clicks")],
    [State("advanced_collapse", "is_open")],
)
def toggle_advanced_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@app.callback(
    Output("dofs_display", "children"),
    Input("dofs_slider", "value"),
)
def update_dofs_display(selected_dofs):
    return f"Selected DOFs: {selected_dofs}"


@app.callback(
    Output("main_display", "figure"),
    Output("output", "children"),
    Input("generate_button", "n_clicks"),
    Input("workspace_button", "n_clicks"),
    State("dofs_slider", "value"),
    State("link_lengths", "value"),
    State("alpha", "value"),
    State("qs", "value"),
    State("initial_samples", "value"),
    State("batch_ratio", "value"),
    State("error_tolerance", "value"),
)
def update_visualization(
    generate_clicks,
    workspace_clicks,
    dofs,
    link_lengths,
    alpha,
    qs,
    initial_samples,
    batch_ratio,
    error_tolerance,
):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Initialize empty figure and default message
    fig = go.Figure()
    message = "Please click a button to generate visualization."

    if button_id is None:
        return fig, message

    try:
        # Parse input values
        link_lengths = [float(length.strip()) for length in link_lengths.split(",")]
        alpha = [float(angle.strip()) for angle in alpha.split(",")]
        qs = [float(q.strip()) for q in qs.split(",")]

        # Parse advanced settings
        initial_samples = int(initial_samples) if initial_samples else 5000
        batch_ratio = float(batch_ratio) if batch_ratio else 0.1
        error_tolerance = float(error_tolerance) if error_tolerance else 0.001

    except ValueError:
        return fig, "Please enter valid numbers for input parameters."

    try:
        # Initialize robot
        robot = initialize_robot(dofs, link_lengths, alpha)

        # Plot the robot arm
        if button_id == "generate_button":
            fig = go.Figure()
            robot.plotly(np.deg2rad(qs), isShow=False, fig=fig, isUpdate=True)
            message = f"Generated a robotic arm with {dofs} DOFs."

        elif button_id == "workspace_button":
            fig = go.Figure()
            robot.plotly(np.deg2rad(qs), isShow=False, fig=fig, isUpdate=True)

            ws = WorkSpace(robot)
            G = ws.iter_calc_global_indice(
                initial_samples=initial_samples,
                batch_ratio=batch_ratio,
                error_tolerance_percentage=error_tolerance,
                method="invcondition",
                axes="all",
                max_samples=50000,
            )
            ws.plot(color="invcondition", fig=fig, isShow=False)
            fig.update_layout(showlegend=False)
            message = f"Performed workspace analysis for a {dofs} DOF robot."

        # Update layout if necessary
        fig.update_layout(
            scene=dict(
                xaxis=dict(title="X", range=[-2, 2]),
                yaxis=dict(title="Y", range=[-2, 2]),
                zaxis=dict(title="Z", range=[-2, 2]),
            ),
            margin=dict(l=0, r=0, b=0, t=30),
        )

    except Exception as e:
        return dash.no_update, f"Error: {e}"

    return fig, message


if __name__ == "__main__":
    app.run(debug=True)
