import numpy as np


class GlobalManipulabilityMixin:
    def calc_global_indice(
        self,
        method="yoshikawa",
        isNormalized=False,
    ):
        v = self.get_volume()
        S_max = self.df[method].max()
        S_sum = self.df[method].sum(skipna=True)
        if isNormalized:
            S_sum_div = S_sum / (len(self.df) * S_max)
            G = S_sum_div / v
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
        Args:
            initial_samples: The starting number of random joint samples.
            batch_ratio: How many additional samples to add in each iteration.
            error_tolerance_percentage: The error threshold for stopping the iterations.
            method: The method used for calculating manipulability values.
            axes: The axes to calculate the manipulability.
            max_samples: The maximum number of samples to use.
        Returns:
            G: np.array, the computed global indices after convergence.
        """
        qlist = self.generate_joints_samples(initial_samples)
        self.add_samples(
            points=self.get_cartesian_points(qlist),
            metric_values=self.calc_manipulability(qlist, method=method, axes=axes),
            metric=method,
        )
        prev_G = 0
        current_G = self.calc_global_indice(method=method, isNormalized=is_normalized)
        err_relative = np.abs(prev_G - current_G) / current_G
        iteration = 1
        while err_relative > error_tolerance_percentage and len(self.df) < max_samples:
            num_samples = int(len(self.df) * batch_ratio)
            qlist = self.generate_joints_samples(num_samples)
            self.add_samples(
                points=self.get_cartesian_points(qlist),
                metric_values=self.calc_manipulability(qlist, method=method, axes=axes),
                metric=method,
            )
            prev_G = current_G
            current_G = self.calc_global_indice(
                method=method, isNormalized=is_normalized
            )
            err_relative = np.abs(prev_G - current_G) / current_G
            iteration += 1
        return current_G
