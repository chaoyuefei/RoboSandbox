import robosandbox as rsb
import aerosandbox.numpy as np
import aerosandbox as asb


def test_MR_GenericFour():
    robot = rsb.models.MR.Generic.GenericFour()
    # theta_list = np.array([0, 0.2, 0, 0.2])
    opti = asb.Opti()

    q1 = opti.variable(init_guess=0.1)
    q2 = opti.variable(init_guess=0.1)
    q3 = opti.variable(init_guess=0.1)
    q4 = opti.variable(init_guess=0.1)

    # opti.subject_to(q1 <= np.pi / 2)
    # opti.subject_to(q2 <= np.pi / 2)
    # opti.subject_to(q3 <= np.pi / 2)
    # opti.subject_to(q4 <= np.pi / 2)

    opti.subject_to(q1 >= 0 * -np.pi / 2)
    opti.subject_to(q2 >= 0 * -np.pi / 2)
    opti.subject_to(q3 >= 0 * -np.pi / 2)
    opti.subject_to(q4 >= 0 * -np.pi / 2)

    theta_list = np.array([q1, q2, q3, q4])

    f = robot.fkine(theta_list)[2, -1]
    print(f)
    opti.minimize(f)
    sol = opti.solve()

    print(sol)

    print("+++++++++++++++++++++++=")
    q1_opt = sol(q1)
    q2_opt = sol(q2)
    q3_opt = sol(q3)
    q4_opt = sol(q4)
    print(f"q1_opt: {q1_opt}")
    print(f"q2_opt: {q2_opt}")
    print(f"q3_opt: {q3_opt}")
    print(f"q4_opt: {q4_opt}")
    theta_list_opt = np.array([q1_opt, q2_opt, q3_opt, q4_opt])
    print(robot.fkine(theta_list_opt))
    print(robot.fkine([0, 0, 0, 0]))


if __name__ == "__main__":
    test_MR_GenericFour()
