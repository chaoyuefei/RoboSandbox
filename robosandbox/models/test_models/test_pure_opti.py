import aerosandbox.numpy as np
import casadi as ca
from scipy.linalg import expm
import aerosandbox as asb

from robosandbox.models.MR.utils import so3ToVec


def is_casadi_type(obj):
    """Checks if the object is of a CasADi type."""
    return isinstance(obj, (ca.MX, ca.DM))


def NearZero(val):
    """Checks if a value is near zero."""

    if is_casadi_type(val):
        return ca.fabs(val) < 1e-6
    else:
        return np.abs(val) < 1e-6


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


def VecTose3(V):
    """Converts a spatial velocity vector to an se(3) representation."""
    so3_mat = VecToso3(V[0:3])
    if is_casadi_type(V):
        return ca.vertcat(
            ca.horzcat(so3_mat, V[3:6]),
            ca.horzcat(0, 0, 0, 0),
        )
    else:
        return np.vstack(
            [
                np.hstack([so3_mat, V[3:6].reshape((3, 1))]),
                [0, 0, 0, 0],
            ]
        )


def VecToso3(V):
    """Converts a 3-vector to an so(3) representation."""
    if is_casadi_type(V):
        return ca.vertcat(
            ca.horzcat(0, -V[2], V[1]),
            ca.horzcat(V[2], 0, -V[0]),
            ca.horzcat(-V[1], V[0], 0),
        )
    else:
        return np.array([[0, -V[2], V[1]], [V[2], 0, -V[0]], [-V[1], V[0], 0]])


def MatrixExp6(se3mat):
    """Compute the matrix exponential of a 4x4 se(3) matrix."""
    se3mat = np.array(se3mat)
    omgtheta = so3ToVec(se3mat[0:3, 0:3])
    if isinstance(se3mat, (ca.MX, ca.SX)):
        pure_translation = ca.norm_fro(omgtheta) < 1e-6
        return ca.if_else(
            pure_translation,
            ca.vertcat(ca.horzcat(ca.MX.eye(3), se3mat[0:3, 3]), ca.MX([[0, 0, 0, 1]])),
            lambda: (
                ca.vertcat(
                    ca.horzcat(
                        MatrixExp3(se3mat[0:3, 0:3]),
                        (
                            (
                                ca.MX.eye(3) * ca.norm_2(omgtheta)
                                + (1 - ca.cos(ca.norm_2(omgtheta)))
                                * (se3mat[0:3, 0:3] / ca.norm_2(omgtheta))
                                + (ca.norm_2(omgtheta) - ca.sin(ca.norm_2(omgtheta)))
                                * (
                                    (se3mat[0:3, 0:3] / ca.norm_2(omgtheta))
                                    @ (se3mat[0:3, 0:3] / ca.norm_2(omgtheta))
                                )
                            )
                            @ se3mat[0:3, 3]
                            / ca.norm_2(omgtheta)
                        ),
                    ),
                    ca.MX([[0, 0, 0, 1]]),
                )
            ),
        )

    # Worked but not sure if it is correct
    # if isinstance(se3mat, (ca.MX, ca.SX)):
    #     omgmat = se3mat[0:3, 0:3]
    #     pure_translation = ca.fabs(ca.norm_fro(omgmat)) < 1e-6

    #     theta = ca.norm_fro(omgmat)
    #     omgmat_normalized = omgmat / theta
    #     exp_omgmat = (
    #         ca.MX.eye(3)
    #         + ca.sin(theta) * omgmat_normalized
    #         + (1 - ca.cos(theta)) * ca.mtimes(omgmat_normalized, omgmat_normalized)
    #     )
    #     v = ca.reshape(se3mat[0:3, 3], (3, 1)) / theta  # Ensure v is 3x1
    #     exp_v = ca.mtimes((ca.MX.eye(3) - exp_omgmat), v) + ca.mtimes(
    #         omgmat_normalized, v
    #     )

    #     result_translation = ca.vertcat(
    #         ca.horzcat(ca.MX.eye(3), se3mat[0:3, 3]),
    #         ca.horzcat(ca.MX.zeros(1, 3), ca.MX(1)),
    #     )

    #     result_rotation = ca.vertcat(
    #         ca.horzcat(exp_omgmat, exp_v),
    #         ca.horzcat(ca.MX.zeros(1, 3), ca.MX(1)),
    #     )

    #     return ca.if_else(pure_translation, result_translation, result_rotation)
    # else:
    #     return expm(se3mat)


