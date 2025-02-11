import robosandbox as rsb
import robosandbox.geometry.Link.CylinderLink as cl
import numpy as np

def test_CylinderLink():
    cylinder_link = rsb.geometry.Link.CylinderLink(length=0.4, E=70e6, rho=2700, Rout=25e-3, parameters=[25e-3, 2e-3], method='linear')
    print(f"Link Length: {cylinder_link.len} m")
    print(np.round(cylinder_link.I_tensor, 5))
    print(f"Center of mass: {np.round(cylinder_link.get_center_of_mass(), 4)}")
    print(f"Mass: {cylinder_link.mass} kg")
def test_CylinderLink_plot():
    cylinder_link = cl(length=0.4, E=70e6, rho=2700, Rout=25e-3, parameters=[25e-3, 2e-3], method='linear')
    cylinder_link.plot_discretized_points()

if __name__ == "__main__":
    test_CylinderLink_plot()
