import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import robosandbox as rsb
import numpy as np
from robosandbox.performance.workspace import WorkSpace
from threading import Thread
import webview

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
                        html.H5("Parameters"),
                        html.Div(style={"height": "10px"}),
                        # Key Parameters Section
                        dbc.Button(
                            "Kinematic Configuration",
                            id="parameters_button",
                            color="info",
                            className="mb-3",
                            style={"width": "80%"},
                        ),
                        dbc.Collapse(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.P("Select Robot:"),
                                        # Simplified dropdown with all robots in a single list
                                        dcc.Dropdown(
                                            id="robot_selection",
                                            options=[
                                                {
                                                    "label": "Franka Emika Panda",
                                                    "value": "panda",
                                                },
                                                {
                                                    "label": "Puma 560",
                                                    "value": "puma560",
                                                },
                                                {
                                                    "label": "Generic 2 DOFs",
                                                    "value": "generic_2",
                                                },
                                                {
                                                    "label": "Generic 3 DOFs",
                                                    "value": "generic_3",
                                                },
                                                {
                                                    "label": "Generic 4 DOFs",
                                                    "value": "generic_4",
                                                },
                                                {
                                                    "label": "Generic 5 DOFs",
                                                    "value": "generic_5",
                                                },
                                                {
                                                    "label": "Generic 6 DOFs",
                                                    "value": "generic_6",
                                                },
                                                {
                                                    "label": "Generic 7 DOFs",
                                                    "value": "generic_7",
                                                },
                                            ],
                                            value="generic_2",
                                            clearable=False,
                                            style={"width": "100%"},
                                        ),
                                        html.Div(
                                            id="robot_info_display",
                                            style={"margin": "10px 0"},
                                        ),
                                        # Parameters section (shown only for generic robots)
                                        html.Div(
                                            id="generic_robot_params",
                                            children=[
                                                html.P(
                                                    "Link Lengths [m] (comma-separated, e.g., 1,1.5,2):"
                                                ),
                                                dcc.Input(
                                                    id="link_lengths",
                                                    value="0.4,0.4",
                                                    type="text",
                                                    style={"width": "100%"},
                                                ),
                                                html.P(
                                                    "Alpha Angles [deg] (comma-separated, e.g., 0,30,45):"
                                                ),
                                                dcc.Input(
                                                    id="alpha",
                                                    value="90,0",
                                                    type="text",
                                                    style={"width": "100%"},
                                                ),
                                                html.P(
                                                    "qs [deg] (comma-separated, e.g., 0,30,45):"
                                                ),
                                                dcc.Input(
                                                    id="qs",
                                                    value="0,0",
                                                    type="text",
                                                    style={"width": "100%"},
                                                ),
                                            ],
                                            style={"display": "block"},
                                        ),
                                        # Joint configuration for commercial robots
                                        html.Div(
                                            id="commercial_robot_params",
                                            children=[
                                                html.P(
                                                    "Joint configuration [deg] (comma-separated):"
                                                ),
                                                dcc.Input(
                                                    id="commercial_qs",
                                                    value="0,0,0,0,0,0,0",
                                                    type="text",
                                                    style={"width": "100%"},
                                                ),
                                            ],
                                            style={"display": "none"},
                                        ),
                                    ]
                                )
                            ),
                            id="parameters_collapse",
                            is_open=False,
                            style={"width": "80%"},
                        ),
                        # html.Hr(),
                        html.Div(style={"height": "5px"}),
                        # Advanced Settings Section
                        dbc.Button(
                            "Workspace Settings",
                            id="advanced_button",
                            color="info",
                            className="mb-3",
                            style={"width": "80%"},
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
                                        html.P("Method:"),
                                        dcc.Dropdown(
                                            id="method_dropdown",
                                            options=[
                                                {
                                                    "label": "Inverse Condition",
                                                    "value": "invcondition",
                                                },
                                                {
                                                    "label": "Yoshikawa",
                                                    "value": "yoshikawa",
                                                },
                                            ],
                                            value="invcondition",
                                            style={"width": "100%"},
                                        ),
                                        html.P("Axes:"),
                                        dcc.Dropdown(
                                            id="axes_dropdown",
                                            options=[
                                                {
                                                    "label": "All (Translation + Rotation)",
                                                    "value": "all",
                                                },
                                                {
                                                    "label": "Translation Only",
                                                    "value": "trans",
                                                },
                                            ],
                                            value="all",
                                            style={"width": "100%"},
                                        ),
                                        html.P("Normalization:"),
                                        dcc.Slider(
                                            id="ws_normalization_slider",
                                            min=0,
                                            max=1,
                                            step=1,
                                            marks={
                                                0: {
                                                    "label": "False",
                                                    "style": {"color": "#77b0b1"},
                                                },
                                                1: {
                                                    "label": "True",
                                                    "style": {"color": "#77b0b1"},
                                                },
                                            },
                                            value=0,
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
                                html.Div(style={"height": "10px"}),
                                dbc.Button(
                                    "Display Robot Arm",
                                    id="generate_button",
                                    color="primary",
                                    style={"width": "80%"},
                                ),
                                html.Div(style={"height": "20px"}),
                                dbc.Button(
                                    "Workspace Analysis",
                                    id="workspace_button",
                                    color="primary",
                                    style={"width": "80%"},
                                ),
                            ]
                        ),
                    ],
                    width=3,
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
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H5("Results"),
                        html.Div(style={"height": "10px"}),
                        # Add table to display results
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    # html.H5("Robot Metrics", className="card-title"),
                                    html.Div(
                                        id="results_table"
                                    ),  # This will contain the table
                                ]
                            )
                        ),
                    ],
                    width=3,
                ),
            ]
        ),
    ],
    fluid=True,
)


