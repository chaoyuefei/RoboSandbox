from typing import Callable, Dict, List, Tuple
import numpy as np


class ManipulabilityIndices:
    """
    Class that implements manipulability indices calculations.
    """

    @staticmethod
    def yoshikawa(workspace, joint_points, axes="all") -> float:
        """
        Calculate the Yoshikawa manipulability index.

        :param workspace: The workspace instance providing access to the robot.
        :param joint_points: List of joint configurations to evaluate.
        :param axes: Which axes to consider ('all', 'trans', 'rot').
        :return: The average Yoshikawa manipulability index.
        """
        return ManipulabilityIndices._calculate_manipulability(
            workspace, joint_points, method="yoshikawa", axes=axes
        )

    @staticmethod
    def invcondition(workspace, joint_points, axes="all") -> float:
        """
        Calculate the inverse condition number manipulability index.

        :param workspace: The workspace instance providing access to the robot.
        :param joint_points: List of joint configurations to evaluate.
        :param axes: Which axes to consider ('all', 'trans', 'rot').
        :return: The average inverse condition number index.
        """
        return ManipulabilityIndices._calculate_manipulability(
            workspace, joint_points, method="invcondition", axes=axes
        )

    @staticmethod
    def asada(workspace, joint_points, axes="all") -> float:
        """
        Calculate the Asada manipulability index.

        :param workspace: The workspace instance providing access to the robot.
        :param joint_points: List of joint configurations to evaluate.
        :param axes: Which axes to consider ('all', 'trans', 'rot').
        :return: The average Asada manipulability index.
        """
        return ManipulabilityIndices._calculate_manipulability(
            workspace, joint_points, method="asada", axes=axes
        )

    @staticmethod
    def _calculate_manipulability(workspace, joint_points, method, axes="all") -> float:
        """
        Base method to calculate any manipulability index.

        :param workspace: The workspace instance providing access to the robot.
        :param joint_points: List of joint configurations to evaluate.
        :param method: The manipulability method to use ('yoshikawa', 'invcondition', 'asada').
        :param axes: Which axes to consider ('all', 'trans', 'rot').
        :return: The average manipulability index value.
        """
        if workspace.robot is None:
            raise ValueError("Robot is not set in the workspace")

        # Calculate manipulability for each joint configuration
        manipulability_values = np.array(
            [
                workspace.robot.manipulability(point, method=method, axes=axes)
                for point in joint_points
            ]
        )

        # Return the average manipulability
        return manipulability_values

    # Mapping of string identifiers to method functions
    METHOD_MAP = {"yoshikawa": yoshikawa, "invcondition": invcondition, "asada": asada}


class IndiceRegistry:
    """
    A registry class that provides a catalog of all available indices.
    """

    # Mapping from string identifiers to (function, description) tuples
    INDICES_MAP = {
        # Manipulability indices
        "yoshikawa": (
            ManipulabilityIndices.yoshikawa,
            "Yoshikawa manipulability index (determinant of Jacobian)",
        ),
        "invcondition": (
            ManipulabilityIndices.invcondition,
            "Inverse condition number of the Jacobian",
        ),
        "asada": (
            ManipulabilityIndices.asada,
            "Asada manipulability index (minimum singular value)",
        ),
    }

    @staticmethod
    def get_all_indices() -> Dict[str, Tuple[Callable, str]]:
        """
        Get a dictionary of all available indices with their functions and descriptions.

        :return: Dictionary mapping index names to (function, description) tuples.
        """
        return IndiceRegistry.INDICES_MAP

    @staticmethod
    def get_function(indice_name: str) -> Callable:
        """
        Get the function corresponding to the indice name.

        :param indice_name: The name of the indice.
        :return: The function that calculates the indice.
        :raises ValueError: If the indice name is not found.
        """
        if indice_name not in IndiceRegistry.INDICES_MAP:
            raise ValueError(f"Indice '{indice_name}' not found in registry.")
        return IndiceRegistry.INDICES_MAP[indice_name][0]

    @staticmethod
    def get_description(indice_name: str) -> str:
        """
        Get the description of the indice.

        :param indice_name: The name of the indice.
        :return: The description of the indice.
        :raises ValueError: If the indice name is not found.
        """
        if indice_name not in IndiceRegistry.INDICES_MAP:
            raise ValueError(f"Indice '{indice_name}' not found in registry.")
        return IndiceRegistry.INDICES_MAP[indice_name][1]


class IndiceManager:
    """
    A manager class that handles registration, retrieval, and calculation of indices
    for robotic workspace analysis.
    """

    def __init__(self):
        """Initialize the indice manager with the registry of standard indices.
        
        The manager does not store custom indices internally but only provides 
        access to the standard indices from the registry.
        """
        pass  # Standard indices are retrieved from the registry

    def add_indice(
        self, name: str, function: Callable, *args, description: str = "", **kwargs
    ):
        """
        Register a custom global indice function to the standard registry.
        
        Note: This method no longer stores the custom indices in the instance.
        Instead, it adds the function to the IndiceRegistry.

        :param name: The name of the custom indice.
        :param function: The callable function that computes the indice.
        :param args: Additional positional arguments for the function.
        :param description: A description of what the indice measures.
        :param kwargs: Additional keyword arguments for the function.
        """
        # Add the custom function to the registry instead of storing locally
        IndiceRegistry.INDICES_MAP[name] = (function, description)

    def get_indice(self, name: str) -> Tuple[Callable, Tuple, Dict, str]:
        """
        Retrieve a specific indice by name from the registry.

        :param name: The name of the indice.
        :return: Tuple containing (function, args, kwargs, description).
        :raises ValueError: If the indice name is not found.
        """
        # Check standard indices from registry
        if name in IndiceRegistry.INDICES_MAP:
            function, description = IndiceRegistry.INDICES_MAP[name]
            return (function, (), {}, description)

        raise ValueError(f"Indice '{name}' not found.")

    def list_indices(self) -> List[str]:
        """
        List all available indices from the registry.

        :return: List of all registered indice names.
        """
        return list(IndiceRegistry.INDICES_MAP.keys())

    def get_indices_info(self) -> Dict[str, str]:
        """
        Get information about all registered indices.

        :return: Dictionary mapping indice names to their descriptions.
        """
        # Get indices from the registry
        return {name: desc for name, (_, desc) in IndiceRegistry.INDICES_MAP.items()}

    def calculate(self, name: str, workspace, joint_points, *args, **kwargs) -> float:
        """
        Calculate a specific indice.

        :param name: The name of the indice to calculate.
        :param workspace: The workspace instance.
        :param joint_points: Joint configurations to evaluate.
        :param args: Additional arguments to pass to the indice function.
        :param kwargs: Additional keyword arguments to pass to the indice function.
        :return: The calculated indice value.
        :raises ValueError: If the indice name is not found.
        """
        function, _, _, _ = self.get_indice(name)

        # Calculate and return the indice using provided arguments
        return function(workspace, joint_points, *args, **kwargs)
