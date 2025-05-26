import numpy as np
import robosandbox as rsb
from robosandbox.performance.workspace.indice_manager import (
    IndiceManager,
    IndiceRegistry,
)
from robosandbox.performance.workspace.WorkSpace import WorkSpace


def main():
    """
    Example script to demonstrate the use of IndiceManager without custom indices storage.
    """
    print("Testing IndiceManager without custom indices storage")
    print("---------------------------------------------------")

    # Initialize the robot model
    robot = rsb.models.DH.Generic.GenericSeven()
    print(f"Robot model: {robot.name}")

    # Create a workspace with the robot
    workspace = WorkSpace(robot)

    # Generate some joint configurations to test
    num_samples = 5
    joint_points = workspace.generate_joints_samples(num_samples)
    print(f"Generated {num_samples} joint configurations")

    # Create an IndiceManager
    indice_manager = IndiceManager()

    # List available standard indices
    print("\nStandard indices available:")
    for name in indice_manager.list_indices():
        description = indice_manager.get_indices_info()[name]
        print(f"- {name}: {description}")

    # Calculate standard indices
    print("\nCalculating standard indices:")
    for name in ["yoshikawa", "invcondition", "asada"]:
        try:
            value = indice_manager.calculate(name, workspace, joint_points, axes="all")
            print(f"- {name}: {value}")
        except Exception as e:
            print(f"- {name}: Error - {str(e)}")

    # Define a custom indice function
    def custom_manipulability(workspace, joint_points, weight=1.0):
        """A custom indice that calculates a weighted sum of joint positions."""
        # Simple example: average joint position weighted by a factor
        if not joint_points:
            return 0.0

        joint_array = np.array(joint_points)
        return float(np.mean(joint_array) * weight)

    # Add the custom indice to the registry via IndiceManager
    print("\nAdding a custom indice:")
    indice_manager.add_indice(
        name="custom_weighted_avg",
        function=custom_manipulability,
        description="Custom weighted average of joint positions",
    )

    # Calculate the custom indice
    try:
        custom_value = indice_manager.calculate(
            "custom_weighted_avg", workspace, joint_points
        )
        print(f"- custom_weighted_avg: {custom_value}")

        # Calculate with a custom weight
        custom_value_weighted = indice_manager.calculate(
            "custom_weighted_avg", workspace, joint_points, weight=2.0
        )
        print(f"- custom_weighted_avg (weight=2.0): {custom_value_weighted}")
        print(
            f"  Ratio of weighted to unweighted: {custom_value_weighted / custom_value:.2f}"
        )
    except Exception as e:
        print(f"- custom_weighted_avg: Error - {str(e)}")

    # Create a new IndiceManager instance and verify it can access the custom indice
    print("\nCreating a new IndiceManager instance:")
    new_manager = IndiceManager()

    # List all indices including the custom one
    print("All indices available in new manager:")
    all_indices = new_manager.list_indices()
    for name in all_indices:
        print(f"- {name}")

    # Verify the custom indice can be calculated with the new manager
    if "custom_weighted_avg" in all_indices:
        value = new_manager.calculate("custom_weighted_avg", workspace, joint_points)
        print(f"Custom indice value from new manager: {value}")
        print("✅ Success: Custom indice accessible from new manager!")
    else:
        print("❌ Error: Custom indice not accessible from new manager")

    print("\nTest complete!")


if __name__ == "__main__":
    main()
