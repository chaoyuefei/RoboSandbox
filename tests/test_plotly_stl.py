"""
Inertia Matrix and Center of Mass Visualization Module

This module provides functions to visualize the center of mass and inertia ellipsoid
of a 3D object using Plotly.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


def create_inertia_ellipsoid(inertia_matrix, center, scale=1.0, resolution=20):
    """
    Create points for an inertia ellipsoid visualization.

    Args:
        inertia_matrix: 3x3 inertia tensor matrix
        center: Center point (COM) as numpy array
        scale: Scaling factor for visualization
        resolution: Number of points for sphere discretization

    Returns:
        Tuple of (x_coords, y_coords, z_coords, eigenvalues, eigenvectors)
    """
    # Get eigenvalues and eigenvectors
    eigenvals, eigenvecs = np.linalg.eigh(inertia_matrix)

    # Create sphere coordinates
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    U, V = np.meshgrid(u, v)

    # Unit sphere
    x_sphere = np.cos(U) * np.sin(V)
    y_sphere = np.sin(U) * np.sin(V)
    z_sphere = np.cos(V)

    # Stack coordinates
    sphere_points = np.stack(
        [x_sphere.flatten(), y_sphere.flatten(), z_sphere.flatten()]
    )

    # Normalize eigenvalues to make ellipsoid visible
    normalized_eigenvals = eigenvals / np.max(eigenvals)
    scaling = scale / np.sqrt(normalized_eigenvals)
    scaled_points = eigenvecs @ np.diag(scaling) @ sphere_points

    # Translate to center
    ellipsoid_points = scaled_points + center.reshape(3, 1)

    # Reshape back to grid
    x_ellipsoid = ellipsoid_points[0].reshape(resolution, resolution)
    y_ellipsoid = ellipsoid_points[1].reshape(resolution, resolution)
    z_ellipsoid = ellipsoid_points[2].reshape(resolution, resolution)

    return x_ellipsoid, y_ellipsoid, z_ellipsoid, eigenvals, eigenvecs


def plot_com(fig, com_position, marker_size=10, color="red"):
    """
    Add center of mass point to the plot.

    Args:
        fig: Plotly figure object
        com_position: Center of mass coordinates as numpy array
        marker_size: Size of the marker
        color: Color of the marker
    """
    fig.add_trace(
        go.Scatter3d(
            x=[com_position[0]],
            y=[com_position[1]],
            z=[com_position[2]],
            mode="markers",
            marker=dict(size=marker_size, color=color, symbol="diamond"),
            name="Center of Mass",
            text=f"COM: ({com_position[0]:.2f}, {com_position[1]:.2f}, {com_position[2]:.2f})",
            hovertemplate="<b>Center of Mass</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>",
        )
    )


def plot_inertia_ellipsoid(
    fig,
    inertia_matrix,
    com_position,
    scale_factor=10.0,
    opacity=0.4,
    colorscale=[[0, "rgb(178,223,138)"]],
):
    """
    Add inertia ellipsoid and principal axes to the plot.

    Args:
        fig: Plotly figure object
        inertia_matrix: 3x3 inertia tensor matrix
        com_position: Center of mass coordinates
        scale_factor: Scaling factor for ellipsoid size
        opacity: Transparency of the ellipsoid
        colorscale: Color scheme for the ellipsoid
    """
    # Create ellipsoid
    x_ell, y_ell, z_ell, eigenvals, eigenvecs = create_inertia_ellipsoid(
        inertia_matrix, com_position, scale=scale_factor
    )
    # Add ellipsoid surface
    fig.add_trace(
        go.Surface(
            x=x_ell,
            y=y_ell,
            z=z_ell,
            opacity=opacity,
            colorscale=colorscale,
            name="Inertia Ellipsoid",
            showscale=False,
            surfacecolor=np.zeros_like(x_ell),
            cmin=0,
            cmax=1,
            hovertemplate="<b>Inertia Ellipsoid</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>",
        )
    )

    # Add principal axes
    axis_length = scale_factor * 0.5
    colors = ["red", "green", "blue"]

    for i in range(3):
        # Normalize eigenvalues for consistent axis scaling
        normalized_eigenval = eigenvals[i] / np.max(eigenvals)
        axis_end = com_position + eigenvecs[:, i] * axis_length / np.sqrt(
            normalized_eigenval
        )

        fig.add_trace(
            go.Scatter3d(
                x=[com_position[0], axis_end[0]],
                y=[com_position[1], axis_end[1]],
                z=[com_position[2], axis_end[2]],
                mode="lines+markers",
                line=dict(color=colors[i], width=6),
                marker=dict(size=[8, 4], color=colors[i]),
                name=f"Principal Axis {i + 1}",
                hovertemplate=f"<b>Principal Axis {i + 1}</b><br>Eigenvalue: {eigenvals[i]:.2e}<extra></extra>",
            )
        )


def add_coordinate_system(fig, origin_size):
    """
    Add global coordinate system axes to the plot.

    Args:
        fig: Plotly figure object
        origin_size: Length of the coordinate axes
    """
    axes_data = [
        ([0, origin_size], [0, 0], [0, 0], "X-axis (global)"),
        ([0, 0], [0, origin_size], [0, 0], "Y-axis (global)"),
        ([0, 0], [0, 0], [0, origin_size], "Z-axis (global)"),
    ]

    for x_data, y_data, z_data, name in axes_data:
        fig.add_trace(
            go.Scatter3d(
                x=x_data,
                y=y_data,
                z=z_data,
                mode="lines",
                line=dict(color="gray", width=3),
                name=name,
                showlegend=False,
            )
        )


def create_inertia_heatmap(inertia_matrix):
    """
    Create a 2D heatmap visualization of the inertia matrix.

    Args:
        inertia_matrix: 3x3 inertia tensor matrix

    Returns:
        Plotly figure with heatmap
    """
    # Create custom text annotations for each cell
    annotations = []
    labels = [["Ixx", "Ixy", "Ixz"], ["Iyx", "Iyy", "Iyz"], ["Izx", "Izy", "Izz"]]

    for i in range(3):
        for j in range(3):
            annotations.append(
                dict(
                    x=j,
                    y=i,
                    text=f"{labels[i][j]}<br>{inertia_matrix[i][j]:.2e}",
                    showarrow=False,
                    font=dict(
                        color="white"
                        if abs(inertia_matrix[i][j])
                        > np.max(np.abs(inertia_matrix)) / 2
                        else "black"
                    ),
                )
            )

    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=inertia_matrix,
            x=["X", "Y", "Z"],
            y=["X", "Y", "Z"],
            colorscale="RdBu",
            showscale=True,
            hoverongaps=False,
            hovertemplate="<b>I%{y}%{x}</b><br>Value: %{z:.2e}<extra></extra>",
        )
    )

    fig_heatmap.update_layout(
        title="Inertia Matrix Heatmap",
        xaxis_title="Column (j)",
        yaxis_title="Row (i)",
        width=500,
        height=400,
        annotations=annotations,
    )

    return fig_heatmap


def print_report(volume, com_position, inertia_matrix):
    """
    Print a comprehensive analysis report of the inertia properties.

    Args:
        volume: Volume of the object
        com_position: Center of mass coordinates
        inertia_matrix: 3x3 inertia tensor matrix
    """
    # Calculate eigenvalues and eigenvectors
    eigenvals, eigenvecs = np.linalg.eigh(inertia_matrix)

    print("=" * 50)
    print("INERTIA ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Volume: {volume:.4f}")
    print(
        f"Center of Mass: [{com_position[0]:.4f}, {com_position[1]:.4f}, {com_position[2]:.4f}]"
    )

    print("\nInertia Matrix:")
    for i, row in enumerate(inertia_matrix):
        print(f"  [{row[0]:12.4e}, {row[1]:12.4e}, {row[2]:12.4e}]")

    print(f"\nPrincipal Moments of Inertia (Eigenvalues):")
    for i, val in enumerate(eigenvals):
        print(f"  I_{i + 1}: {val:.4e}")

    print(f"\nPrincipal Axes (Eigenvectors):")
    for i, vec in enumerate(eigenvecs.T):
        print(f"  Axis {i + 1}: [{vec[0]:8.4f}, {vec[1]:8.4f}, {vec[2]:8.4f}]")


def visualize_inertia_properties(
    volume, com_position, inertia_matrix, scale_factor=10.0, show_plots=True
):
    """
    Main function to visualize all inertia properties.

    Args:
        volume: Volume of the object
        com_position: Center of mass coordinates as numpy array
        inertia_matrix: 3x3 inertia tensor matrix
        scale_factor: Scaling factor for ellipsoid visualization
        show_plots: Whether to display the plots

    Returns:
        Tuple of (main_figure, heatmap_figure)
    """
    # Create main 3D visualization
    fig = go.Figure()

    # Add center of mass
    plot_com(fig, com_position)

    # Add inertia ellipsoid and principal axes
    plot_inertia_ellipsoid(fig, inertia_matrix, com_position, scale_factor)

    # Add coordinate system
    origin_size = max(abs(com_position)) * 0.3
    add_coordinate_system(fig, origin_size)

    # Update layout
    fig.update_layout(
        title={
            "text": "Center of Mass and Inertia Matrix Visualization",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 16},
        },
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            aspectmode="cube",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
        ),
        width=1200,
        height=900,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    # Create heatmap
    fig_heatmap = create_inertia_heatmap(inertia_matrix)

    # Show plots if requested
    if show_plots:
        fig.show()
        fig_heatmap.show()

    # Print analysis report
    print_report(volume, com_position, inertia_matrix)

    return fig, fig_heatmap


# Example usage with given data
if __name__ == "__main__":
    # Given data
    Volume = 2453.0099283854165
    COM = np.array([15.89999849, -7.89999265, 6.12640468])
    Inertia_matrix = np.array(
        [
            [8.95441448e04, 1.38562798e-01, -2.29828603e00],
            [1.38562798e-01, 2.60752037e05, 1.12978402e00],
            [-2.29828603e00, 1.12978402e00, 3.00661729e05],
        ]
    )

    # Create visualization
    main_fig, heatmap_fig = visualize_inertia_properties(
        Volume, COM, Inertia_matrix, scale_factor=10.0
    )
