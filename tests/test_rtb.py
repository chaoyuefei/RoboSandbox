import roboticstoolbox as rtb
import numpy as np

panda = rtb.models.Panda()
mu = panda.manipulability(panda.qr, method="yoshikawa")
J = panda.jacob0(panda.qr)
print(f"Manipulability: {mu}")
mu_test = np.sqrt(abs(np.linalg.det(J @ J.T)))
print(f"Manipulability test: {mu_test}")

# def test_define_panda():
#     panda = define_panda()
#     assert panda is not None, "Panda robot not defined"


# if __name__ == "__main__":
#     robot = rtb.models.Panda()
#     robot.plot(block=True)
