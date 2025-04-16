import numpy as np
import plotly.graph_objects as go

# Create a grid from 0 to 20 without using j notation
x = np.linspace(0, 20, 21)
y = np.linspace(0, 20, 20)
z = np.linspace(0, 20, 20)

# Create the 3D grid using meshgrid
X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
print(x)

# Define the volume data
vol = (X - 10) ** 2 + (Y - 10) ** 2 + (Z - 10) ** 2

# Create the 3D volume plot
fig = go.Figure(
    data=go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=vol.flatten(),
        isomin=50,
        isomax=200,
        opacity=0.2,
        surface_count=21,
        caps=dict(x_show=False, y_show=False, z_show=False),  # no caps
    )
)

# Update layout for better visualization
fig.update_layout(
    title="3D Volume Plot (0-20 scale)",
    scene=dict(
        xaxis=dict(range=[0, 20]), yaxis=dict(range=[0, 20]), zaxis=dict(range=[0, 20])
    ),
)

fig.show()
