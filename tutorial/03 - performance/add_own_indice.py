import robosandbox as rsb


def global_isotropy_index(ws):
    """
    Custom global isotropic index function.
    This function computes the global isotropic index based on the mean of the
    'yoshikawa' and 'invcondition' columns in the DataFrame.
    """
    ws.robot.calc_manipulability(ws.df["q"].values, method="yoshikawa", axes="all")


robot = rsb.models.DH.Generic.GenericSeven()
ws = rsb.performance.workspace.WorkSpace(robot)
ws.add_indice(
    "custom_indice",
    lambda ws: ws.df["yoshikawa"].mean() + ws.df["invcondition"].mean(),
)
