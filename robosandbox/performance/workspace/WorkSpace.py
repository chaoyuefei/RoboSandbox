from robosandbox.visualization.plotly_WorkSpace import PlotlyWorkSpace
from .base_workspace import BaseWorkSpace
from .sampling_mixin import SamplingMixin
from .manipulability_mixin import ManipulabilityMixin
from .global_manipulability_mixin import GlobalManipulabilityMixin


class WorkSpace(
    BaseWorkSpace,
    SamplingMixin,
    ManipulabilityMixin,
    GlobalManipulabilityMixin,
    PlotlyWorkSpace,
):
    """
    Complete WorkSpace class that combines all functionality from mixins
    """

    def __init__(self, robot=None):
        BaseWorkSpace.__init__(self, robot)
        PlotlyWorkSpace.__init__(self, df=self.df)
