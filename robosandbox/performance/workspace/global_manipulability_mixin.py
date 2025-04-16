import numpy as np


class GlobalManipulabilityMixin:
    def calc_global_indice(
        self,
        method="yoshikawa",
        isNormalized=False,
    ):
        v = self.get_volume()
        S_max = self.df[method].max()
        S_sum = self.df[method].sum()
        S_rootb = (
            self.df[method].apply(lambda x: x ** (1 / (self.robot.dofs + 1))).sum()
        )
        if isNormalized:
            if S_max == 0:
                S_sum_div = S_sum / (len(self.df))
            else:
                S_sum_div = S_sum / (len(self.df) * S_max)
            # G = S_sum_div / v
            G = S_sum_div
            # G = S_rootb / (len(self.df))

        else:
            G = S_sum / len(self.df)
        return G

    def global_indice(
        self,
        initial_samples=3000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-2,
        method="yoshikawa",
        axes="all",
        max_samples=20000,
        is_normalized=False,
    ):
        """
        Computes the global indices for a given robotic manipulator.

        :param initial_samples: The starting number of random joint samples.
        :param batch_ratio: How many additional samples to add in each iteration.
        :param error_tolerance_percentage: The error threshold for stopping the iterations.
        :param method: The method used for calculating manipulability values.
        :param axes: The axes to calculate the manipulability.
        :param max_samples: The maximum number of samples to use.
        :returns: np.array, the computed global indices after convergence.

        The method starts by generating an initial set of joint configurations.
        Then, it adds the corresponding Cartesian points and manipulability values
        to the existing data. The calculation of global indices is performed iteratively,
        adjusting the number of samples according to the specified batch ratio and monitoring
        the relative error until it meets the defined tolerance or the maximum number of
        samples is reached.

        The main loop continues until the relative error between consecutive global index
        calculations is lower than the predefined tolerance percentage or the number of
        samples exceeds the maximum limit. Finally, the computed global index is returned.
        """

        # Generate initial samples of joint configurations.
        qlist = self.generate_joints_samples(initial_samples)

        # Add Cartesian points and corresponding manipulability values to the data.
        self.add_samples(
            points=self.get_cartesian_points(qlist),
            metric_values=self.calc_manipulability(qlist, method=method, axes=axes),
            metric=method,
        )

        # Initialize previous and current global indices.
        prev_G = 0
        current_G = self.calc_global_indice(method=method, isNormalized=is_normalized)

        # If the initial global index is zero, return early.
        if current_G == 0:
            return current_G

        # Calculate the relative error between global indices.
        err_relative = np.abs(prev_G - current_G) / current_G

        # Start the iteration process.
        iteration = 1
        while err_relative > error_tolerance_percentage and len(self.df) < max_samples:
            # Determine the number of additional samples to generate.
            num_samples = int(len(self.df) * batch_ratio)

            # Generate additional samples of joint configurations.
            qlist = self.generate_joints_samples(num_samples)

            # Add new Cartesian points and manipulability values to the data.
            self.add_samples(
                points=self.get_cartesian_points(qlist),
                metric_values=self.calc_manipulability(qlist, method=method, axes=axes),
                metric=method,
            )

            # Update previous and current global indices for the next iteration.
            prev_G = current_G
            current_G = self.calc_global_indice(
                method=method, isNormalized=is_normalized
            )

            # Recalculate the relative error.
            err_relative = np.abs(prev_G - current_G) / current_G
            iteration += 1

        # Return the computed global index after convergence.
        return current_G
