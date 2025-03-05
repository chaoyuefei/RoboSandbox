import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import robosandbox as rsb
import numpy as np

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

# Initialize the figure with a fixed layout
fig_init = go.Figure()
fig_init.update_layout(
    title="Robot Arm Configuration",
    scene=dict(
        xaxis=dict(title="X", range=[-2, 2]),
        yaxis=dict(title="Y", range=[-2, 2]),
        zaxis=dict(title="Z", range=[-2, 2]),
    ),
    margin=dict(l=0, r=0, b=0, t=30),
)

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
                        html.Div(
                            [
                                html.H5("Key Parameters"),
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
                                html.Div(id="dofs_display", style={"margin": "10px 0"}),
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
                                html.P("qs [deg] (comma-separated, e.g., 0,30,45):"),
                                dcc.Input(
                                    id="qs",
                                    value="90,0,0,0",
                                    type="text",
                                    style={"width": "100%"},
                                ),
                            ]
                        ),
                        html.Div(style={"height": "20px"}),
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
                            ]
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.H5("Robot Arm Configuration"),
                        dbc.Spinner(
                            dcc.Graph(
                                id="arm_display",
                                figure=fig_init,  # Set the initialized figure
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


@app.callback(
    Output("dofs_display", "children"),
    Input("dofs_slider", "value"),
)
def update_dofs_display(selected_dofs):
    return f"Selected DOFs: {selected_dofs}"


@app.callback(
    Output("arm_display", "figure"),
    Output("output", "children"),
    Input("generate_button", "n_clicks"),
    State("dofs_slider", "value"),
    State("link_lengths", "value"),
    State("alpha", "value"),
    State("qs", "value"),
)
def update_robot_arm(n_clicks, dofs, link_lengths, alpha, qs):
    if n_clicks is None:
        return dash.no_update, "Please click the 'Generate Robot Arm' button."

    try:
        link_lengths = [float(length.strip()) for length in link_lengths.split(",")]
        alpha = [float(angle.strip()) for angle in alpha.split(",")]
        qs = [float(q.strip()) for q in qs.split(",")]
    except ValueError:
        return dash.no_update, "Please enter valid numbers for link lengths and angles."

    # Initialize a new figure with the existing layout
    fig = go.Figure(fig_init)

    try:
        if dofs == 2:
            robot = rsb.models.DH.Generic.GenericTwo(
                linklengths=link_lengths, alpha=[np.deg2rad(a) for a in alpha]
            )
        elif dofs == 3:
            robot = rsb.models.DH.Generic.GenericThree(
                linklengths=link_lengths, alpha=[np.deg2rad(a) for a in alpha]
            )
        elif dofs == 4:
            robot = rsb.models.DH.Generic.GenericFour(
                linklengths=link_lengths, alpha=[np.deg2rad(a) for a in alpha]
            )
        elif dofs == 5:
            robot = rsb.models.DH.Generic.GenericFive(
                linklengths=link_lengths, alpha=[np.deg2rad(a) for a in alpha]
            )
        elif dofs == 6:
            robot = rsb.models.DH.Generic.GenericSix(
                linklengths=link_lengths, alpha=[np.deg2rad(a) for a in alpha]
            )
        elif dofs == 7:
            robot = rsb.models.DH.Generic.GenericSeven(
                linklengths=link_lengths, alpha=[np.deg2rad(a) for a in alpha]
            )
        else:
            return dash.no_update, f"DOFs of {dofs} not supported."

        # Plot the robot arm on the existing figure
        robot.plotly(np.deg2rad(qs), isShow=False, fig=fig, isUpdate=True)

    except Exception as e:
        return dash.no_update, f"Error generating robot arm: {e}"

    output_text = f"Generated a robotic arm with {dofs} DOFs."

    return fig, output_text


if __name__ == "__main__":
    app.run(debug=True)
