import plotly.graph_objects as go
import pandas as pd


class PlotlyWorkSpace:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def plot(
        self, color="invcondition", path="", fig=go.Figure(), isShow=True, isUpdate=True
    ):
        fig.add_trace(
            go.Scatter3d(
                x=self.df["x"],
                y=self.df["y"],
                z=self.df["z"],
                mode="markers",
                marker=dict(
                    size=5,
                    color=self.df[
                        color
                    ],  # set color to an array/list of desired values
                    colorscale="Viridis",  # choose a colorscale
                    colorbar=dict(title=color),
                    opacity=0.5,
                ),
            )
        )
        if isUpdate:
            fig.update_layout(
                scene=dict(
                    xaxis_title="X",
                    yaxis_title="Y",
                    zaxis_title="Z",
                ),
            )
        if isShow:
            fig.show()

    def plot_distribution(
        self,
        color="invcondition",
        num_bins=7,
        path="",
        fig=go.Figure(),
        isShow=True,
        isUpdate=True,
    ):
        min_value = self.df[color].min()  # Minimum value in the data
        max_value = self.df[color].max()  # Maximum value in the data

        data_range = max_value - min_value

        # Calculate the width of each bin
        bin_width = data_range / num_bins

        # Generate bin edges
        bins = [min_value + i * bin_width for i in range(num_bins + 1)]

        # Create bins using cut
        self.df["Binned Values"] = pd.cut(self.df[color], bins=bins, right=False)

        # Count the occurrences in each bin
        binned_counts = self.df["Binned Values"].value_counts().reset_index()
        binned_counts.columns = ["Range", "Count"]

        # Add a bar trace to the figure
        fig.add_trace(
            go.Bar(
                x=binned_counts["Range"].astype(
                    str
                ),  # Ensure the bin ranges are string type for proper display
                y=binned_counts["Count"],
                marker=dict(color="royalblue"),
                text=binned_counts["Count"],
                textposition="auto",
            )
        )

        # Update layout
        if isUpdate:
            fig.update_layout(
                title="Value Distribution by Quantile Range",
                xaxis_title="Value Range",
                yaxis_title="Count",
                template="plotly_white",
            )

        # Show the figure
        if isShow:
            fig.show()

    def plot_zero_approach(
        self,
        data_column="invcondition",
        thresholds=None,
        path="",
        fig=go.Figure(),
        isShow=True,
        isUpdate=True,
        color_scheme="Blues",
    ):
        """
        Plot the percentage of data points approaching zero compared to the total number of data points.

        Parameters:
        -----------
        data_column : str
            Column name containing the data to analyze
        thresholds : list
            List of threshold values to define the ranges approaching zero (default: [0.001, 0.01, 0.05, 0.1, 0.5, 1.0])
        path : str
            Path to save the figure
        fig : go.Figure
            Plotly figure object
        isShow : bool
            Whether to display the figure
        isUpdate : bool
            Whether to update the figure layout
        color_scheme : str
            Color scheme for the bars (blues, greens, reds, etc.)
        """
        # Set default thresholds if not provided
        if thresholds is None:
            thresholds = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0]

        # Ensure thresholds are sorted
        thresholds = sorted(thresholds)

        # Get absolute values to focus on proximity to zero
        abs_values = self.df[data_column].abs()

        # Total number of data points
        total_points = len(abs_values)

        # Calculate counts and percentages for each threshold
        ranges = ["< " + str(threshold) for threshold in thresholds]
        counts = [sum(abs_values < threshold) for threshold in thresholds]
        percentages = [(count / total_points) * 100 for count in counts]

        # Prepare data for plotting
        plot_data = pd.DataFrame(
            {"Range": ranges, "Count": counts, "Percentage": percentages}
        )

        # Generate a color gradient ourselves
        if color_scheme.lower() == "blues":
            colors = ["#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5"]
        elif color_scheme.lower() == "greens":
            colors = ["#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#41ab5d", "#238b45"]
        elif color_scheme.lower() == "reds":
            colors = ["#fee5d9", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d"]
        else:  # Default to blues
            colors = ["#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5"]

        # Make sure we have enough colors
        while len(colors) < len(ranges):
            colors.append(colors[-1])  # Repeat the last color if needed

        # Add a bar trace to the figure
        fig.add_trace(
            go.Bar(
                x=plot_data["Range"],
                y=plot_data["Percentage"],
                marker=dict(
                    color=colors[: len(ranges)],
                    line=dict(color="rgba(0,0,0,0.5)", width=0.5),
                ),
                text=[f"{p:.2f}%" for p in plot_data["Percentage"]],
                textposition="outside",
                hovertemplate="Range: %{x}<br>Percentage: %{y:.2f}%<br>Count: %{customdata}<extra></extra>",
                customdata=plot_data["Count"],
            )
        )

        # Update layout
        if isUpdate:
            fig.update_layout(
                # title="Percentage of Values Approaching Zero",
                xaxis_title="Range",
                yaxis_title="Percentage of Total (%)",
                template="plotly_white",
                bargap=0.2,
                height=600,
                width=800,
                margin=dict(l=50, r=50, t=80, b=50),
            )

            # # Add a line for reference at 50%
            # fig.add_shape(
            #     type="line",
            #     x0=-0.5,
            #     y0=50,
            #     x1=len(ranges) - 0.5,
            #     y1=50,
            #     line=dict(
            #         color="red",
            #         width=1,
            #         dash="dash",
            #     ),
            # )

        # Save the figure if path is provided
        if path:
            fig.write_image(path)

        # Show the figure
        if isShow:
            fig.show()

        return fig
