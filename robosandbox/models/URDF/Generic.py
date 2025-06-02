#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.ERobot import ERobot
import tempfile
import os

try:
    from .dh_to_urdf import xml_string
except ImportError:
    from dh_to_urdf import xml_string


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
    ):
        """
        Create a generic robot from DH parameters

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
        """

        # Set default values
        if a is None:
            a = np.zeros(dofs)
        if d is None:
            d = np.zeros(dofs)
        if alpha is None:
            alpha = np.zeros(dofs)
        if offset is None:
            offset = np.zeros(dofs)
        if qlim is None:
            qlim = np.array([[-np.pi] * dofs, [np.pi] * dofs])

        # Convert to numpy arrays
        a = np.array(a)
        d = np.array(d)
        alpha = np.array(alpha)
        offset = np.array(offset)

        # Validate dimensions
        if not all(len(param) == dofs for param in [a, d, alpha, offset]):
            raise ValueError("All DH parameter arrays must have length equal to dofs")

        # Create DH parameter list for URDF generation
        # Assuming all joints are revolute for now
        DH_Params = []
        for i in range(dofs):
            DH_Params.append(["r", d[i], a[i], alpha[i]])

        # Generate URDF string
        urdf_string = xml_string(DH_Params)

        # Create temporary URDF file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".urdf", delete=False) as f:
            f.write(urdf_string)
            urdf_filepath = f.name

        try:
            # Read the URDF
            links, robot_name, urdf_string, _ = self.URDF_read(
                file_path=urdf_filepath, tld=None
            )

            super().__init__(
                links,
                name=name,
                manufacturer="Generic",
                urdf_string=urdf_string,
                urdf_filepath=urdf_filepath,
            )

        finally:
            # Clean up temporary file
            if os.path.exists(urdf_filepath):
                os.unlink(urdf_filepath)

        # Set joint limits
        self.qlim = qlim

        # Set default configurations
        self.qz = np.zeros(dofs)
        self.qr = np.zeros(dofs)  # Can be customized based on specific robot

        self.addconfiguration("qz", self.qz)
        self.addconfiguration("qr", self.qr)

        # Store DH parameters for reference
        self._dh_a = a
        self._dh_d = d
        self._dh_alpha = alpha
        self._dh_offset = offset