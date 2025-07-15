import numpy as np

"""
BASIC FUNCTIONS
"""


def NearZero(z):
    """Determines whether a scalar is small enough to be treated as zero

    :param z: A scalar input to check
    :return: True if z is close to zero, false otherwise

    Example Input:
        z = -1e-7
    Output:
        True
    """
    return abs(z) < 1e-6


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


"""
*** CHAPTER 3: RIGID-BODY MOTIONS ***
"""


def RotInv(R):
    """Inverts a rotation matrix

    :param R: A rotation matrix
    :return: The inverse of R

    Example Input:
        R = np.array([[0, 0, 1],
                        [1, 0, 0],
                        [0, 1, 0]])
    Output:
        np.array([[0, 1, 0],
                    [0, 0, 1],
                    [1, 0, 0]])
    """
    return np.array(R).T


def VecToso3(omg):
    """Converts a 3-vector to an so(3) representation

    :param omg: A 3-vector
    :return: The skew symmetric representation of omg

    Example Input:
        omg = np.array([1, 2, 3])
    Output:
        np.array([[ 0, -3,  2],
                    [ 3,  0, -1],
                    [-2,  1,  0]])
    """
    return np.array([[0, -omg[2], omg[1]], [omg[2], 0, -omg[0]], [-omg[1], omg[0], 0]])


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


def MatrixLog3(R):
    """Computes the matrix logarithm of a rotation matrix

    :param R: A 3x3 rotation matrix
    :return: The matrix logarithm of R

    Example Input:
        R = np.array([[0, 0, 1],
                        [1, 0, 0],
                        [0, 1, 0]])
    Output:
        np.array([[          0, -1.20919958,  1.20919958],
                    [ 1.20919958,           0, -1.20919958],
                    [-1.20919958,  1.20919958,           0]])
    """
    acosinput = (np.trace(R) - 1) / 2.0
    if acosinput >= 1:
        return np.zeros((3, 3))
    elif acosinput <= -1:
        if not NearZero(1 + R[2][2]):
            omg = (1.0 / np.sqrt(2 * (1 + R[2][2]))) * np.array(
                [R[0][2], R[1][2], 1 + R[2][2]]
            )
        elif not NearZero(1 + R[1][1]):
            omg = (1.0 / np.sqrt(2 * (1 + R[1][1]))) * np.array(
                [R[0][1], 1 + R[1][1], R[2][1]]
            )
        else:
            omg = (1.0 / np.sqrt(2 * (1 + R[0][0]))) * np.array(
                [1 + R[0][0], R[1][0], R[2][0]]
            )
        return VecToso3(np.pi * omg)
    else:
        theta = np.arccos(acosinput)
        return theta / 2.0 / np.sin(theta) * (R - np.array(R).T)


def RpToTrans(R, p):
    """Converts a rotation matrix and a position vector into homogeneous
    transformation matrix

    :param R: A 3x3 rotation matrix
    :param p: A 3-vector
    :return: A homogeneous transformation matrix corresponding to the inputs

    Example Input:
        R = np.array([[1, 0,  0],
                        [0, 0, -1],
                        [0, 1,  0]])
        p = np.array([1, 2, 5])
    Output:
        np.array([[1, 0,  0, 1],
                    [0, 0, -1, 2],
                    [0, 1,  0, 5],
                    [0, 0,  0, 1]])
    """
    return np.r_[np.c_[R, p], [[0, 0, 0, 1]]]


def TransToRp(T):
    """Converts a homogeneous transformation matrix into a rotation matrix
    and position vector

    :param T: A homogeneous transformation matrix
    :return R: The corresponding rotation matrix,
    :return p: The corresponding position vector.

    Example Input:
        T = np.array([[1, 0,  0, 0],
                        [0, 0, -1, 0],
                        [0, 1,  0, 3],
                        [0, 0,  0, 1]])
    Output:
        (np.array([[1, 0,  0],
                    [0, 0, -1],
                    [0, 1,  0]]),
            np.array([0, 0, 3]))
    """
    T = np.array(T)
    return T[0:3, 0:3], T[0:3, 3]


def TransInv(T):
    """Inverts a homogeneous transformation matrix

    :param T: A homogeneous transformation matrix
    :return: The inverse of T
    Uses the structure of transformation matrices to avoid taking a matrix
    inverse, for efficiency.

    Example input:
        T = np.array([[1, 0,  0, 0],
                        [0, 0, -1, 0],
                        [0, 1,  0, 3],
                        [0, 0,  0, 1]])
    Output:
        np.array([[1,  0, 0,  0],
                    [0,  0, 1, -3],
                    [0, -1, 0,  0],
                    [0,  0, 0,  1]])
    """
    R, p = TransToRp(T)
    Rt = np.array(R).T
    return np.r_[np.c_[Rt, -np.dot(Rt, p)], [[0, 0, 0, 1]]]