def MatrixExp3(so3mat):
    """Computes the matrix exponential of an so3 matrix."""
    omgvec = so3ToVec(so3mat)
    theta = ca.norm_2(omgvec)
    return ca.if_else(
        NearZero(theta),
        ca.MX.eye(3),
        ca.MX.eye(3)
        + ca.sin(theta) * (so3mat / theta)
        + (1 - ca.cos(theta)) * ((so3mat / theta) @ (so3mat / theta)),
    )


def FKinSpace(M, Slist, thetalist):
    """Computes forward kinematics in the space frame for an open chain robot."""
    T = M
    num_joints = thetalist.shape[0]  # Works for both NumPy and CasADi
    for i in range(num_joints - 1, -1, -1):
        T = MatrixExp6(VecTose3(Slist[:, i] * thetalist[i])) @ T
    return T


# Example Usage
if __name__ == "__main__":
    # NumPy Example
    M_np = np.array([[-1, 0, 0, 0], [0, 1, 0, 6], [0, 0, -1, 2], [0, 0, 0, 1]])
    Slist_np = np.array(
        [[0, 0, 1, 4, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, -1, -6, 0, -0.1]]
    ).T
    thetalist_np = np.array([np.pi / 2.0, 3, np.pi])
    result_np = FKinSpace(M_np, Slist_np, thetalist_np)
    print("NumPy Result:")
    print(result_np)

    # CasADi Example
    M_ca = ca.vertcat(
        ca.horzcat(0, 0, -1, 0),
        ca.horzcat(-1, 0, 0, 0),
        ca.horzcat(0, 1, 0, 1.6),
        ca.horzcat(0, 0, 0, 1),
    )

    j1 = ScrewToAxis(q=ca.vertcat(0, 0, 0), s=ca.vertcat(0, 0, 1), h=0)
    j2 = ScrewToAxis(q=ca.vertcat(0, 0, 0.4), s=ca.vertcat(0, 1, 0), h=0)
    j3 = ScrewToAxis(q=ca.vertcat(0, 0, 0.4 + 0.4), s=ca.vertcat(0, 1, 0), h=0)
    j4 = ScrewToAxis(q=ca.vertcat(0, 0, 0.4 + 0.4 + 0.4), s=ca.vertcat(0, 1, 0), h=0)

    Slist_ca = ca.horzcat(j1, j2, j3, j4)

    opti = asb.Opti()
    q4 = opti.variable(init_guess=0.1, lower_bound=0, upper_bound=np.pi / 2)
    q3 = opti.variable(init_guess=0.01, lower_bound=0, upper_bound=np.pi / 2)
    thetalist_ca = np.array([0, 0, q3, q4])
    # result_ca = np.power(FKinSpace(M_ca, Slist_ca, thetalist_ca)[2, -1] - 1.6, 2)
    result_ca = -FKinSpace(M_ca, Slist_ca, thetalist_ca)[2, -1]

    print(result_ca.shape)
    opti.minimize(result_ca)
    sol = opti.solve()

    print("+++++++++++++++++++++++=")
    q3_opt = sol.value(q3)
    q4_opt = sol.value(q4)
    re_opt = sol.value(result_ca)
    print(f"q3_opt: {q3_opt}")
    print(f"q4_opt: {q4_opt}")
    print(f"result: {re_opt}")

    print("CasADi Result:")
    print(FKinSpace(M_ca, Slist_ca, np.array([0, 0, q3_opt, q4_opt])))
    print("+++++++++++++++++++++++=")
    print(
        np.power(
            FKinSpace(M_ca, Slist_ca, np.array([0, 0, q3_opt, q4_opt]))[2, -1] - 1.6, 2
        )
    )
