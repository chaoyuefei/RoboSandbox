import swift
import roboticstoolbox as rtb
import spatialmath as sm
# import numpy as np

# env = swift.Swift()
# env.launch(realtime=True)

panda = rtb.models.Panda()
panda.q = panda.qr
print(panda)
# env = swift.Swift()
# env.launch(realtime=False)
panda.plot(panda.qz, backend="swift")
