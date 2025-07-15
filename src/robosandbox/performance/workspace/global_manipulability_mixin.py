"""
This module provides the GlobalManipulabilityMixin class which computes global indices
for a robotic manipulator. It supports the default calculation method as well as user-defined
custom indice functions.
"""

import numpy as np


class GlobalManipulabilityMixin:
    def add_indice(self, name, function_to_calc):
        """
        Add a custom global indice function.

        :param name: str
            The name of the custom indice.
        :param function_to_calc: callable
            A function that accepts the workspace instance (self) and returns a numerical value.
        """
        if not hasattr(self, "_global_index_functions"):
            self._global_index_functions = {}
        self._global_index_functions[name] = function_to_calc

    def calc_global_indice(self, method="yoshikawa", isNormalized=False):
        """
        Calculate the default global indice.

        :param method: str, optional
            The metric to use for calculation (default is "yoshikawa").
        :param isNormalized: bool, optional
            Flag indicating whether to normalize the indice (default is False).
        :return: float
            The computed global indice value.
        """
        v = self.get_volume()
        S_max = self.df[method].max()
        S_sum = self.df[method].sum()
        S_rootb = self.df[method].apply(lambda x: x ** (1 / (self.robot.dofs + 1))).sum()

        if isNormalized:
            if S_max == 0:
                S_sum_div = S_sum / len(self.df)
            else:
                S_sum_div = S_sum / (len(self.df) * S_max)
            G = S_sum_div
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
        Compute the global indice for the robotic manipulator.

        The function generates an initial set of joint samples, calculates the corresponding
        Cartesian points and metric values, and computes the global indice. If a custom indice
        function has been registered with the given method, it will be used instead.

        :param initial_samples: int, optional
            The initial number of random joint samples (default is 3000).
        :param batch_ratio: float, optional
            The ratio of additional samples to add in each iteration (default is 0.1).
        :param error_tolerance_percentage: float, optional
            The relative error tolerance for iteration termination (default is 1e-2).
        :param method: str, optional
            The metric or custom indice name to use (default is "yoshikawa").
        :param axes: str, optional
            The axes to calculate the manipulability (default is "all").
        :param max_samples: int, optional
            The maximum number of samples allowed (default is 20000).
        :param is_normalized: bool, optional
            Flag indicating whether to normalize the indice computation (default is False).
        :return: float
            The computed global indice after convergence.
        """
        # Generate initial joint samples.
        qlist = self.generate_joints_samples(initial_samples)

        # Add Cartesian points and corresponding metric values to the data.
        self.add_samples(
            points=self.get_cartesian_points(qlist),
            metric_values=self.calc_manipulability(qlist, method=method, axes=axes),
            metric=method,
        )

        # Determine if a custom indice function is used.
        if hasattr(self, "_global_index_functions") and method in self._global_index_functions:
            current_G = self._global_index_functions[method](self)
        else:
            current_G = self.calc_global_indice(method=method, isNormalized=is_normalized)

        # Early return if the computed indice is zero.
        if current_G == 0:
            return current_G

        prev_G = 0
        err_relative = np.abs(prev_G - current_G) / current_G
        iteration = 1

        # Iteratively refine the global indice until convergence.
        while err_relative > error_tolerance_percentage and len(self.df) < max_samples:
            num_samples = int(len(self.df) * batch_ratio)
            qlist = self.generate_joints_samples(num_samples)

            self.add_samples(
                points=self.get_cartesian_points(qlist),
                metric_values=self.calc_manipulability(qlist, method=method, axes=axes),
                metric=method,
            )

            prev_G = current_G
            if hasattr(self, "_global_index_functions") and method in self._global_index_functions:
                current_G = self._global_index_functions[method](self)
            else:
                current_G = self.calc_global_indice(method=method, isNormalized=is_normalized)

            err_relative = np.abs(prev_G - current_G) / current_G
            iteration += 1

        return current_G
