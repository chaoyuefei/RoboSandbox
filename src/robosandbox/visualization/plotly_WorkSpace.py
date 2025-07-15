import plotly.graph_objects as go
import pandas as pd
# import plotly.express as px
# import numpy as np


class PlotlyWorkSpace:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def plot(
        self,
        color="invcondition",
        path="",
        fig=None,
        isShow=True,
        isUpdate=True,
        show_colorbar=True,
    ):
        if fig is None:
            fig = go.Figure()
        trace = go.Scatter3d(
            x=self.df["x"],
            y=self.df["y"],
            z=self.df["z"],
            mode="markers",
            marker=dict(
                size=5,
                color=self.df[color],
                colorscale="Viridis",
                opacity=0.5,
            ),
        )
        if show_colorbar:
            trace.marker["colorbar"] = dict(
                title=dict(text=color),
            )

        fig.add_trace(trace)
        # fig.add_trace(
        #     go.Scatter3d(
        #         x=self.df["x"],
        #         y=self.df["y"],
        #         z=self.df["z"],
        #         mode="markers",
        #         marker=dict(
        #             size=5,
        #             color=self.df[
        #                 color
        #             ],  # set color to an array/list of desired values
        #             colorscale="Viridis",  # choose a colorscale
        #             colorbar=dict(
        #                 title=dict(text=color),
        #                 # tickfont=dict(size=40),
        #             ),
        #             opacity=0.5,
        #         ),
        #     )
        # )
        if isUpdate:
            fig.update_layout(
                scene=dict(
                    xaxis_title="X",
                    yaxis_title="Y",
                    zaxis_title="Z",
                    # xaxis_title_font=dict(size=16),
                    # yaxis_title_font=dict(size=16),
                    # zaxis_title_font=dict(size=16),
                    # xaxis=dict(tickfont=dict(size=16)),
                    # yaxis=dict(tickfont=dict(size=16)),
                    # zaxis=dict(tickfont=dict(size=16)),
                ),
            )
        if isShow:
            fig.show()

        return fig

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
                textfont=dict(size=18),
                hovertemplate="Range: %{x}<br>Percentage: %{y:.2f}%<br>Count: %{customdata}<extra></extra>",
                customdata=plot_data["Count"],
            )
        )

        # Update layout
        if isUpdate:
            fig.update_layout(
                # title="Percentage of Values Approaching Zero",
                xaxis_title="Local Indice Range",
                yaxis_title="Percentage of Total (%)",
                xaxis=dict(tickfont=dict(size=18)),
                yaxis=dict(tickfont=dict(size=18)),
                xaxis_title_font=dict(size=18),
                yaxis_title_font=dict(size=18),
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

    # def plot_zero_approach_pie(
    #     self,
    #     data_column="invcondition",
    #     thresholds=None,
    #     path="",
    #     fig=go.Figure(),
    #     isShow=True,
    #     isUpdate=True,
    #     color_scheme="Blues",
    # ):
    #     """
    #     Plot the percentage of data points approaching zero compared to the total number of data points
    #     as a pie chart.

    #     Parameters:
    #     -----------
    #     data_column : str
    #         Column name containing the data to analyze
    #     thresholds : list
    #         List of threshold values to define the ranges approaching zero (default: [0.001, 0.01, 0.05, 0.1, 0.5, 1.0])
    #     path : str
    #         Path to save the figure
    #     fig : go.Figure
    #         Plotly figure object
    #     isShow : bool
    #         Whether to display the figure
    #     isUpdate : bool
    #         Whether to update the figure layout
    #     color_scheme : str
    #         Color scheme for the pie slices (Blues, Greens, Reds, Purples, Oranges, etc.)
    #     """
    #     # Set default thresholds if not provided
    #     if thresholds is None:
    #         thresholds = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0]

    #     # Ensure thresholds are sorted
    #     thresholds = sorted(thresholds)

    #     # Get absolute values to focus on proximity to zero
    #     abs_values = self.df[data_column].abs()

    #     # Total number of data points
    #     total_points = len(abs_values)

    #     # Calculate counts for each threshold range
    #     counts = []
    #     labels = []

    #     # For the first threshold
    #     count_first = sum(abs_values < thresholds[0])
    #     counts.append(count_first)
    #     labels.append(f"< {thresholds[0]}")

    #     # For intermediate thresholds
    #     for i in range(1, len(thresholds)):
    #         count = sum(
    #             (abs_values >= thresholds[i - 1]) & (abs_values < thresholds[i])
    #         )
    #         counts.append(count)
    #         labels.append(f"{thresholds[i - 1]} - {thresholds[i]}")

    #     # For values greater than the last threshold
    #     count_last = sum(abs_values >= thresholds[-1])
    #     if count_last > 0:
    #         counts.append(count_last)
    #         labels.append(f"≥ {thresholds[-1]}")

    #     # Define color maps based on the color scheme
    #     color_maps = {
    #         "blues": px.colors.sequential.Blues,
    #         "greens": px.colors.sequential.Greens,
    #         "reds": px.colors.sequential.Reds,
    #         "purples": px.colors.sequential.Purples,
    #         "oranges": px.colors.sequential.Oranges,
    #         "greys": px.colors.sequential.Greys,
    #         "ylorbr": px.colors.sequential.YlOrBr,
    #         "ylgnbu": px.colors.sequential.YlGnBu,
    #         "rdpu": px.colors.sequential.RdPu,
    #     }

    #     # Get the color scale based on the selected scheme
    #     color_scale = color_maps.get(color_scheme.lower(), px.colors.sequential.Blues)

    #     # For pie charts, we want distinct but related colors
    #     # Extract a subset from the color scale based on the number of slices needed
    #     if len(labels) <= len(color_scale):
    #         # If we have enough colors in the scale, select evenly spaced colors
    #         indices = np.linspace(0, len(color_scale) - 1, len(labels)).astype(int)
    #         colors = [color_scale[i] for i in indices]
    #     else:
    #         # If we need more colors than available in the scale, interpolate
    #         from scipy.interpolate import interp1d

    #         # Convert hex colors to RGB for interpolation
    #         def hex_to_rgb(hex_color):
    #             hex_color = hex_color.lstrip("#")
    #             return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    #         # Convert RGB back to hex
    #         def rgb_to_hex(rgb):
    #             return f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}"

    #         # Get RGB values for interpolation
    #         rgb_colors = [hex_to_rgb(color) for color in color_scale]

    #         # Create interpolation function for each RGB component
    #         r_interp = interp1d(
    #             np.linspace(0, 1, len(rgb_colors)), [c[0] for c in rgb_colors]
    #         )
    #         g_interp = interp1d(
    #             np.linspace(0, 1, len(rgb_colors)), [c[1] for c in rgb_colors]
    #         )
    #         b_interp = interp1d(
    #             np.linspace(0, 1, len(rgb_colors)), [c[2] for c in rgb_colors]
    #         )

    #         # Generate new colors
    #         new_points = np.linspace(0, 1, len(labels))
    #         colors = [
    #             rgb_to_hex((r_interp(x), g_interp(x), b_interp(x))) for x in new_points
    #         ]

    #     # Calculate percentages
    #     percentages = [(count / total_points) * 100 for count in counts]

    #     # Add a pie trace to the figure
    #     fig.add_trace(
    #         go.Pie(
    #             labels=labels,
    #             values=counts,
    #             marker=dict(
    #                 colors=colors, line=dict(color="rgba(255,255,255,0.5)", width=0.5)
    #             ),
    #             text=[f"{p:.2f}%" for p in percentages],
    #             textposition="inside",
    #             textfont=dict(size=14, color="white"),
    #             hovertemplate="Range: %{label}<br>Percentage: %{percent}<br>Count: %{value}<extra></extra>",
    #             textinfo="label+percent",
    #             insidetextorientation="radial",
    #         )
    #     )

    #     # Update layout
    #     if isUpdate:
    #         fig.update_layout(
    #             title="Distribution of Values Approaching Zero",
    #             template="plotly_white",
    #             height=600,
    #             width=800,
    #             margin=dict(l=50, r=50, t=80, b=50),
    #             legend=dict(
    #                 font=dict(size=14),
    #                 orientation="h",
    #                 yanchor="bottom",
    #                 y=-0.2,
    #                 xanchor="center",
    #                 x=0.5,
    #             ),
    #         )

    #     # Save the figure if path is provided
    #     if path:
    #         fig.write_image(path)

    #     # Show the figure
    #     if isShow:
    #         fig.show()

    #     return fig
