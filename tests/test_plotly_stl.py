import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

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


def create_inertia_ellipsoid(inertia_matrix, center, scale=1.0, resolution=20):
    """
    Create points for an inertia ellipsoid visualization
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

    # Scale by inverse square root of eigenvalues (for visualization)
    # Smaller eigenvalues = larger semi-axes (less resistance to rotation)
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


# Create the visualization
fig = go.Figure()

# 1. Add Center of Mass point
fig.add_trace(
    go.Scatter3d(
        x=[COM[0]],
        y=[COM[1]],
        z=[COM[2]],
        mode="markers",
        marker=dict(size=10, color="red", symbol="diamond"),
        name="Center of Mass",
        text=f"COM: ({COM[0]:.2f}, {COM[1]:.2f}, {COM[2]:.2f})",
        hovertemplate="<b>Center of Mass</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>",
    )
)

# 2. Create and add inertia ellipsoid
scale_factor = 10.0  # Adjust this to make ellipsoid visible
x_ell, y_ell, z_ell, eigenvals, eigenvecs = create_inertia_ellipsoid(
    Inertia_matrix, COM, scale=scale_factor
)

# Debug information for ellipsoid
print(f"Eigenvalues: {eigenvals}")
print(f"Ellipsoid X range: {np.min(x_ell):.2f} to {np.max(x_ell):.2f}")
print(f"Ellipsoid Y range: {np.min(y_ell):.2f} to {np.max(y_ell):.2f}")
print(f"Ellipsoid Z range: {np.min(z_ell):.2f} to {np.max(z_ell):.2f}")
print(f"COM position: {COM}")

fig.add_trace(
    go.Surface(
        x=x_ell,
        y=y_ell,
        z=z_ell,
        opacity=0.8,
        colorscale="Viridis",
        name="Inertia Ellipsoid",
        showscale=False,
        surfacecolor=np.ones_like(x_ell),
        cmin=0,
        cmax=1,
        hovertemplate="<b>Inertia Ellipsoid</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>",
    )
)

# 3. Add principal axes
axis_length = scale_factor * 0.5
colors = ["red", "green", "blue"]
axis_names = ["X-axis", "Y-axis", "Z-axis"]

for i in range(3):
    # Normalize eigenvalues for consistent axis scaling
    normalized_eigenval = eigenvals[i] / np.max(eigenvals)
    axis_end = COM + eigenvecs[:, i] * axis_length / np.sqrt(normalized_eigenval)

    fig.add_trace(
        go.Scatter3d(
            x=[COM[0], axis_end[0]],
            y=[COM[1], axis_end[1]],
            z=[COM[2], axis_end[2]],
            mode="lines+markers",
            line=dict(color=colors[i], width=6),
            marker=dict(size=[8, 4], color=colors[i]),
            name=f"Principal Axis {i + 1}",
            hovertemplate=f"<b>Principal Axis {i + 1}</b><br>Eigenvalue: {eigenvals[i]:.2e}<extra></extra>",
        )
    )

# # 4. Add coordinate system at origin
# origin_size = max(abs(COM)) * 0.3
# fig.add_trace(
#     go.Scatter3d(
#         x=[0, origin_size],
#         y=[0, 0],
#         z=[0, 0],
#         mode="lines",
#         line=dict(color="gray", width=3),
#         name="X-axis (global)",
#         showlegend=False,
#     )
# )
# fig.add_trace(
#     go.Scatter3d(
#         x=[0, 0],
#         y=[0, origin_size],
#         z=[0, 0],
#         mode="lines",
#         line=dict(color="gray", width=3),
#         name="Y-axis (global)",
#         showlegend=False,
#     )
# )
# fig.add_trace(
#     go.Scatter3d(
#         x=[0, 0],
#         y=[0, 0],
#         z=[0, origin_size],
#         mode="lines",
#         line=dict(color="gray", width=3),
#         name="Z-axis (global)",
#         showlegend=False,
#     )
# )

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
    width=2000,
    height=1700,
    margin=dict(l=0, r=0, t=40, b=0),
)

# Show the plot
fig.show()

# Print summary information
print("=" * 50)
print("INERTIA ANALYSIS SUMMARY")
print("=" * 50)
print(f"Volume: {Volume:.4f}")
print(f"Center of Mass: [{COM[0]:.4f}, {COM[1]:.4f}, {COM[2]:.4f}]")
print("\nInertia Matrix:")
for i, row in enumerate(Inertia_matrix):
    print(f"  [{row[0]:12.4e}, {row[1]:12.4e}, {row[2]:12.4e}]")

print(f"\nPrincipal Moments of Inertia (Eigenvalues):")
for i, val in enumerate(eigenvals):
    print(f"  I_{i + 1}: {val:.4e}")

print(f"\nPrincipal Axes (Eigenvectors):")
for i, vec in enumerate(eigenvecs.T):
    print(f"  Axis {i + 1}: [{vec[0]:8.4f}, {vec[1]:8.4f}, {vec[2]:8.4f}]")

# Create a 2D inertia matrix heatmap
fig_heatmap = go.Figure(
    data=go.Heatmap(
        z=Inertia_matrix,
        x=["Ixx", "Ixy", "Ixz"],
        y=["Iyx", "Iyy", "Iyz"],
        colorscale="RdBu",
        text=Inertia_matrix,
        texttemplate="%{text:.2e}",
        textfont={"size": 12},
        hoverongaps=False,
    )
)

fig_heatmap.update_layout(
    title="Inertia Matrix Heatmap",
    xaxis_title="Column",
    yaxis_title="Row",
    width=500,
    height=400,
)

fig_heatmap.show()
