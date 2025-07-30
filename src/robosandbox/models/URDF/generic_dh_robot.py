import numpy as np
from numpy import sin, cos, pi
from scipy.spatial.transform import Rotation as R


class DH_2_URDF:
    def __init__(
        self,
        dofs,
        a=None,
        d=None,
        alpha=None,
        link_radius=0.04,
        actuator_radius=0.05,
        actuator_length=0.1,
        qlim=None,
        name="GenericDH",
        joint_types=None,
    ):
        """
        Initialize the GenericDH robot.

        Parameters:
        - dofs: Number of degrees of freedom (int)
        - a: List of link lengths (default: None)
        - d: List of link offsets (default: None)
        - alpha: List of link twists (default: None)
        - link_radius: Radius of the links (default: 0.04)
        - actuator_radius: Radius of the actuators (default: 0.05)
        - actuator_length: Length of the actuators (default: 0.1)
        - qlim: Joint limits (default: None)
        - name: Name of the robot (default: "GenericDH")
        - joint_types: List of joint types, e.g. ['r', 'p', 'f'] (default: all 'r')
        """
        self.dofs = dofs
        self.a = a if a is not None else [0] * dofs
        self.d = d if d is not None else [0] * dofs
        self.alpha = alpha if alpha is not None else [0] * dofs

        def ensure_list(val, length):
            if isinstance(val, (float, int)):
                return [val] * length
            if isinstance(val, list) or isinstance(val, np.ndarray):
                if len(val) != length:
                    raise ValueError("Length of list parameter does not match dofs")
                return list(val)
            raise ValueError(
                "Parameter must be a float, int, or list of correct length"
            )

        self.link_radius = ensure_list(link_radius, dofs)
        self.actuator_radius = ensure_list(actuator_radius, dofs)
        self.actuator_length = ensure_list(actuator_length, dofs)
        self.qlim = qlim if qlim is not None else [(None, None)] * dofs
        self.name = name
        self.joint_types = joint_types if joint_types is not None else ["r"] * dofs

    def dh_trans(self, DH, joint_val):
        # DH: [joint_type, d/theta, a, alpha] or [joint_type, d, theta, a, alpha] for fixed
        if DH[0] == "r":
            d, theta, a, alpha = (DH[1], joint_val, DH[2], DH[3])
        elif DH[0] == "p":
            d, theta, a, alpha = (joint_val, DH[1], DH[2], DH[3])
        elif DH[0] == "f":
            d, theta, a, alpha = (DH[1], DH[2], DH[3], DH[4])
        else:
            raise ValueError(f"Unknown joint type: {DH[0]}")
        trans_mat = np.array(
            [
                [
                    cos(theta),
                    -1 * sin(theta) * cos(alpha),
                    sin(theta) * sin(alpha),
                    a * cos(theta),
                ],
                [
                    sin(theta),
                    cos(theta) * cos(alpha),
                    -1 * cos(theta) * sin(alpha),
                    a * sin(theta),
                ],
                [0, sin(alpha), cos(alpha), d],
                [0, 0, 0, 1],
            ]
        )
        return trans_mat

    def joint_transforms(self, DH_Params):
        transforms = []
        transforms.append(np.eye(4))
        for DH in DH_Params:
            if DH[0] in ("r", "p"):
                transforms.append(self.dh_trans(DH, 0.0))
            else:
                transforms.append(self.dh_trans(DH, 0.0))
        return transforms

    def joint_frames(self, transforms):
        joint_frames = [transforms[0]]
        for trans in transforms[1:]:
            joint_frames.append(joint_frames[-1] @ trans)
        return joint_frames

    def build_DH_params(self):
        # Build DH_Params list for internal use
        DH_Params = []
        for i in range(self.dofs):
            jt = self.joint_types[i] if self.joint_types else "r"
            if jt == "r":
                DH_Params.append(["r", self.d[i], self.a[i], self.alpha[i]])
            elif jt == "p":
                DH_Params.append(["p", 0.0, self.a[i], self.alpha[i]])
            elif jt == "f":
                # For fixed, need d, theta, a, alpha
                DH_Params.append(["f", self.d[i], 0.0, self.a[i], self.alpha[i]])
            else:
                raise ValueError(f"Unknown joint type: {jt}")
        return DH_Params

    def generate_urdf(self):
        """
        Generate the URDF string for the robot, following dh_to_urdf.py logic.
        """
        DH_Params = self.build_DH_params()
        transforms = self.joint_transforms(DH_Params)
        frames = self.joint_frames(transforms)

        urdf = f"<robot name='{self.name}'>\n"
        urdf += (
            "\t<material name='blue'>\n\t\t<color rgba='0 0 0.8 1'/>\n\t</material>\n"
        )
        urdf += (
            "\t<material name='red'>\n\t\t<color rgba='0.8 0 0 1'/>\n\t</material>\n"
        )

        for i in range(len(transforms)):
            if i < self.dofs:
                el = transforms[i]
                fr = frames[i]

                # Link for actuator
                rpy = R.from_matrix(fr[0:3, 0:3]).as_euler("XYZ")
                rpy_str = f"{round(rpy[0], 3)} {round(rpy[1], 3)} {round(rpy[2], 3)}"
                xyz_str = (
                    f"{round(el[0, 3], 3)} {round(el[1, 3], 3)} {round(el[2, 3], 3)}"
                )
                urdf += f"\t<link name='a{i}'>\n"
                urdf += "\t\t<visual>\n"
                urdf += f"\t\t\t<origin rpy='{rpy_str}' xyz='{xyz_str}'/>\n"
                urdf += "\t\t\t<geometry>\n"
                urdf += f"\t\t\t\t<cylinder length='{self.actuator_length[i]}' radius='{self.actuator_radius[i]}'/>\n"
                urdf += "\t\t\t</geometry>\n"
                urdf += "\t\t\t<material name='blue'><color rgba='0.73 0.79 0.82 1'/></material>\n"
                urdf += "\t\t</visual>\n"
                urdf += "\t\t<collision>\n"
                urdf += "\t\t\t<geometry>\n"
                urdf += f"\t\t\t\t<cylinder length='{self.actuator_length[i]}' radius='{self.actuator_radius[i]}'/>\n"
                urdf += "\t\t\t</geometry>\n"
                urdf += "\t\t</collision>\n"
                urdf += "\t</link>\n"

                # If not on the first transformation, fix the actuator to the previous link
                if i != 0:
                    urdf += f"\t<joint name='fix_a{i}_to_l{i - 1}' type='fixed'>\n"
                    urdf += f"\t\t<parent link='l{i - 1}'/>\n"
                    urdf += f"\t\t<child link='a{i}'/>\n"
                    urdf += "\t\t<origin rpy='0 0 0' xyz='0 0 0'/>\n"
                    urdf += "\t</joint>\n"

                # Link for the actual link (cylinder between origins)
                origins_vector = transforms[i + 1][0:3, 3]
                origins_vector_norm = np.linalg.norm(origins_vector)
                cylinder_origin = (
                    origins_vector / 2 if origins_vector_norm != 0 else origins_vector
                )

                rpy_link = [0, 0, 0]
                if origins_vector_norm != 0.0:
                    origins_vector_unit = origins_vector / origins_vector_norm
                    axis = np.cross(origins_vector, np.array([0, 0, -1]))
                    axis_norm = np.linalg.norm(axis)
                    if axis_norm != 0.0:
                        axis = axis / axis_norm
                    angle = np.arccos(origins_vector_unit @ np.array([0, 0, 1]))
                    rpy_link = R.from_rotvec(angle * axis).as_euler("XYZ")
                    rpy_link_str = f"{round(rpy_link[0], 3)} {round(rpy_link[1], 3)} {round(rpy_link[2], 3)}"
                    xyz_link_str = f"{round(cylinder_origin[0], 3)} {round(cylinder_origin[1], 3)} {round(cylinder_origin[2], 3)}"

                    urdf += f"\t<link name='l{i}'>\n"
                    urdf += "\t\t<visual>\n"
                    urdf += (
                        f"\t\t\t<origin rpy='{rpy_link_str}' xyz='{xyz_link_str}'/>\n"
                    )
                    urdf += "\t\t\t<geometry>\n"
                    urdf += f"\t\t\t\t<cylinder length='{origins_vector_norm}' radius='{self.link_radius[i]}'/>\n"
                    urdf += "\t\t\t</geometry>\n"
                    urdf += "\t\t\t<material name='grey'><color rgba='0.99 0.54 0.54 1'/></material>\n"
                    urdf += "\t\t</visual>\n"
                    urdf += "\t\t<collision>\n"
                    urdf += "\t\t\t<geometry>\n"
                    urdf += f"\t\t\t\t<cylinder length='{origins_vector_norm}' radius='{self.link_radius[i]}'/>\n"
                    urdf += "\t\t\t</geometry>\n"
                    urdf += "\t\t</collision>\n"

                    urdf += "\t</link>\n"

                # Add the actual joint between the actuator and link
                jt = DH_Params[i][0]
                if jt == "r":
                    jointType = "continuous"
                elif jt == "p":
                    jointType = "prismatic"
                else:
                    jointType = "fixed"

                urdf += f"\t<joint name='move_l{i}_from_a{i}' type='{jointType}'>\n"
                urdf += f"\t\t<parent link='a{i}'/>\n"
                urdf += f"\t\t<child link='l{i}'/>\n"
                # Axis: use z-axis of the frame
                urdf += f"\t\t<axis xyz='{np.round(fr[0, 2], 5)} {np.round(fr[1, 2], 5)} {np.round(fr[2, 2], 5)}'/>\n"
                urdf += f"\t\t<origin rpy='0 0 0' xyz='{el[0, 3]} {el[1, 3]} {el[2, 3]}'/>\n"
                urdf += "\t</joint>\n"

            if i == self.dofs:
                el = transforms[i]
                fr = frames[i]
                rpy = R.from_matrix(fr[0:3, 0:3]).as_euler("XYZ")
                rpy_str = f"{round(rpy[0], 3)} {round(rpy[1], 3)} {round(rpy[2], 3)}"
                xyz_str = (
                    f"{round(el[0, 3], 3)} {round(el[1, 3], 3)} {round(el[2, 3], 3)}"
                )

                urdf += "\t<link name='tool0'/>\n"
                urdf += "\t<joint name='tool0_fixed_joint' type='fixed'>\n"
                urdf += f"\t\t<origin rpy='{rpy_str}' xyz='{xyz_str}'/>\n"
                urdf += f"\t\t<parent link='l{self.dofs - 1}'/>\n"
                urdf += "\t\t<child link='tool0'/>\n"
                urdf += "\t</joint>\n"

        urdf += "</robot>\n"
        return urdf

    def save_urdf(self, filename="robot.urdf"):
        urdf = self.generate_urdf()
        with open(filename, "w") as f:
            f.write(urdf)


if __name__ == "__main__":
    # Example usage
    # ['r', d, a, alpha] for revolute joints
    # ['p', theta, a, alpha] for prismatic joints
    # ['f', d, theta, a, alpha] for fixed joints
    robot = DH_2_URDF(
        dofs=6,
        a=[0, -0.42500, -0.39225, 0, 0, 0],
        d=[0.089459, 0, 0, 0.10915, 0.09465, 0.0823],
        alpha=[np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0],
        link_radius=0.04,
        actuator_radius=0.02,
        actuator_length=0.05,
        qlim=[(None, None)] * 4,
        name="ExampleRobot",
        joint_types=["r", "r", "r", "r", "r", "r"],
    )
    robot.save_urdf("example_robot.urdf")
