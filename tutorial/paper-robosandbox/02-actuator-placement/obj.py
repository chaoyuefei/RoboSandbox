import robosandbox.models.DH.Generic as generic
from robosandbox.performance.workspace import WorkSpace


def obj(alpha1, alpha2, method="invcondition", axes="all", **kwargs):
    """Objective function to evaluate robot performance for given alpha values"""
    robot = generic.GenericFour(alpha=[alpha1, alpha2, 0, 0])
    ws = WorkSpace(robot=robot)
    G = ws.global_indice(
        initial_samples=3000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-3,
        method=method,
        axes=axes,
        max_samples=30000,
        is_normalized=kwargs.get("is_normalized", False),
    )
    return G
