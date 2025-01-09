from roboticssandbox.example import define_panda



def test_define_panda():
    panda = define_panda()
    assert panda is not None, "Panda robot not defined"
