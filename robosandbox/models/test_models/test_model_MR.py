
import robosandbox as rsb
import aerosandbox.numpy as np
import aerosandbox as asb


def test_MR_GenericFour():
    robot = rsb.models.MR.Generic.GenericFour()
    theta_list = np.array([0, 0.2, 0, 0.2])
    opti = asb.Opti()

    q1 = opti.variable(init_guess=0.2)
    q2 = opti.variable(init_guess=0.2)
    q3 = opti.variable(init_guess=0.2)
    q4 = opti.variable(init_guess=0.2)

    theta_list = np.array([q1, q2, q3, q4])

    f = robot.fkine(theta_list)

    opti.minimize(-f)
    sol = opti.solve()
    print(sol)

if __name__ == "__main__":
    test_MR_GenericFour()
