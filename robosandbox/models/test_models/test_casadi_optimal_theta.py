# import numpy as np
import casadi as ca
from scipy.linalg import expm
import aerosandbox.numpy as np
import aerosandbox as asb

def is_casadi_type(obj):
    """Checks if the object is of a CasADi type."""
    return isinstance(obj, (ca.MX, ca.DM))


def VecTose3(V):
    """Converts a spatial velocity vector to an se(3) representation."""
    so3_mat = VecToso3(V[0:3])
    if is_casadi_type(V):
        return ca.vertcat(
            ca.horzcat(so3_mat, V[3:6]),
            ca.horzcat(0, 0, 0, 0),
        )
    else:
        return np.vstack([
            np.hstack([so3_mat, V[3:6].reshape((3, 1))]),
            [0, 0, 0, 0],
        ])


def VecToso3(V):
    """Converts a 3-vector to an so(3) representation."""
    if is_casadi_type(V):
        return ca.vertcat(
            ca.horzcat(0, -V[2], V[1]),
            ca.horzcat(V[2], 0, -V[0]),
            ca.horzcat(-V[1], V[0], 0),
        )
    else:
        return np.array([
            [0, -V[2], V[1]],
            [V[2], 0, -V[0]],
            [-V[1], V[0], 0]
        ])


def MatrixExp6(se3mat):
    """Compute the matrix exponential of a 4x4 se(3) matrix."""
    if is_casadi_type(se3mat):
        omgmat = se3mat[0:3, 0:3]
        theta = ca.norm_fro(omgmat)  # Angle of rotation

        # Conditional logic for pure translation or rotation
        is_pure_translation = ca.fabs(theta) < 1e-6

        exp_omgmat = ca.if_else(
            is_pure_translation,
            ca.MX.eye(3),  # No rotation
            ca.MX.eye(3) +
            (ca.sin(theta) / theta) * omgmat +
            ((1 - ca.cos(theta)) / (theta ** 2)) * ca.mtimes(omgmat, omgmat),
        )

        v = se3mat[0:3, 3]
        exp_v = ca.if_else(
            is_pure_translation,
            v,  # Direct translation
            ca.mtimes((ca.MX.eye(3) - exp_omgmat) @ ca.inv(omgmat), v) + (1 / theta) * v
        )
        return ca.vertcat(
            ca.horzcat(exp_omgmat, exp_v),
            ca.horzcat(ca.MX.zeros(1, 3), ca.MX(1))
        )
    else:
        # NumPy version
        return expm(se3mat)

def FKinSpace(M, Slist, thetalist):
    """Computes forward kinematics in the space frame for an open chain robot."""
    T = M
    num_joints = thetalist.shape[0]  # Works for both NumPy and CasADi
    for i in range(num_joints - 1, -1, -1):
        T = MatrixExp6(VecTose3(Slist[:, i] * thetalist[i])) @ T
    return T

def ScrewToAxis(q, s, h):
    """
    Takes a parametric description of a screw axis and converts it to a
    normalized screw axis.

    :param q: A point lying on the screw axis (3-vector)
    :param s: A unit vector in the direction of the screw axis (3-vector)
    :param h: The pitch of the screw axis (scalar)
    :return: A normalized screw axis described by the inputs (6-vector)

    Example Input:
        q = np.array([3, 0, 0])
        s = np.array([0, 0, 1])
        h = 2
    Output:
        np.array([0, 0, 1, 0, -3, 2])
    """
    if is_casadi_type(q) or is_casadi_type(s) or is_casadi_type(h):
        # CasADi version
        return ca.vertcat(s, ca.cross(q, s) + h * s)
    else:
        # NumPy version
        return np.r_[s, np.cross(q, s) + h * s]


# Example Usage
if __name__ == "__main__":
    # NumPy Example
    M_np = np.array([[-1, 0,  0, 0],
                     [ 0, 1,  0, 6],
                     [ 0, 0, -1, 2],
                     [ 0, 0,  0, 1]])
    Slist_np = np.array([[0, 0,  1,  4, 0,    0],
                         [0, 0,  0,  0, 1,    0],
                         [0, 0, -1, -6, 0, -0.1]]).T
    thetalist_np = np.array([np.pi / 2.0, 3, np.pi])
    result_np = FKinSpace(M_np, Slist_np, thetalist_np)
    print("NumPy Result:")
    print(result_np)

    # CasADi Example
    M_ca = ca.vertcat(
        ca.horzcat(0, 0,  -1, 0),
        ca.horzcat(-1,  0,  0, 0),
        ca.horzcat(0,  1, 0, 1.6),
        ca.horzcat(0,  0,  0, 1)
    )
    j1 = ScrewToAxis(q=ca.vertcat(0, 0, 0), s=ca.vertcat(0, 0, 1), h=0)
    j2 = ScrewToAxis(q=ca.vertcat(0, 0, 0.4), s=ca.vertcat(0, 1, 0), h=0)
    j3 = ScrewToAxis(q=ca.vertcat(0, 0, 0.4 + 0.4), s=ca.vertcat(0, 1, 0), h=0)
    j4 = ScrewToAxis(q=ca.vertcat(0, 0, 0.4 + 0.4 + 0.4), s=ca.vertcat(0, 1, 0), h=0)

    Slist_ca = ca.horzcat(
        j1,
        j2,
        j3,
        j4
    )
    # thetalist_ca = ca.vertcat(ca.pi / 2.0, 3, ca.pi)
    # thetalist_ca = ca.vertcat(0, 0, 0, 0)
    #
    opti = asb.Opti()
    # q1 = opti.variable(init_guess=0.2)
    # q2 = opti.variable(init_guess=0.2)
    # q3 = opti.variable(init_guess=0.2)
    q4 = opti.variable(init_guess=0.5)
    theta_list = np.array([0, 0, 0, q4])
    result_ca = np.power(FKinSpace(M_ca, Slist_ca, theta_list)[2, -1] -1.6, 2)
    opti.minimize(result_ca)

    sol = opti.solve()
    print("+++++++++++++++++++++++=")
    # q1_opt = sol(q1)
    # q2_opt = sol(q2)
    # q3_opt = sol(q3)
    q4_opt = sol(q4)
    # print(f"q1_opt: {q1_opt}")
    # print(f"q2_opt: {q2_opt}")
    # print(f"q3_opt: {q3_opt}")
    print(f"q4_opt: {q4_opt}")
    print(sol(result_ca))

    # print("CasADi Result:")
    # print(result_ca)
