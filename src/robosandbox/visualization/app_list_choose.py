import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Robot Arm Design App"),
                        html.H5("Create your robotic arm configuration"),
                        html.Div(
                            [
                                html.H5("Key Parameters"),
                                html.P("Degrees of Freedom (DOFs):"),
                                dcc.Dropdown(
                                    id="dofs_dropdown",
                                    options=[
                                        {"label": "2 DOFs", "value": 2},
                                        {"label": "3 DOFs", "value": 3},
                                        {"label": "4 DOFs", "value": 4},
                                        {"label": "5 DOFs", "value": 5},
                                        {"label": "6 DOFs", "value": 6},
                                        {"label": "7 DOFs", "value": 7},
                                    ],
                                    value=2,  # 默认值
                                ),
                                html.P(
                                    "Link Lengths (comma-separated, e.g., 1, 1.5, 2):"
                                ),
                                dcc.Input(id="link_lengths", value="1, 1", type="text"),
                                html.P(
                                    "Alpha Angles (comma-separated, e.g., 0, 30, 45):"
                                ),
                                dcc.Input(id="alpha", value="0, 30", type="text"),
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


@app.callback(
    Output("arm_display", "figure"),
    Output("output", "children"),
    Input("generate_button", "n_clicks"),
    Input("dofs_dropdown", "value"),
    Input("link_lengths", "value"),
    Input("alpha", "value"),
)
def update_robot_arm(n_clicks, dofs, link_lengths, alpha):
    if n_clicks is None:
        return {}, "Please click the button to generate the robot arm"

    # 解析用户输入的连杆长度和攻角
    link_lengths = list(map(float, link_lengths.split(",")))
    alpha = list(map(float, alpha.split(",")))

    # 这里可以添加绘制机械臂的逻辑
    # 例如，使用 matplotlib、plotly、或者其他库绘制机器人信息
    # 模拟返回的图：
    fig = {
        "data": [
            # 示例数据；您将用实际计算的数据替代
            {"x": [0, 1, 2], "y": [0, 1, 0], "type": "lines", "name": "Robot Arm"},
        ],
        "layout": {
            "title": f"Robot Arm with {dofs} DOFs",
            "xaxis": {"title": "X", "range": [-1, 3]},
            "yaxis": {"title": "Y", "range": [-1, 2]},
        },
    }

    output_text = f"Generated a robotic arm with {dofs} DOFs, link lengths: {link_lengths}, alpha angles: {alpha}"
    return fig, output_text


if __name__ == "__main__":
    app.run(debug=True)
