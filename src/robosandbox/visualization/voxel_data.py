import numpy as np
import pandas as pd
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt


class VoxelData:
    def __init__(self, df, voxel_size=0.05, method="order_independent_manipulability"):
        self.df = df
        self.voxel_size = voxel_size
        self.method = method
        self.voxels = None
        self.avg_metric = None
        self.grid_shape = None
        self.ranges = None
        self.total_voxels = None
        self.total_volume = None
        
        self._validate_method()
        self._create_voxel_workspace()
        
    def _validate_method(self):
        if self.method not in self.df.columns:
            available_columns = list(self.df.columns)
            raise ValueError(f"Method '{self.method}' not found in DataFrame columns. Available: {available_columns}")

    def _get_coordinate_ranges(self):
        coords = ["x", "y", "z"]
        return {coord: (self.df[coord].min(), self.df[coord].max()) for coord in coords}

    def _calculate_voxel_indices(self):
        coords = ["x", "y", "z"]
        indices = {}
        for coord in coords:
            min_val, max_val = self.ranges[coord]
            indices[f"{coord}_idx"] = ((self.df[coord] - min_val) / self.voxel_size).astype(int)
        return indices

    def _initialize_grids(self, indices):
        coords = ["x", "y", "z"]
        self.grid_shape = tuple(indices[f"{coord}_idx"].max() + 1 for coord in coords)
        self.voxels = np.zeros(self.grid_shape, dtype=bool)
        metric_sum = np.zeros(self.grid_shape)
        count_values = np.zeros(self.grid_shape, dtype=int)
        return metric_sum, count_values

    def _populate_voxel_data(self, indices, metric_sum, count_values):
        for i in range(len(self.df)):
            x_idx = indices["x_idx"][i]
            y_idx = indices["y_idx"][i]
            z_idx = indices["z_idx"][i]

            self.voxels[x_idx, y_idx, z_idx] = True
            metric_sum[x_idx, y_idx, z_idx] += self.df.iloc[i][self.method]
            count_values[x_idx, y_idx, z_idx] += 1

    def _calculate_average_metric(self, metric_sum, count_values):
        with np.errstate(divide="ignore", invalid="ignore"):
            self.avg_metric = np.divide(
                metric_sum,
                count_values,
                out=np.zeros_like(metric_sum),
                where=count_values > 0,
            )

    def _calculate_volume_stats(self):
        self.total_voxels = np.sum(self.voxels)
        self.total_volume = self.total_voxels * (self.voxel_size**3)

    def _create_voxel_workspace(self):
        self.ranges = self._get_coordinate_ranges()
        indices = self._calculate_voxel_indices()
        metric_sum, count_values = self._initialize_grids(indices)
        self._populate_voxel_data(indices, metric_sum, count_values)
        self._calculate_average_metric(metric_sum, count_values)
        self._calculate_volume_stats()

    def _get_metric_range(self):
        return (self.df[self.method].min(), self.df[self.method].max())

    def _create_color_mapping(self, metric_range, cmap_name):
        norm = Normalize(vmin=metric_range[0], vmax=metric_range[1])
        cmap = plt.cm.get_cmap(cmap_name)
        return norm, cmap

    def _apply_colors_to_voxels(self, norm, cmap, alpha):
        colors = np.zeros(self.voxels.shape + (4,))
        valid_voxels = np.where(self.voxels)
        
        if len(valid_voxels[0]) > 0:
            metric_values = self.avg_metric[valid_voxels]
            rgba_colors = cmap(norm(metric_values))
            rgba_colors[:, 3] = alpha
            colors[valid_voxels] = rgba_colors
            
        return colors

    def create_colors(self, cmap_name="viridis", alpha=0.7):
        metric_range = self._get_metric_range()
        norm, cmap = self._create_color_mapping(metric_range, cmap_name)
        colors = self._apply_colors_to_voxels(norm, cmap, alpha)
        return colors, norm, cmap

    def _setup_plot_figure(self, figsize):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection="3d")
        return fig, ax

    def _draw_voxels(self, ax, colors):
        ax.voxels(self.voxels, facecolors=colors, edgecolors="k", alpha=0.5, linewidth=0.1)

    def _calculate_axis_ticks(self, coord_index, min_val, max_val):
        tick_positions = np.linspace(0, self.grid_shape[coord_index] - 1, 5)
        tick_labels = np.linspace(min_val, max_val, 5)
        return tick_positions, tick_labels

    def _set_axis_properties(self, ax, coord, tick_positions, tick_labels):
        formatted_labels = [f"{val:.2f}" for val in tick_labels]
        
        if coord == "x":
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(formatted_labels)
            ax.set_xlabel("X (meters)")
        elif coord == "y":
            ax.set_yticks(tick_positions)
            ax.set_yticklabels(formatted_labels)
            ax.set_ylabel("Y (meters)")
        else:
            ax.set_zticks(tick_positions)
            ax.set_zticklabels(formatted_labels)
            ax.set_zlabel("Z (meters)")

    def _configure_axes(self, ax):
        coords = ["x", "y", "z"]
        coord_ranges = [self.ranges["x"], self.ranges["y"], self.ranges["z"]]
        
        for i, (coord, (min_val, max_val)) in enumerate(zip(coords, coord_ranges)):
            tick_positions, tick_labels = self._calculate_axis_ticks(i, min_val, max_val)
            self._set_axis_properties(ax, coord, tick_positions, tick_labels)

    def _add_colorbar(self, ax, norm, cmap):
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        label = self.method.replace("_", " ").title()
        plt.colorbar(sm, ax=ax, label=label, shrink=0.8)

    def _add_title(self):
        title = (
            f"Robot Workspace Voxel Representation\n"
            f"Voxels: {self.total_voxels:,} | "
            f"Volume: {self.total_volume:.4f} m³ | "
            f"Resolution: {self.voxel_size:.3f} m"
        )
        plt.title(title)

    def plot(self, figsize=(12, 9), cmap_name="viridis", alpha=0.7):
        colors, norm, cmap = self.create_colors(cmap_name, alpha)
        fig, ax = self._setup_plot_figure(figsize)
        self._draw_voxels(ax, colors)
        self._configure_axes(ax)
        self._add_colorbar(ax, norm, cmap)
        self._add_title()
        plt.tight_layout()
        return fig

    def get_statistics(self):
        fill_ratio = self.total_voxels / np.prod(self.grid_shape)
        return {
            "total_data_points": len(self.df),
            "voxel_size": self.voxel_size,
            "grid_dimensions": self.grid_shape,
            "occupied_voxels": self.total_voxels,
            "workspace_volume": self.total_volume,
            "fill_ratio": fill_ratio,
            "method": self.method
        }

    def print_statistics(self):
        stats = self.get_statistics()
        print(f"\nWorkspace Statistics:")
        print(f"├─ Method: {stats['method']}")
        print(f"├─ Total data points: {stats['total_data_points']:,}")
        print(f"├─ Voxel size: {stats['voxel_size']:.3f} m")
        print(f"├─ Grid dimensions: {stats['grid_dimensions']}")
        print(f"├─ Occupied voxels: {stats['occupied_voxels']:,}")
        print(f"├─ Workspace volume: {stats['workspace_volume']:.4f} m³")
        print(f"└─ Fill ratio: {stats['fill_ratio']:.3%}")


