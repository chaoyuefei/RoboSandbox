

def objective_global_indice(alpha2, alpha3, alpha4, method):
    robot = rsb.models.DH.Generic.GenericFour(alpha=[alpha2, alpha3, alpha4, 0])
    ws = WorkSpace(robot=robot)
    G = ws.iter_calc_global_indice(
        initial_samples=3000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-3,
        method=method,
        axes="all",
        max_samples=30000,
    )
    return G