def VecTose3(V):
    """Converts a spatial velocity vector into a 4x4 matrix in se3

    :param V: A 6-vector representing a spatial velocity
    :return: The 4x4 se3 representation of V

    Example Input:
        V = np.array([1, 2, 3, 4, 5, 6])
    Output:
        np.array([[ 0, -3,  2, 4],
                    [ 3,  0, -1, 5],
                    [-2,  1,  0, 6],
                    [ 0,  0,  0, 0]])
    """
    return np.r_[
        np.c_[VecToso3([V[0], V[1], V[2]]), [V[3], V[4], V[5]]], np.zeros((1, 4))
    ]


def se3ToVec(se3mat):
    """Converts an se3 matrix into a spatial velocity vector

    :param se3mat: A 4x4 matrix in se3
    :return: The spatial velocity 6-vector corresponding to se3mat

    Example Input:
        se3mat = np.array([[ 0, -3,  2, 4],
                            [ 3,  0, -1, 5],
                            [-2,  1,  0, 6],
                            [ 0,  0,  0, 0]])
    Output:
        np.array([1, 2, 3, 4, 5, 6])
    """
    return np.r_[
        [se3mat[2][1], se3mat[0][2], se3mat[1][0]],
        [se3mat[0][3], se3mat[1][3], se3mat[2][3]],
    ]


def Adjoint(T):
    """Computes the adjoint representation of a homogeneous transformation
    matrix

    :param T: A homogeneous transformation matrix
    :return: The 6x6 adjoint representation [AdT] of T

    Example Input:
        T = np.array([[1, 0,  0, 0],
                        [0, 0, -1, 0],
                        [0, 1,  0, 3],
                        [0, 0,  0, 1]])
    Output:
        np.array([[1, 0,  0, 0, 0,  0],
                    [0, 0, -1, 0, 0,  0],
                    [0, 1,  0, 0, 0,  0],
                    [0, 0,  3, 1, 0,  0],
                    [3, 0,  0, 0, 0, -1],
                    [0, 0,  0, 0, 1,  0]])
    """
    R, p = TransToRp(T)
    return np.r_[np.c_[R, np.zeros((3, 3))], np.c_[np.dot(VecToso3(p), R), R]]


def ScrewToAxis(q, s, h):
    """Takes a parametric description of a screw axis and converts it to a
    normalized screw axis

    :param q: A point lying on the screw axis
    :param s: A unit vector in the direction of the screw axis
    :param h: The pitch of the screw axis
    :return: A normalized screw axis described by the inputs

    Example Input:
        q = np.array([3, 0, 0])
        s = np.array([0, 0, 1])
        h = 2
    Output:
        np.array([0, 0, 1, 0, -3, 2])
    """
    # return np.r_[s, np.cross(q, s) + np.dot(h, s)]
    return np.concatenate([s, np.cross(q, s) + h * s], axis=0)


def AxisAng6(expc6):
    """Converts a 6-vector of exponential coordinates into screw axis-angle
    form

    :param expc6: A 6-vector of exponential coordinates for rigid-body motion
                    S*theta
    :return S: The corresponding normalized screw axis
    :return theta: The distance traveled along/about S

    Example Input:
        expc6 = np.array([1, 0, 0, 1, 2, 3])
    Output:
        (np.array([1.0, 0.0, 0.0, 1.0, 2.0, 3.0]), 1.0)
    """
    theta = np.linalg.norm([expc6[0], expc6[1], expc6[2]])
    if NearZero(theta):
        theta = np.linalg.norm([expc6[3], expc6[4], expc6[5]])
    return (np.array(expc6 / theta), theta)


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
    if NearZero(np.linalg.norm(omgtheta)):
        return np.r_[np.c_[np.eye(3), se3mat[0:3, 3]], [[0, 0, 0, 1]]]
    else:
        theta = AxisAng3(omgtheta)[1]
        omgmat = se3mat[0:3, 0:3] / theta
        return np.r_[
            np.c_[
                MatrixExp3(se3mat[0:3, 0:3]),
                np.dot(
                    np.eye(3) * theta
                    + (1 - np.cos(theta)) * omgmat
                    + (theta - np.sin(theta)) * np.dot(omgmat, omgmat),
                    se3mat[0:3, 3],
                )
                / theta,
            ],
            [[0, 0, 0, 1]],
        ]


