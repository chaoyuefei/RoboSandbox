import robosandbox as rsb
import robosandbox.geometry.Link.CylinderLink as cl
import numpy as np
from robosandbox.visualization.plotly_Figure3D import Figure3D

def test_DHLink():
    GenericFourLink = rsb.models.DHLink.Generic.GenericFour()
    print(GenericFourLink.dynamics())
def test_customed_DHLink():
    l1 = cl(length=0.4, E=70e6, rho=2700, Rout=25e-3, parameters=[20e-3, 20e-3], method='linear')
    l2 = cl(length=0.3, E=70e6, rho=2700, Rout=25e-3, parameters=[21e-3, 21e-3], method='linear')
    l3 = cl(length=0.2, E=70e6, rho=2700, Rout=25e-3, parameters=[22e-3, 22e-3], method='linear')
    l4 = cl(length=0.1, E=70e6, rho=2700, Rout=25e-3, parameters=[23e-3, 23e-3], method='linear')
    links = [l1, l2, l3, l4]
    robot = rsb.models.DHLink.Generic.GenericFour(links=links)
    print(robot.dynamics())

def test_mesh_plot():
    l1 = cl(length=0.4, E=70e6, rho=2700, Rout=25e-3, parameters=[20e-3, 20e-3], method='linear')
    points, faces = l1.get_outer_mesh()
    print(len(points))
    print(points[360-1]) # first layer z = 0 last point: (0.025, -6.123233995736766e-18, 0.0)
    print(points[360]) # second layer z = 0.005 first point: (0.025, 0.0, 0.005063291139240506)
    print(len(np.linspace(0, 2*np.pi, 360)))
    print(len(faces))
    print(faces[0])
    print(faces[1])

    fig = Figure3D()
    count = 0
    for f in faces:
        count += 1
        fig.add_quad(
            (
                points[f[0]],
                points[f[1]],
                points[f[2]],
                points[f[3]],
            ),
            intensity=count, # random give int
            outline=False,
        )
    return fig.draw()

if __name__ == "__main__":
    # test_DHLink()
    # test_customed_DHLink()
    test_mesh_plot()
