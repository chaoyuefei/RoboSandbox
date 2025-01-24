import robosandbox as rsb
import aerosandbox.numpy as np
import aerosandbox as asb


def test_opti():
    opti = asb.Opti()
    l1 = opti.variable(init_guess=0.2)
    l2 = opti.variable(init_guess=0.2)
    l3 = opti.variable(init_guess=0.2)
    l4 = opti.variable(init_guess=0.2)

    robot = rsb.models.MR.Generic.GenericFour(np.array([l1, l2, l3, l4]))

    theta_list = np.array([0, 0, 0, 0])

    # f = np.power(rsb.models.MR.Generic.GenericFour(np.array([l1, l2, l3, l4])).M[2, -1] - 2, 2)
    f = np.power(rsb.models.MR.Generic.GenericFour(np.array([l1, l2, l3, l4])).fkine(theta_list)[2, -1] - 2, 2)

    # opti.subject_to(l1 <= 0.3)
    # opti.subject_to(l2 <= 0.6)
    # opti.subject_to(l3 <= 0.8)
    # opti.subject_to(l4 <= 1)

    # opti.subject_to(l3 - l2 >= 0.2)

    opti.minimize(f)
    sol = opti.solve()

    l1_opt = sol(l1)
    l2_opt = sol(l2)
    l3_opt = sol(l3)
    l4_opt = sol(l4)

    print(f"l1_opt: {l1_opt}")
    print(f"l2_opt: {l2_opt}")
    print(f"l3_opt: {l3_opt}")
    print(f"l4_opt: {l4_opt}")

if __name__ == "__main__":
    test_opti()
