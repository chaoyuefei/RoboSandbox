import numpy as np
import matplotlib.pyplot as plt
from robosandbox.visualization.plotly_Link3D import Link3D
from robosandbox.geometry.mesh_utilities import add_face, index_of


class CylinderLink(Link3D):
    def __init__(
        self,
        length=0.5,
        E=70e6,
        rho=2700,
        Rout=25e-3,
        inner_profile={"params": [20e-3, 20e-3], "method": "linear"},
        resolutions={"axial": 80, "radial": 10, "angular": 360},
    ):
        self.len = length
        self.resolutions = resolutions
        self.segments_number = self.resolutions["axial"]  # segments number along z axis
        self.segement_length = self.len / self.segments_number
        self.segments_location = np.linspace(0, self.len, self.segments_number)
        self.E = E
        self.rho = rho
        self.inner_profile = inner_profile
        self.thickness_distribution = self.get_thickness_distribution(
            inner_profile["params"], inner_profile["method"]
        )
        self.Rout = Rout
        self.mass = self.get_link_mass()
        self.COM = self.get_center_of_mass()
        self.I_tensor = self.get_inertia_tensor(self.COM)

    def get_discretized_points(self):
        """
        Get the discretized points (x,y,z)
        return: list of points [(x,y,z), (x,y,z), ...]
        """
        points = []
        for idx in range(self.segments_number):
            z = self.segments_location[idx]
            for phi in np.linspace(0, 2 * np.pi, self.resolutions["angular"]):
                for r in np.arange(
                    float(self.Rout - self.thickness_distribution[idx]),
                    float(self.Rout),
                    1e-3,
                ):
                    x = r * np.cos(phi)
                    y = r * np.sin(phi)
                    points.append((x, y, z))
        return points, len(points)

    def get_outer_mesh(self, method="quad"):
        """
        Get the mesh of the outer surface
        return: list of mesh [(x,y,z), (x,y,z), ...]
        """
        points = []
        for idx in range(self.resolutions["axial"]):
            z = self.segments_location[idx]
            for phi in np.linspace(0, 2 * np.pi, self.resolutions["angular"]):
                x = self.Rout * np.cos(phi)
                y = self.Rout * np.sin(phi)
                # if near 0, set to 0
                if abs(x) < 1e-10:
                    x = 0
                if abs(y) < 1e-10:
                    y = 0
                points.append((x, y, z))

        faces = []
        for j in range(self.resolutions["axial"] - 1):
            for i in range(self.resolutions["angular"] - 1):
                faces = add_face(
                    faces,
                    index_of(i, j, self.resolutions["angular"]),
                    index_of(i + 1, j, self.resolutions["angular"]),
                    index_of(i + 1, j + 1, self.resolutions["angular"]),
                    index_of(i, j + 1, self.resolutions["angular"]),
                    method=method,
                )
        return np.array(points), np.array(faces)

    def get_inner_mesh(self, method="quad"):
        """
        Get the mesh of the outer surface
        return: list of mesh [(x,y,z), (x,y,z), ...]
        """
        points = []
        for idx in range(self.resolutions["axial"]):
            z = self.segments_location[idx]
            for phi in np.linspace(0, 2 * np.pi, self.resolutions["angular"]):
                x = (self.Rout - self.thickness_distribution[idx]) * np.cos(phi)
                y = (self.Rout - self.thickness_distribution[idx]) * np.sin(phi)
                # if near 0, set to 0
                if abs(x) < 1e-10:
                    x = 0
                if abs(y) < 1e-10:
                    y = 0
                points.append((x, y, z))

        faces = []
        for j in range(self.resolutions["axial"] - 1):
            for i in range(self.resolutions["angular"] - 1):
                faces = add_face(
                    faces,
                    index_of(i, j, self.resolutions["angular"]),
                    index_of(i + 1, j, self.resolutions["angular"]),
                    index_of(i + 1, j + 1, self.resolutions["angular"]),
                    index_of(i, j + 1, self.resolutions["angular"]),
                    method=method,
                )
        return np.array(points), np.array(faces)

    def get_side_mesh(self, method="quad", side="start"):
        """
        Get the mesh of the outer surface
        return: list of mesh [(x,y,z), (x,y,z), ...]
        """
        if side == "start":
            idx = 0
        if side == "end":
            idx = -1

        points = []
        for r in np.linspace(
            self.Rout - self.thickness_distribution[idx],
            self.Rout,
            self.resolutions["radial"],
        ):
            z = self.segments_location[idx]
            for phi in np.linspace(0, 2 * np.pi, self.resolutions["angular"]):
                x = r * np.cos(phi)
                y = r * np.sin(phi)
                # if near 0, set to 0
                if abs(x) < 1e-10:
                    x = 0
                if abs(y) < 1e-10:
                    y = 0
                points.append((x, y, z))

        faces = []
        for j in range(self.resolutions["radial"] - 1):
            for i in range(self.resolutions["angular"] - 1):
                faces = add_face(
                    faces,
                    index_of(i, j, self.resolutions["angular"]),
                    index_of(i + 1, j, self.resolutions["angular"]),
                    index_of(i + 1, j + 1, self.resolutions["angular"]),
                    index_of(i, j + 1, self.resolutions["angular"]),
                    method=method,
                )
        return np.array(points), np.array(faces)

    # def get_outer_side_mesh_connected(self, stacked_mesh, method="quad"):
    #     points = stacked_mesh[0]
    #     faces = stacked_mesh[1]

    def plot_discretized_points(self):
        """
        Plot the discretized points
        """
        points, number = self.get_discretized_points()
        points = np.array(points)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        # make points transparent
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], alpha=0.1)
        # ax.scatter(points[:, 0], points[:, 1], points[:, 2])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Discretized Points")
        plt.show()

    def get_thickness_distribution(self, parameters, method="linear"):
        """
        Get the thickness distribution of the link
        parameters: list of parameters [p1, p2, ...]
        method: method of thickness distribution
        return: list of thickness distribution [t1, t2, ...], shape = (segments_number,)
        """
        if method == "linear":
            initial_thickness = parameters[0]
            final_thickness = parameters[1]
            thickness = np.linspace(
                initial_thickness, final_thickness, self.segments_number
            )
            return thickness

    def get_segments_mass(self):
        """
        Get the mass of each segment
        return: list of mass [m1, m2, ...], shape = (segments_number,)
        """
        segments_mass = []
        for thickness in self.thickness_distribution:
            mass = (
                np.pi
                * (self.Rout**2 - (self.Rout - thickness) ** 2)
                * self.segement_length
                * self.rho
            )
            segments_mass.append(mass)
        return segments_mass

    def get_link_mass(self):
        """
        Get the mass of the link
        return: mass of the link
        """
        if self.inner_profile["params"][0] == self.inner_profile["params"][1]:
            return (
                np.pi
                * (self.Rout**2 - (self.Rout - self.inner_profile["params"][0]) ** 2)
                * self.len
                * self.rho
            )
        else:
            return sum(self.get_segments_mass())

    def get_inertia_tensor(self, origin=(0, 0, 0)):
        """
        Get the inertia tensor, the origin is at (0, 0, 0) by default
        origin: origin of the frame
        return: inertia tensor, shape = (3, 3)
        """
        if self.inner_profile["params"][0] == self.inner_profile["params"][1]:
            return self.inertia_vector_hollow_cylinder(
                M=self.mass,
                R1=self.inner_profile["params"][0],
                R2=self.Rout,
                h=self.len,
            )

        points, points_number = self.get_discretized_points()
        Ixx, Iyy, Izz, Ixy, Ixz, Iyz = 0, 0, 0, 0, 0, 0
        points_mass = self.mass / points_number
        for point in points:
            x, y, z = point
            x -= origin[0]
            y -= origin[1]
            z -= origin[2]
            Ixx += points_mass * (y**2 + z**2)
            Iyy += points_mass * (x**2 + z**2)
            Izz += points_mass * (x**2 + y**2)
            Ixy -= points_mass * x * y
            Ixz -= points_mass * x * z
            Iyz -= points_mass * y * z
        I_tensor = np.array([[Ixx, Ixy, Ixz], [Ixy, Iyy, Iyz], [Ixz, Iyz, Izz]])
        return I_tensor

    def get_center_of_mass(self):
        """
        Get the center of mass
        return: center of mass (x, y, z)
        """
        if self.inner_profile["params"][0] == self.inner_profile["params"][1]:
            return np.array([0, 0, self.len / 2])
        points, points_number = self.get_discretized_points()
        x, y, z = 0, 0, 0
        points_mass = self.mass / points_number
        for point in points:
            x += point[0] * points_mass
            y += point[1] * points_mass
            z += point[2] * points_mass
        COM = np.array([x, y, z]) / self.mass
        # COM = np.mean(np.array(points), axis=0) # another way to calculate the center of mass since the points are equivalent
        return COM

    @staticmethod
    def inertia_vector_hollow_cylinder(M, R1, R2, h) -> np.ndarray:
        """
        Calculate the inertia vector of a hollow cylinder.

        Parameters:
        M  -- Mass of the cylinder (kg)
        R1 -- Inner radius (m)
        R2 -- Outer radius (m)
        h  -- Height of the cylinder (m)

        Returns:
        inertia_tensor
        """
        # Calculate the moments of inertia around each principal axis
        Ixx = (1 / 4) * M * (R1**2 + R2**2) + (1 / 12) * M * h**2
        Iyy = Ixx  # Due to symmetry
        Izz = (1 / 2) * M * (R1**2 + R2**2)

        inertia_tensor = np.array([[Ixx, 0, 0], [0, Iyy, 0], [0, 0, Izz]])

        return inertia_tensor