def create_test_data(n_points=1000):
    """Create synthetic robot workspace data for testing."""
    np.random.seed(42)
    
    # Generate points in a roughly spherical workspace
    theta = np.random.uniform(0, 2*np.pi, n_points)
    phi = np.random.uniform(0, np.pi, n_points)
    r = np.random.uniform(0.2, 0.8, n_points)
    
    # Convert to Cartesian coordinates
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi) + 0.5  # Offset to make it above ground
    
    # Generate synthetic manipulability metrics
    # Higher manipulability near center, lower at edges
    distance_from_center = np.sqrt(x**2 + y**2 + (z-0.5)**2)
    
    order_independent_manipulability = np.exp(-distance_from_center * 2) + np.random.normal(0, 0.1, n_points)
    order_independent_manipulability = np.clip(order_independent_manipulability, 0.01, 1.0)
    
    yoshikawa_manipulability = order_independent_manipulability * 0.8 + np.random.normal(0, 0.05, n_points)
    yoshikawa_manipulability = np.clip(yoshikawa_manipulability, 0.01, 0.8)
    
    condition_number = 1.0 / order_independent_manipulability + np.random.normal(0, 0.5, n_points)
    condition_number = np.clip(condition_number, 1.0, 50.0)
    
    # Create DataFrame
    data = {
        'x': x,
        'y': y,
        'z': z,
        'order_independent_manipulability': order_independent_manipulability,
        'yoshikawa_manipulability': yoshikawa_manipulability,
        'condition_number': condition_number
    }
    
    return pd.DataFrame(data)


def test_voxel_data():
    """Test function to validate VoxelData class functionality."""
    print("=" * 60)
    print("Testing VoxelData Class")
    print("=" * 60)
    
    # Create test data
    print("Creating synthetic robot workspace data...")
    df = create_test_data(n_points=2000)
    print(f"Generated {len(df)} data points")
    print(f"Workspace bounds: X[{df['x'].min():.2f}, {df['x'].max():.2f}], "
          f"Y[{df['y'].min():.2f}, {df['y'].max():.2f}], "
          f"Z[{df['z'].min():.2f}, {df['z'].max():.2f}]")
    
    # Test different methods
    methods_to_test = [
        "order_independent_manipulability",
        "yoshikawa_manipulability", 
        "condition_number"
    ]
    
    for i, method in enumerate(methods_to_test):
        print(f"\n{'-' * 40}")
        print(f"Test {i+1}: Testing method '{method}'")
        print(f"{'-' * 40}")
        
        try:
            # Create VoxelData instance
            voxel_data = VoxelData(df, voxel_size=0.1, method=method)
            print(f"✓ VoxelData created successfully")
            
            # Print statistics
            voxel_data.print_statistics()
            
            # Create plot
            print("Creating visualization...")
            fig = voxel_data.plot(figsize=(10, 8))
            print(f"✓ Plot created successfully")
            
            # Show plot
            plt.show()
            
        except Exception as e:
            print(f"✗ Error testing method '{method}': {e}")
    
    print(f"\n{'=' * 60}")
    print("Testing completed!")
    print(f"{'=' * 60}")


def main():
    """Main function to run tests."""
    test_voxel_data()


if __name__ == "__main__":
    main()