def MatrixLog6(T):
    """Computes the matrix logarithm of a homogeneous transformation matrix

    :param R: A matrix in SE3
    :return: The matrix logarithm of R

    Example Input:
        T = np.array([[1, 0,  0, 0],
                        [0, 0, -1, 0],
                        [0, 1,  0, 3],
                        [0, 0,  0, 1]])
    Output:
        np.array([[0,          0,           0,           0]
                    [0,          0, -1.57079633,  2.35619449]
                    [0, 1.57079633,           0,  2.35619449]
                    [0,          0,           0,           0]])
    """
    R, p = TransToRp(T)
    omgmat = MatrixLog3(R)
    if np.array_equal(omgmat, np.zeros((3, 3))):
        return np.r_[
            np.c_[np.zeros((3, 3)), [T[0][3], T[1][3], T[2][3]]], [[0, 0, 0, 0]]
        ]
    else:
        theta = np.arccos((np.trace(R) - 1) / 2.0)
        return np.r_[
            np.c_[
                omgmat,
                np.dot(
                    np.eye(3)
                    - omgmat / 2.0
                    + (1.0 / theta - 1.0 / np.tan(theta / 2.0) / 2)
                    * np.dot(omgmat, omgmat)
                    / theta,
                    [T[0][3], T[1][3], T[2][3]],
                ),
            ],
            [[0, 0, 0, 0]],
        ]


def ProjectToSO3(mat):
    """Returns a projection of mat into SO(3)

    :param mat: A matrix near SO(3) to project to SO(3)
    :return: The closest matrix to R that is in SO(3)
    Projects a matrix mat to the closest matrix in SO(3) using singular-value
    decomposition (see
    http://hades.mech.northwestern.edu/index.php/Modern_Robotics_Linear_Algebra_Review).
    This function is only appropriate for matrices close to SO(3).

    Example Input:
        mat = np.array([[ 0.675,  0.150,  0.720],
                        [ 0.370,  0.771, -0.511],
                        [-0.630,  0.619,  0.472]])
    Output:
        np.array([[ 0.67901136,  0.14894516,  0.71885945],
                    [ 0.37320708,  0.77319584, -0.51272279],
                    [-0.63218672,  0.61642804,  0.46942137]])
    """
    U, s, Vh = np.linalg.svd(mat)
    R = np.dot(U, Vh)
    if np.linalg.det(R) < 0:
        # In this case the result may be far from mat.
        R[:, 2] = -R[:, 2]
    return R


def ProjectToSE3(mat):
    """Returns a projection of mat into SE(3)

    :param mat: A 4x4 matrix to project to SE(3)
    :return: The closest matrix to T that is in SE(3)
    Projects a matrix mat to the closest matrix in SE(3) using singular-value
    decomposition (see
    http://hades.mech.northwestern.edu/index.php/Modern_Robotics_Linear_Algebra_Review).
    This function is only appropriate for matrices close to SE(3).

    Example Input:
        mat = np.array([[ 0.675,  0.150,  0.720,  1.2],
                        [ 0.370,  0.771, -0.511,  5.4],
                        [-0.630,  0.619,  0.472,  3.6],
                        [ 0.003,  0.002,  0.010,  0.9]])
    Output:
        np.array([[ 0.67901136,  0.14894516,  0.71885945,  1.2 ],
                    [ 0.37320708,  0.77319584, -0.51272279,  5.4 ],
                    [-0.63218672,  0.61642804,  0.46942137,  3.6 ],
                    [ 0.        ,  0.        ,  0.        ,  1.  ]])
    """
    mat = np.array(mat)
    return RpToTrans(ProjectToSO3(mat[:3, :3]), mat[:3, 3])


def DistanceToSO3(mat):
    """Returns the Frobenius norm to describe the distance of mat from the
    SO(3) manifold

    :param mat: A 3x3 matrix
    :return: A quantity describing the distance of mat from the SO(3)
                manifold
    Computes the distance from mat to the SO(3) manifold using the following
    method:
    If det(mat) <= 0, return a large number.
    If det(mat) > 0, return norm(mat^T.mat - I).

    Example Input:
        mat = np.array([[ 1.0,  0.0,   0.0 ],
                        [ 0.0,  0.1,  -0.95],
                        [ 0.0,  1.0,   0.1 ]])
    Output:
        0.08835
    """
    if np.linalg.det(mat) > 0:
        return np.linalg.norm(np.dot(np.array(mat).T, mat) - np.eye(3))
    else:
        return 1e9


