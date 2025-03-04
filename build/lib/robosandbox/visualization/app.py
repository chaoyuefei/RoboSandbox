import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import robosandbox as rsb
import numpy as np

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Robot Arm Design App"),
                        # Key Parameters 区域
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
                                html.Div(
                                    id="dofs_display", style={"margin": "10px 0"}
                                ),  # 显示当前的 DOFs 值
                                html.P(
                                    "Link Lengths [m](comma-separated, e.g., 1, 1.5, 2):"
                                ),
                                dcc.Input(
                                    id="link_lengths",
                                    value="0.4, 0.4, 0.4, 0.4",
                                    type="text",
                                ),
                                html.P(
                                    "Alpha Angles [deg](comma-separated, e.g., 0, 30, 45):"
                                ),
                                dcc.Input(id="alpha", value="90, 0, 0, 0", type="text"),
                                html.P("qs [deg](comma-separated, e.g., 0, 30, 45):"),
                                dcc.Input(id="qs", value="90, 0, 0, 0", type="text"),
                            ]
                        ),
                        html.Div(style={"height": "20px"}),
                        # Command 区域
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
                    width=4,  # 左侧列占据4个网格
                ),
                dbc.Col(
                    [
                        html.H5("Robot Arm Configuration"),
                        dbc.Spinner(
                            dcc.Graph(id="arm_display", style={"height": "80vh"}),
                            color="primary",
                        ),
                        html.Div(id="output", style={"margin-top": "20px"}),
                    ],
                    width=8,  # 右侧列占据8个网格
                ),
            ]
        ),
    ],
    fluid=True,
)


@app.callback(Output("dofs_display", "children"), Input("dofs_slider", "value"))
def update_dofs_display(selected_dofs):
    return f"Selected DOFs: {selected_dofs}"


@app.callback(
    Output("arm_display", "figure"),
    Output("output", "children"),
    Input("generate_button", "n_clicks"),
    Input("dofs_slider", "value"),
    Input("link_lengths", "value"),
    Input("alpha", "value"),
    Input("qs", "value"),
)
def update_robot_arm(n_clicks, dofs, link_lengths, alpha, qs):
    if n_clicks is None:
        return {}, "Please click the button to generate the robot arm"

    # 解析用户输入的连杆长度和攻角
    try:
        link_lengths = list(map(float, link_lengths.split(",")))
        alpha = list(map(float, alpha.split(",")))
        qs = list(map(float, qs.split(",")))
    except ValueError:
        return {}, "Please enter valid numbers for link lengths and alpha angles."

    # 根据 DOFs 绘制不同数量的圆
    fig = go.Figure()

    if dofs == 2:
        # 绘制两个圆
        for i in range(2):
            fig.add_shape(
                type="circle",
                xref="x",
                yref="y",
                x0=i,
                y0=0,
                x1=i + 1,
                y1=1,
                fillcolor="skyblue",
                line_color="blue",
            )
    elif dofs == 3:
        robot = rsb.models.DH.Generic.GenericThree(
            linklengths=link_lengths, alpha=[np.deg2rad(a) for a in alpha]
        )
        robot.plotly(np.deg2rad(qs), isShow=False, fig=fig)

    elif dofs == 4:
        robot = rsb.models.DH.Generic.GenericFour(
            linklengths=link_lengths, alpha=[np.deg2rad(a) for a in alpha]
        )
        # robot.plotly(robot.qz, isShow=False, fig=fig)
        robot.plotly(np.deg2rad(qs), isShow=False, fig=fig)

    # 设置图形布局
    fig.update_layout(
        title=f"Robot Arm with {dofs} DOFs",
        xaxis=dict(title="X", range=[-1, 4]),
        yaxis=dict(title="Y", range=[-1, 2]),
        showlegend=False,
    )

    output_text = f"Generated a robotic arm with {dofs} DOFs, link lengths: {link_lengths}, alpha angles: {alpha}"
    return fig, output_text


if __name__ == "__main__":
    app.run(debug=True)
