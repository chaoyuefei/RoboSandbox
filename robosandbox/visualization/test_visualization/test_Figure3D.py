import robosandbox as rsb
import aerosandbox as asb
from robosandbox.visualization.plotly_Figure3D import Figure3D

def test_add_line():
    fig = Figure3D()
    fig.add_line([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0)])
    fig.draw()

def test_add_quad():
    fig = Figure3D()
    fig.add_quad(
        [
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 0),
        ],
        outline=True,
    )
    fig.draw()

def test_asb_plane():
    plane = asb.Airplane()
    plane.draw()


if __name__ == "__main__":
    # test_add_line()
    test_add_quad()
