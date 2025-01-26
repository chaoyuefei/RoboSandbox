import aerosandbox.numpy as np
import casadi as ca
import aerosandbox as asb


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
    """Computes the matrix exponential of an se3 representation of
    exponential coordinates

    :param se3mat: A matrix in se3
    :return: The matrix exponential of se3mat

    Example Input:
        se3mat = np.array([[0,          0,           0,          0],
                           [0,          0, -1.57079632, 2.35619449],
                           [0, 1.57079632,           0, 2.35619449],
                           [0,          0,           0,          0]])
    Output:
        np.array([[1.0, 0.0,  0.0, 0.0],
                  [0.0, 0.0, -1.0, 0.0],
                  [0.0, 1.0,  0.0, 3.0],
                  [  0,   0,    0,   1]])
    """
    se3mat = np.array(se3mat)
    omgtheta = so3ToVec(se3mat[0:3, 0:3])
    if is_casadi_type(se3mat):
        res = ca.if_else(
            NearZero(np.linalg.norm(omgtheta)),
            ca.vertcat(
                ca.horzcat(ca.MX.eye(3), se3mat[0:3, 3].reshape((3, 1))),
                ca.horzcat(ca.MX.zeros(1, 3), ca.MX(1)),
            ),
            ca.vertcat(
                ca.horzcat(
                    MatrixExp3(se3mat[0:3, 0:3]),
                    (
                        ca.mtimes(
                            (ca.MX.eye(3) - MatrixExp3(se3mat[0:3, 0:3])),
                            se3mat[0:3, 3].reshape((3, 1)),
                        )
                        / np.linalg.norm(omgtheta)
                    ),
                ),
                ca.horzcat(ca.MX.zeros(1, 3), ca.MX(1)),
            ),
        )
        return res
    else:
        if NearZero(np.linalg.norm(omgtheta)):
            return np.concatenate(
                [
                    np.concatenate([np.eye(3), se3mat[0:3, 3].reshape((3, 1))], axis=1),
                    [[0, 0, 0, 1]],
                ],
                axis=0,
            )
        else:
            theta = AxisAng3(omgtheta)[1]
            omgmat = se3mat[0:3, 0:3] / theta
            t1 = MatrixExp3(se3mat[0:3, 0:3])
            t2 = np.dot(
                np.eye(3) * theta
                + (1 - np.cos(theta)) * omgmat
                + (theta - np.sin(theta)) * np.dot(omgmat, omgmat),
                se3mat[0:3, 3],
            ).reshape((3, 1))
            return np.concatenate(
                [
                    np.concatenate(
                        [
                            MatrixExp3(se3mat[0:3, 0:3]),
                            t2 / theta,
                        ],
                        axis=1,
                    ),
                    [[0, 0, 0, 1]],
                ],
                axis=0,
            )


def MatrixExp3(so3mat):
    """Computes the matrix exponential of a matrix in so(3)

    :param so3mat: A 3x3 skew-symmetric matrix
    :return: The matrix exponential of so3mat

    Example Input:
        so3mat = np.array([[ 0, -3,  2],
                           [ 3,  0, -1],
                           [-2,  1,  0]])
    Output:
        np.array([[-0.69492056,  0.71352099,  0.08929286],
                  [-0.19200697, -0.30378504,  0.93319235],
                  [ 0.69297817,  0.6313497 ,  0.34810748]])
    """
    omgtheta = so3ToVec(so3mat)
    # print(omgtheta)
    if is_casadi_type(omgtheta):
        theta = AxisAng3(omgtheta)[1]
        omgmat = so3mat / theta
        res = ca.if_else(
            NearZero(np.linalg.norm(omgtheta)),
            np.eye(3),
            np.eye(3)
            + np.sin(theta) * omgmat
            + (1 - np.cos(theta)) * np.dot(omgmat, omgmat),
        )
        return res
    else:
        if NearZero(np.linalg.norm(omgtheta)):
            return np.eye(3)
        else:
            theta = AxisAng3(omgtheta)[1]
            omgmat = so3mat / theta
            return (
                np.eye(3)
                + np.sin(theta) * omgmat
                + (1 - np.cos(theta)) * np.dot(omgmat, omgmat)
            )


def so3ToVec(so3mat):
    """Converts an so(3) representation to a 3-vector

    :param so3mat: A 3x3 skew-symmetric matrix
    :return: The 3-vector corresponding to so3mat

    Example Input:
        so3mat = np.array([[ 0, -3,  2],
                           [ 3,  0, -1],
                           [-2,  1,  0]])
    Output:
        np.array([1, 2, 3])
    """
    if is_casadi_type(so3mat):
        return ca.vertcat(so3mat[2, 1], so3mat[0, 2], so3mat[1, 0])
    return np.array([so3mat[2][1], so3mat[0][2], so3mat[1][0]])


def AxisAng3(expc3):
    """Converts a 3-vector of exponential coordinates for rotation into
    axis-angle form

    :param expc3: A 3-vector of exponential coordinates for rotation
    :return omghat: A unit rotation axis
    :return theta: The corresponding rotation angle

    Example Input:
        expc3 = np.array([1, 2, 3])
    Output:
        (np.array([0.26726124, 0.53452248, 0.80178373]), 3.7416573867739413)
    """
    return (Normalize(expc3), np.linalg.norm(expc3))


def Normalize(V):
    """Normalizes a vector

    :param V: A vector
    :return: A unit vector pointing in the same direction as z

    Example Input:
        V = np.array([1, 2, 3])
    Output:
        np.array([0.26726124, 0.53452248, 0.80178373])
    """
    return V / np.linalg.norm(V)


def FKinSpace(M, Slist, thetalist):
    """Computes forward kinematics in the space frame for an open chain robot."""
    T = M
    num_joints = thetalist.shape[0]  # Works for both NumPy and CasADi
    for i in range(num_joints - 1, -1, -1):
        T = MatrixExp6(VecTose3(Slist[:, i] * thetalist[i])) @ T
    return T


# Example Usage
if __name__ == "__main__":
    # # NumPy Example
    # M_np = np.array([[-1, 0, 0, 0], [0, 1, 0, 6], [0, 0, -1, 2], [0, 0, 0, 1]])
    # Slist_np = np.array(
    #     [[0, 0, 1, 4, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, -1, -6, 0, -0.1]]
    # ).T
    # thetalist_np = np.array([np.pi / 2.0, 3, np.pi])
    # result_np = FKinSpace(M_np, Slist_np, thetalist_np)
    # print("NumPy Result:")
    # print(result_np)

    # # CasADi Example
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
    q3 = opti.variable(init_guess=0.1, lower_bound=0, upper_bound=np.pi / 2)
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

    print(FKinSpace(M_ca, Slist_ca, np.array([0, 0, q3_opt, q4_opt])))
