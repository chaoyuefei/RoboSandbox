#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.ERobot import ERobot
import os
import pathlib
import time

try:
    from .generic_dh_robot import DH_2_URDF
except ImportError:
    from generic_dh_robot import DH_2_URDF


class GenericDH(ERobot):
    def __init__(
        self,
        dofs,
        a=None,
        d=None,
        alpha=None,
        offset=None,
        qlim=None,
        name="GenericDH",
        joint_types=None,
        gripper_links=None,
        link_radius=0.04,
        actuator_radius=0.05,
        actuator_length=0.1,
    ):
        """
        Create a generic robot from DH parameters

        This class generates a URDF file from DH parameters and stores it
        persistently in the rsb-data directory for later access. The URDF
        filename is automatically generated to avoid conflicts.

        Parameters:
        -----------
        dofs : int
            Number of degrees of freedom
        a : array_like, optional
            Link lengths (default: zeros)
        d : array_like, optional
            Link offsets (default: zeros)
        alpha : array_like, optional
            Link twists (default: zeros)
        offset : array_like, optional
            Joint offsets (default: zeros)
        qlim : array_like, optional
            Joint limits [[qmin], [qmax]] (default: [-pi, pi] for all joints)
        name : str, optional
            Robot name (default: "GenericDH")
        joint_types : list, optional
            List of joint types, e.g. ['r', 'p', 'f'] (default: all 'r')
        link_radius : float, optional
            Radius of the links (default: 0.04)
        actuator_radius : float, optional
            Radius of the actuators (default: 0.05)
        actuator_length : float, optional
            Length of the actuators (default: 0.1)

        Note:
        -----
        The generated URDF file is stored in rsb-data/{name}_{dofs}dof.urdf
        and can be accessed later via the urdf_file_path property.
        """
        # print(qlim.shape)
        # print(qlim)
        # Set default values
        if a is None:
            a = [0.0] * dofs
        if d is None:
            d = [0.0] * dofs
        if alpha is None:
            alpha = [0.0] * dofs
        if offset is None:
            offset = [0.0] * dofs
        if qlim is None:
            qlim = np.array([[-np.pi] * dofs, [np.pi] * dofs])
        if joint_types is None:
            joint_types = ["r"] * dofs

        # Allow link_radius, actuator_radius, actuator_length as float or list
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

        link_radius = ensure_list(link_radius, dofs)
        actuator_radius = ensure_list(actuator_radius, dofs)
        actuator_length = ensure_list(actuator_length, dofs)

        # Validate dimensions
        if not all(len(param) == dofs for param in [a, d, alpha, offset, joint_types]):
            raise ValueError(
                "All DH parameter arrays and joint_types must have length equal to dofs"
            )

        # Generate URDF string using DH_2_URDF
        dh2urdf = DH_2_URDF(
            dofs=dofs,
            a=a,
            d=d,
            alpha=alpha,
            link_radius=link_radius,
            actuator_radius=actuator_radius,
            actuator_length=actuator_length,
            qlim=[(None, None)]
            * dofs,  # qlim not used in URDF string, but kept for compatibility
            name=name,
            joint_types=joint_types,
        )
        urdf_string = dh2urdf.generate_urdf()

        # Create persistent URDF file in rsb-data folder
        current_dir = pathlib.Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        rsb_data_dir = project_root / "rsb-data"

        # Ensure rsb-data directory exists
        rsb_data_dir.mkdir(exist_ok=True)

        # Create unique filename based on robot name and parameters
        urdf_filename = self._generate_unique_filename(rsb_data_dir, name, dofs)
        urdf_filepath = rsb_data_dir / urdf_filename

        # Write URDF file
        with open(urdf_filepath, "w") as f:
            f.write(urdf_string)

        # Read the URDF
        links, robot_name, urdf_string, _ = self.URDF_read(
            file_path=str(urdf_filepath), tld=None
        )

        super().__init__(
            links,
            name=name,
            manufacturer="Generic",
            urdf_string=urdf_string,
            urdf_filepath=str(urdf_filepath),
            # gripper_links=links[-1],
        )

        # Set joint limits
        self.qlim = qlim

        # Set default configurations
        self.qz = np.zeros(dofs)
        self.qr = np.zeros(dofs)  # Can be customized based on specific robot

        self.addconfiguration("qz", self.qz)
        self.addconfiguration("qr", self.qr)

        # Store DH parameters for reference
        self._dh_a = np.array(a)
        self._dh_d = np.array(d)
        self._dh_alpha = np.array(alpha)
        self._dh_offset = np.array(offset)
        self._joint_types = joint_types

        # Store URDF file path for reference
        self._urdf_filepath = str(urdf_filepath)

    def _generate_unique_filename(self, directory, name, dofs):
        """
        Generate a unique URDF filename to avoid conflicts

        Parameters:
        -----------
        directory : pathlib.Path
            Directory where the file will be stored
        name : str
            Base name for the robot
        dofs : int
            Number of degrees of freedom

        Returns:
        --------
        str
            Unique filename
        """
        base_filename = f"{name}_{dofs}dof"
        urdf_filename = f"{base_filename}.urdf"

        # Check if file already exists and create unique name if needed
        counter = 1
        while (directory / urdf_filename).exists():
            urdf_filename = f"{base_filename}_{counter}.urdf"
            counter += 1

        return urdf_filename

    @property
    def urdf_file_path(self):
        """
        Get the path to the stored URDF file

        Returns:
        --------
        str
            Path to the URDF file
        """
        return self._urdf_filepath

    @classmethod
    def cleanup_generated_urdf_files(cls, name_pattern=None):
        """
        Clean up generated URDF files from rsb-data directory

        Parameters:
        -----------
        name_pattern : str, optional
            Pattern to match filenames (e.g., "GenericDH*" or "test_robot*")
            If None, removes all *_*dof*.urdf files

        Returns:
        --------
        list
            List of deleted file paths
        """
        import glob

        # Get rsb-data directory path
        current_dir = pathlib.Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        rsb_data_dir = project_root / "rsb-data"

        if not rsb_data_dir.exists():
            return []

        # Define search pattern
        if name_pattern is None:
            search_pattern = str(rsb_data_dir / "*_*dof*.urdf")
        else:
            search_pattern = str(rsb_data_dir / f"{name_pattern}.urdf")

        # Find and remove matching files
        deleted_files = []
        for file_path in glob.glob(search_pattern):
            try:
                os.unlink(file_path)
                deleted_files.append(file_path)
            except OSError:
                pass  # File might be in use or already deleted

        return deleted_files

    def teach(self, q=None, realtime=True):
        """
        Launch an interactive teaching interface for the robot using Swift

        This method creates a Swift environment with sliders to control each
        joint of the robot in real-time. Similar to the MATLAB Robotics
        Toolbox teach() function.

        Parameters:
        -----------
        realtime : bool, optional
            Whether to run the simulation in real-time (default: True)
        config : str, optional
            Initial configuration to use ('qr', 'qz', or None for current)
            (default: 'qr')

        Returns:
        --------
        None

        Example:
        --------
        >>> robot = GenericDH(dofs=4, name="MyRobot")
        >>> robot.teach()  # Opens interactive interface with ready pose
        >>> robot.teach(config='qz')  # Start from zero configuration
        """
        try:
            import swift
        except ImportError:
            raise ImportError(
                "Swift package is required for teach functionality. "
                "Please install it with: pip install swift-sim"
            )

        # Launch the simulator Swift
        env = swift.Swift()
        env.launch(realtime=realtime)

        self.q = np.zeros(self.n) if q is None else np.array(q)

        env.add(self)

        # Callback function for sliders to set joint angles
        def set_joint(j, value):
            self.q[j] = np.deg2rad(float(value))

        # Add sliders for each joint
        j = 0
        for link in self.links:
            if link.isjoint and hasattr(link, "qlim") and link.qlim is not None:
                # Add slider with joint limits and current position
                env.add(
                    swift.Slider(
                        lambda x, j=j: set_joint(j, x),
                        min=np.round(np.rad2deg(link.qlim[0]), 3),
                        max=np.round(np.rad2deg(link.qlim[1]), 3),
                        step=1,
                        value=np.round(np.rad2deg(self.q[j]), 3),
                        desc=f"{self.name} Joint {j}",
                        unit="&#176;",  # HTML unicode for degree sign
                    )
                )
                j += 1

        print(f"Teaching interface launched for {self.name}")
        print(f"Robot has {self.n} joints with the following limits:")
        j = 0
        for link in self.links:
            if link.isjoint and hasattr(link, "qlim") and link.qlim is not None:
                print(
                    f"  Joint {j}: [{np.rad2deg(link.qlim[0]):.3f}°, {np.rad2deg(link.qlim[1]):.3f}°]"
                )
                j += 1
        print(
            "Use the sliders to control joint angles. Press Ctrl+C or close the Swift window to exit."
        )

        # Main control loop
        try:
            while True:
                # Update the environment with the new robot pose
                env.step(0.0)
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("\nTeaching session ended by user.")
            print(f"Final joint configuration: {np.rad2deg(self.q)}")
        except Exception as e:
            print(f"Teaching session ended due to error: {e}")
        finally:
            # Clean up
            try:
                env.close()
            except Exception:
                pass

    def interactive_teach(self, **kwargs):
        """
        Convenience method that calls teach_gui() with the same parameters

        This method provides an alternative name for the interactive teaching interface.

        Parameters:
        -----------
        **kwargs
            All keyword arguments are passed to teach()

        Example:
        --------
        >>> robot = GenericDH(dofs=4, name="MyRobot")
        >>> robot.interactive_teach()  # Opens interactive interface
        """
        return self.teach(**kwargs)


if __name__ == "__main__":
    import roboticstoolbox as rtb

    # Example usage
    robot = GenericDH(
        dofs=6,
        a=[0, -0.42500, -0.39225, 0, 0, 0],
        d=[0.089459, 0, 0, 0.10915, 0.09465, 0.0823],
        alpha=[np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0],
        offset=[0, 0, 0, 0, 0, 0],
        link_radius=[0.060, 0.054, 0.060, 0.040, 0.045, 0.045],
        actuator_radius=[0.064, 0.060, 0.060, 0.060, 0.045, 0.045],
        actuator_length=[0.04, 0.12, 0.12, 0.12, 0.05, 0.090],
        # qlim=np.array([-np.pi * np.ones(6), np.pi * np.ones(6)]),
    )
    print(f"Created robot: {robot.name} with {robot.n} DOFs")
    print(f"URDF file path: {robot.urdf_file_path}")

    # Launch interactive teaching interface
    print(robot)
    print(robot.fkine(robot.qz))
    robot.teach()