def DistanceToSE3(mat):
    """Returns the Frobenius norm to describe the distance of mat from the
    SE(3) manifold

    :param mat: A 4x4 matrix
    :return: A quantity describing the distance of mat from the SE(3)
                manifold
    Computes the distance from mat to the SE(3) manifold using the following
    method:
    Compute the determinant of matR, the top 3x3 submatrix of mat.
    If det(matR) <= 0, return a large number.
    If det(matR) > 0, replace the top 3x3 submatrix of mat with matR^T.matR,
    and set the first three entries of the fourth column of mat to zero. Then
    return norm(mat - I).

    Example Input:
        mat = np.array([[ 1.0,  0.0,   0.0,   1.2 ],
                        [ 0.0,  0.1,  -0.95,  1.5 ],
                        [ 0.0,  1.0,   0.1,  -0.9 ],
                        [ 0.0,  0.0,   0.1,   0.98 ]])
    Output:
        0.134931
    """
    matR = np.array(mat)[0:3, 0:3]
    if np.linalg.det(matR) > 0:
        return np.linalg.norm(
            np.r_[
                np.c_[np.dot(np.transpose(matR), matR), np.zeros((3, 1))],
                [np.array(mat)[3, :]],
            ]
            - np.eye(4)
        )
    else:
        return 1e9


def TestIfSO3(mat):
    """Returns true if mat is close to or on the manifold SO(3)

    :param mat: A 3x3 matrix
    :return: True if mat is very close to or in SO(3), false otherwise
    Computes the distance d from mat to the SO(3) manifold using the
    following method:
    If det(mat) <= 0, d = a large number.
    If det(mat) > 0, d = norm(mat^T.mat - I).
    If d is close to zero, return true. Otherwise, return false.

    Example Input:
        mat = np.array([[1.0, 0.0,  0.0 ],
                        [0.0, 0.1, -0.95],
                        [0.0, 1.0,  0.1 ]])
    Output:
        False
    """
    return abs(DistanceToSO3(mat)) < 1e-3


def TestIfSE3(mat):
    """Returns true if mat is close to or on the manifold SE(3)

    :param mat: A 4x4 matrix
    :return: True if mat is very close to or in SE(3), false otherwise
    Computes the distance d from mat to the SE(3) manifold using the
    following method:
    Compute the determinant of the top 3x3 submatrix of mat.
    If det(mat) <= 0, d = a large number.
    If det(mat) > 0, replace the top 3x3 submatrix of mat with mat^T.mat, and
    set the first three entries of the fourth column of mat to zero.
    Then d = norm(T - I).
    If d is close to zero, return true. Otherwise, return false.

    Example Input:
        mat = np.array([[1.0, 0.0,   0.0,  1.2],
                        [0.0, 0.1, -0.95,  1.5],
                        [0.0, 1.0,   0.1, -0.9],
                        [0.0, 0.0,   0.1, 0.98]])
    Output:
        False
    """
    return abs(DistanceToSE3(mat)) < 1e-3


def rotation_matrix_from_vector(vector):
    """
    Create a rotation matrix from a vector.

    # Example usage
            vector = (1, 1, 1)
            rotation_matrix = rotation_matrix_from_vector(vector)
            print(rotation_matrix)
    """

    # Normalize the input vector
    vector = np.array(vector)
    norm = np.linalg.norm(vector)

    if norm == 0:
        raise ValueError("The vector cannot be the zero vector.")

    unit_vector = vector / norm

    # World frame's Z-axis
    z_axis = np.array([0, 0, 1])

    # Compute the angle between the z-axis and the unit vector
    cos_theta = np.dot(z_axis, unit_vector)
    angle = np.arccos(cos_theta)

    # If the angle is zero or 180 degrees, return identity or reflection matrix
    if np.isclose(angle, 0):
        return np.eye(3)
    elif np.isclose(angle, np.pi):
        # 180 degree rotation around any axis perpendicular to the direction
        # Here we'll use the x-axis or y-axis (we can choose any)
        if unit_vector[0] != 0 or unit_vector[1] != 0:
            rotation_axis = np.cross(z_axis, unit_vector)
        else:
            rotation_axis = np.array([1, 0, 0])  # arbitrary in this case

        rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
        return create_rotation_matrix(rotation_axis, np.pi)

    # Find the axis of rotation using cross product
    rotation_axis = np.cross(z_axis, unit_vector)

    # Normalize the rotation axis
    rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)

    # Use Rodrigues' rotation formula to create the rotation matrix
    K = np.array(
        [
            [0, -rotation_axis[2], rotation_axis[1]],
            [rotation_axis[2], 0, -rotation_axis[0]],
            [-rotation_axis[1], rotation_axis[0], 0],
        ]
    )

    R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)

    return R


