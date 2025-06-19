# inherent from roboticstoolbox.models.Puma560
#!/usr/bin/env python
import roboticstoolbox.models.URDF.Puma560 as Puma560Base


class Puma560(Puma560Base):
    """
    Class that imports a Puma560 URDF model.
    """

    def __init__(self):
        super().__init__()