def get_robot(robot_selection, link_lengths=None, alpha=None):
    """Helper function to initialize the robot based on selection."""
    # Commercial robots
    if robot_selection == "panda":
        return rsb.models.DH.Panda()
    elif robot_selection == "puma560":
        return rsb.models.DH.Puma560()

    # Generic robots
    elif robot_selection.startswith("generic_"):
        dofs = int(robot_selection.split("_")[1])
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

    else:
        raise ValueError(f"Robot selection '{robot_selection}' not recognized.")


@app.callback(
    [
        Output("robot_info_display", "children"),
        Output("generic_robot_params", "style"),
        Output("commercial_robot_params", "style"),
        Output("commercial_qs", "value"),
        # Add these new outputs
        Output("link_lengths", "value"),
        Output("alpha", "value"),
        Output("qs", "value"),
    ],
    Input("robot_selection", "value"),
)
def update_robot_info(robot_selection):
    """Update the display and parameter fields based on robot selection."""
    if robot_selection.startswith("generic_"):
        dofs = int(robot_selection.split("_")[1])

        # Create default values based on the number of DOFs
        default_link_lengths = ",".join(["0.4"] * dofs)

        # For alpha angles, typically first joint is 90 degrees, rest are 0
        default_alpha = ["90"] + ["0"] * (dofs - 1)
        default_alpha_str = ",".join(default_alpha)

        # Default joint angles all set to 0
        default_qs = ",".join(["0"] * dofs)

        return (
            f"Selected Generic Robot with {dofs} DOFs",
            {"display": "block"},  # Show generic robot parameters
            {"display": "none"},  # Hide commercial robot parameters
            "0,0,0,0,0,0,0",  # Default joint values for commercial (not used)
            default_link_lengths,  # Update link lengths based on DOFs
            default_alpha_str,  # Update alpha angles based on DOFs
            default_qs,  # Update qs values based on DOFs
        )
    elif robot_selection == "panda":
        return (
            "Selected Franka Emika Panda (7 DOFs)",
            {"display": "none"},  # Hide generic robot parameters
            {"display": "block"},  # Show commercial robot parameters
            "0,0,0,0,0,0,0",  # Default joint values for Panda
            "0.4,0.4,0.4,0.4,0.4,0.4,0.4",  # Not used but needed for output
            "90,0,0,0,0,0,0",  # Not used but needed for output
            "0,0,0,0,0,0,0",  # Not used but needed for output
        )
    elif robot_selection == "puma560":
        return (
            "Selected Puma 560 (6 DOFs)",
            {"display": "none"},  # Hide generic robot parameters
            {"display": "block"},  # Show commercial robot parameters
            "0,0,0,0,0,0",  # Default joint values for Puma 560
            "0.4,0.4,0.4,0.4,0.4,0.4",  # Not used but needed for output
            "90,0,0,0,0,0",  # Not used but needed for output
            "0,0,0,0,0,0",  # Not used but needed for output
        )
    else:
        return (
            "Invalid robot selection",
            {"display": "none"},
            {"display": "none"},
            "",
            "",
            "",
            "",
        )


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
    [
        Output("main_display", "figure"),
        Output("output", "children"),
        Output("results_table", "children"),  # Add new output for the results table
    ],
    Input("generate_button", "n_clicks"),
    Input("workspace_button", "n_clicks"),
    State("robot_selection", "value"),
    State("link_lengths", "value"),
    State("alpha", "value"),
    State("qs", "value"),
    State("commercial_qs", "value"),
    State("initial_samples", "value"),
    State("batch_ratio", "value"),
    State("error_tolerance", "value"),
    State("method_dropdown", "value"),
    State("axes_dropdown", "value"),
    State("ws_normalization_slider", "value"),  # Added normalization slider state
)
def update_visualization(
    generate_clicks,
    workspace_clicks,
    robot_selection,
    link_lengths,
    alpha,
    generic_qs,
    commercial_qs,
    initial_samples,
    batch_ratio,
    error_tolerance,
    method,
    axes,
    is_normalized_value,  # New parameter
):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Initialize empty figure and default message
    fig = go.Figure()
    message = "Please click a button to generate visualization."
    results_table = html.P("No data available. Run workspace analysis to see results.")

    if button_id is None:
        return fig, message, results_table

    try:
        # Determine if we're using a commercial or generic robot
        is_commercial = not robot_selection.startswith("generic_")

        # Parse input values
        if is_commercial:
            qs = [float(q.strip()) for q in commercial_qs.split(",")]
            # Commercial robots have pre-defined parameters
            link_lengths = None
            alpha = None
        else:
            qs = [float(q.strip()) for q in generic_qs.split(",")]
            link_lengths = [float(length.strip()) for length in link_lengths.split(",")]
            alpha = [float(angle.strip()) for angle in alpha.split(",")]

        # Parse advanced settings
        initial_samples = int(initial_samples) if initial_samples else 5000
        batch_ratio = float(batch_ratio) if batch_ratio else 0.1
        error_tolerance = float(error_tolerance) if error_tolerance else 0.001

        # Convert slider value to boolean
        is_normalized = bool(is_normalized_value)

    except ValueError:
        return fig, "Please enter valid numbers for input parameters.", results_table

    try:
        # Initialize robot
        robot = get_robot(robot_selection, link_lengths, alpha)

        # Generate descriptive robot name for feedback messages
        if robot_selection == "panda":
            robot_name = "Franka Emika Panda"
        elif robot_selection == "puma560":
            robot_name = "Puma 560"
        else:
            dofs = robot_selection.split("_")[1]
            robot_name = f"Generic {dofs} DOF Robot"

        # Calculate total arm length
        total_length = 0
        if is_commercial:
            # For commercial robots, sum the a values from DH parameters
            # total_length = sum([abs(dh[0]) for dh in robot.dh_params])
            # if robot_selection == "panda":
            #     total_length =
            total_length = "N/A"
        else:
            # For generic robots, use the provided link lengths
            total_length = sum(link_lengths)

        # Create table with only length for now
        if total_length == "N/A":
            text_length = "N/A"
        else:
            text_length = f"{total_length:.3f}"

        # Plot the robot arm
        if button_id == "generate_button":
            fig = go.Figure()
            robot.plotly(np.deg2rad(qs), isShow=False, fig=fig, isUpdate=True)
            message = f"Generated {robot_name}."

            results_table = dbc.Table(
                [
                    html.Thead(html.Tr([html.Th("Metric"), html.Th("Value")])),
                    html.Tbody(
                        [
                            html.Tr(
                                [
                                    html.Td("Total Arm Length [m]"),
                                    html.Td(text_length),
                                ]
                            ),
                            html.Tr(
                                [
                                    html.Td("Global Manipulability (G)"),
                                    html.Td("Run workspace analysis"),
                                ]
                            ),
                        ]
                    ),
                ],
                bordered=True,
                hover=True,
                striped=True,
                size="sm",
            )

        elif button_id == "workspace_button":
            fig = go.Figure()
            robot.plotly(np.deg2rad(qs), isShow=False, fig=fig, isUpdate=True)

            ws = WorkSpace(robot)
            G = ws.global_indice(
                initial_samples=initial_samples,
                batch_ratio=batch_ratio,
                error_tolerance_percentage=error_tolerance,
                method=method,
                axes=axes,
                max_samples=50000,
                is_normalized=is_normalized,  # Use the slider value here
            )
            ws.plot(color=method, fig=fig, isShow=False)

            # Get reach for all axes
            reach = ws.reach(axes="all")
            reach_x = reach[0]
            reach_y = reach[1]
            reach_z = reach[2]
            text_reach_x = f"[{reach_x[0]:.3f}, {reach_x[1]:.3f}]"
            text_reach_y = f"[{reach_y[0]:.3f}, {reach_y[1]:.3f}]"
            text_reach_z = f"[{reach_z[0]:.3f}, {reach_z[1]:.3f}]"

            fig.update_layout(showlegend=False)

            # Create detailed message with all settings
            axes_desc = (
                "all axes (translation + rotation)"
                if axes == "all"
                else "translation axes only"
            )
            message = (
                f"Performed workspace analysis for {robot_name} using:\n"
                f"• Method: {method}\n"
                f"• Axes: {axes_desc}\n"
                f"• Initial samples: {initial_samples}\n"
                f"• Batch ratio: {batch_ratio}\n"
                f"• Error tolerance: {error_tolerance}\n"
                f"• Normalization: {is_normalized}"
            )

            # Create updated table with both length and global manipulability
            results_table = dbc.Table(
                [
                    html.Thead(html.Tr([html.Th("Metric"), html.Th("Value")])),
                    html.Tbody(
                        [
                            html.Tr(
                                [
                                    html.Td("Total Arm Length [m]"),
                                    html.Td(text_length),
                                ]
                            ),
                            html.Tr(
                                [
                                    html.Td("x Reach [m]"),
                                    html.Td(text_reach_x),
                                ]
                            ),
                            html.Tr(
                                [
                                    html.Td("y Reach [m]"),
                                    html.Td(text_reach_y),
                                ]
                            ),
                            html.Tr(
                                [
                                    html.Td("z Reach [m]"),
                                    html.Td(text_reach_z),
                                ]
                            ),
                            html.Tr(
                                [
                                    html.Td("Global Manipulability (G)"),
                                    html.Td(f"{G:.6f}"),
                                ]
                            ),
                            html.Tr([html.Td("Method"), html.Td(f"{method}")]),
                            html.Tr([html.Td("Axes"), html.Td(f"{axes_desc}")]),
                            html.Tr(
                                [html.Td("Normalization"), html.Td(f"{is_normalized}")]
                            ),
                        ]
                    ),
                ],
                bordered=True,
                hover=True,
                striped=True,
                size="sm",
            )

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
        return fig, f"Error: {e}", results_table

    return fig, message, results_table


def run_dash():
    app.run(debug=True, use_reloader=False)


def create_window():
    webview.create_window(
        "Plotly Dash App", "http://127.0.0.1:8050/", width=800, height=600
    )
    webview.start()


if __name__ == "__main__":
    try:
        run_dash_thread = Thread(target=run_dash, daemon=True)
        run_dash_thread.start()

        # Give some time for the server to start
        import time

        time.sleep(1)  # Adjust based on how long the server takes to start
        create_window()
    except Exception as e:
        print(f"An error occurred: {e}")