def create_rotation_matrix(axis, angle):
    """
    Create a rotation matrix given an axis and an angle.

    """
    K = np.array(
        [[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]]
    )

    return np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)


def axis_angle_to_rotation_matrix(axis, angle):
    # Normalize the axis
    axis = np.array(axis)
    norm = np.linalg.norm(axis)

    if norm == 0:
        raise ValueError("The rotation axis cannot be the zero vector.")

    unit_axis = axis / norm
    u_x, u_y, u_z = unit_axis

    # Compute the rotation matrix using Rodrigues' formula
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)

    # Skew-symmetric cross product matrix
    K = np.array([[0, -u_z, u_y], [u_z, 0, -u_x], [-u_y, u_x, 0]])

    # Rotation matrix
    R = np.eye(3) + sin_theta * K + (1 - cos_theta) * np.dot(K, K)

    return R


"""
*** CHAPTER 4: FORWARD KINEMATICS ***
"""


def FKinSpace(M, Slist, thetalist):
    """Computes forward kinematics in the space frame for an open chain robot

    :param M: The home configuration (position and orientation) of the end-
                effector
    :param Slist: The joint screw axes in the space frame when the
                    manipulator is at the home position, in the format of a
                    matrix with axes as the columns
    :param thetalist: A list of joint coordinates
    :return: A homogeneous transformation matrix representing the end-
                effector frame when the joints are at the specified coordinates
                (i.t.o Space Frame)

    Example Input:
        M = np.array([[-1, 0,  0, 0],
                        [ 0, 1,  0, 6],
                        [ 0, 0, -1, 2],
                        [ 0, 0,  0, 1]])
        Slist = np.array([[0, 0,  1,  4, 0,    0],
                            [0, 0,  0,  0, 1,    0],
                            [0, 0, -1, -6, 0, -0.1]]).T
        thetalist = np.array([np.pi / 2.0, 3, np.pi])
    Output:
        np.array([[0, 1,  0,         -5],
                    [1, 0,  0,          4],
                    [0, 0, -1, 1.68584073],
                    [0, 0,  0,          1]])
    """
    # if not is_casadi_type([M, Slist, thetalist]):
    #     T = np.array(M)
    # if is_casadi_type([M, Slist, thetalist]):

    #     def make_row(contents: List):
    #         try:
    #             return ca.horzcat(*contents)
    #         except (TypeError, Exception):
    #             return contents

    #     T = ca.vertcat(*[make_row(row) for row in M])
    #     # M = ca.MX.sym('M', m.shape[0], m.shape[1])\
    #     # T = ca.MX(m)
    T = np.array(M)
    for i in range(np.length(thetalist) - 1, -1, -1):
        # print(f"i: {i}")
        # print(MatrixExp6(VecTose3(np.array(Slist)[:, i] * thetalist[i])).shape)
        # print(type(MatrixExp6(VecTose3(np.array(Slist)[:, i] * thetalist[i]))))
        # print(T.shape)
        # print(type(T))
        # T = np.dot(MatrixExp6(VecTose3(np.array(Slist)[:, i] * thetalist[i])), T)
        print(np.array(Slist)[:, i])
        print(np.array(Slist)[:, i] @ ca.vertcat(thetalist[i]))
        print(ca.mtimes(np.array(Slist)[:, i], ca.vertcat(thetalist[i])))
        print("======================")
        T = MatrixExp6(VecTose3(np.array(Slist)[:, i] * thetalist[i])) @ T
        # print(T.shape)
        # print(type(T))
    return T


def FKinSpace_all(Jilist, Slist, thetalist):
    """
    Computes forward kinematics in the space frame

    Args:
        Jilist: Ji is the zero position transformation matrix from the base frame to joint frame i, Milist is a list of these
        Slist: 6xn matrix of screw axes in space frame
        thetalist: n-vector of joint variables

    Returns:
        Tlist: List of transformations for each frame
    """
    n = np.length(thetalist)
    Tlist = [np.eye(4)]  # Start with identity matrix for base frame

    # Calculate transformation up to each frame
    for i in range(n):
        Mi = Jilist[i]  # Home configuration for current frame

        # Calculate product of exponentials up to current joint
        T = np.eye(4)
        for j in range(i + 1):
            S = Slist[:, j]
            theta = thetalist[j]
            # T = T @ MatrixExp6(VecTose3(S) * theta)
            T = np.dot(T, MatrixExp6(VecTose3(S) * theta))

        # Multiply by home configuration
        # T = T @ Mi
        T = np.dot(T, Mi)
        Tlist.append(T)
    return Tlist
