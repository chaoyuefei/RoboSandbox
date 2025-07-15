from typing import Callable, Dict, List, Tuple
import inspect
from . import robot_indices


def _get_index_functions_from_module():
    """
    Automatically discover all index functions from the robot_indices module.
    
    :return: Dictionary mapping function names to (function, description) tuples.
    """
    indices_map = {}
    
    # Get all functions from the robot_indices module
    for name, obj in inspect.getmembers(robot_indices, inspect.isfunction):
        # Skip private functions (starting with _)
        if name.startswith('_'):
            continue
            
        # Skip functions that don't belong to the robot_indices module
        if obj.__module__ != robot_indices.__name__:
            continue
            
        # Extract description from docstring
        description = ""
        if obj.__doc__:
            # Get the first line of the docstring as description
            lines = obj.__doc__.strip().split('\n')
            if lines:
                description = lines[0].strip()
        
        indices_map[name] = (obj, description)
    
    return indices_map


class IndiceRegistry:
    """
    A registry class that provides a catalog of all available indices.
    """

    # Dynamically populate indices map from robot_indices module
    INDICES_MAP = _get_index_functions_from_module()

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
    A manager class that handles registration, retrieval, and calculation of performance indices
    for robotic workspace analysis and optimization.
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
        Register a custom global performance index function to the standard registry.
        
        Note: This method no longer stores the custom indices in the instance.
        Instead, it adds the function to the IndiceRegistry.

        :param name: The name of the custom performance index.
        :param function: The callable function that computes the index.
        :param args: Additional positional arguments for the function.
        :param description: A description of what the index measures.
        :param kwargs: Additional keyword arguments for the function.
        """
        # Add the custom function to the registry instead of storing locally
        IndiceRegistry.INDICES_MAP[name] = (function, description)

    def get_indice(self, name: str) -> Tuple[Callable, Tuple, Dict, str]:
        """
        Retrieve a specific performance index by name from the registry.

        :param name: The name of the index.
        :return: Tuple containing (function, args, kwargs, description).
        :raises ValueError: If the index name is not found.
        """
        # Check standard indices from registry
        if name in IndiceRegistry.INDICES_MAP:
            function, description = IndiceRegistry.INDICES_MAP[name]
            return (function, (), {}, description)

        raise ValueError(f"Performance index '{name}' not found.")

    def list_indices(self) -> List[str]:
        """
        List all available performance indices from the registry.

        :return: List of all registered performance index names.
        """
        return list(IndiceRegistry.INDICES_MAP.keys())

    def get_indices_info(self) -> Dict[str, str]:
        """
        Get information about all registered performance indices.

        :return: Dictionary mapping performance index names to their descriptions.
        """
        # Get indices from the registry
        return {name: desc for name, (_, desc) in IndiceRegistry.INDICES_MAP.items()}

    def calculate(self, name: str, workspace, joint_points, *args, **kwargs) -> float:
        """
        Calculate a specific robot performance index.

        :param name: The name of the index to calculate.
        :param workspace: The workspace instance.
        :param joint_points: Joint configurations to evaluate.
        :param args: Additional arguments to pass to the index function.
        :param kwargs: Additional keyword arguments to pass to the index function.
        :return: The calculated index value.
        :raises ValueError: If the index name is not found.
        """
        function, _, _, _ = self.get_indice(name)

        # Calculate and return the indice using provided arguments
        return function(workspace, joint_points, *args, **kwargs)