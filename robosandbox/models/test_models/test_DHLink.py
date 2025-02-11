import robosandbox as rsb
import robosandbox.geometry.Link.CylinderLink as cl

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

if __name__ == "__main__":
    # test_DHLink()
    test_customed_DHLink()
