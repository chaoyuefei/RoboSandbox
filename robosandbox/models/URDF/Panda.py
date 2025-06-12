# inherent from roboticstoolbox.models.Panda
#!/usr/bin/env python
import roboticstoolbox.models.URDF.Panda as PandaBase


class Panda(PandaBase):
    """
    Class that imports a Panda URDF model.

    This class extends the functionality of the base Panda class from the
    roboticstoolbox library, allowing for additional customizations or methods
    if needed in the future.
    """

    def __init__(self):
        super().__init__()
        # Additional initializations can be added here if necessary
