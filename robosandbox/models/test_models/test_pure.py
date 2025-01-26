import aerosandbox.numpy as np
import casadi as ca
from scipy.linalg import expm


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
    if isinstance(se3mat, (ca.MX, ca.SX)):
        omgmat = se3mat[0:3, 0:3]
        if ca.norm_fro(omgmat) < 1e-6:  # Pure translation
            return ca.vertcat(
                ca.horzcat(ca.MX.eye(3), se3mat[0:3, 3]),
                ca.horzcat(ca.MX.zeros(1, 3), ca.MX(1)),
            )
        else:
            theta = ca.norm_fro(omgmat)  # Angle of rotation
            omgmat_normalized = omgmat / theta
            exp_omgmat = (
                ca.MX.eye(3)
                + ca.sin(theta) * omgmat_normalized
                + (1 - ca.cos(theta)) * ca.mtimes(omgmat_normalized, omgmat_normalized)
            )
            v = se3mat[0:3, 3] / theta
            exp_v = ca.mtimes((ca.MX.eye(3) - exp_omgmat), v) + ca.mtimes(
                v, ca.transpose(v)
            )
            return ca.vertcat(
                ca.horzcat(exp_omgmat, exp_v), ca.horzcat(ca.MX.zeros(1, 3), ca.MX(1))
            )
    else:
        return expm(se3mat)


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
        ca.horzcat(-1, 0, 0, 0),
        ca.horzcat(0, 1, 0, 6),
        ca.horzcat(0, 0, -1, 2),
        ca.horzcat(0, 0, 0, 1),
    )
    Slist_ca = ca.horzcat(
        ca.vertcat(0, 0, 1, 4, 0, 0),
        ca.vertcat(0, 0, 0, 0, 1, 0),
        ca.vertcat(0, 0, -1, -6, 0, -0.1),
    )
    thetalist_ca = ca.vertcat(ca.pi / 2.0, 3, ca.pi)
    # thetalist_ca = ca.vertcat(0, 0, 0, 2.14)

    result_ca = FKinSpace(M_ca, Slist_ca, thetalist_ca)
    print("CasADi Result:")
    print(result_ca)
