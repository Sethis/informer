from src.adapters.encryption.code import CaesarCodeEncoder


def test_null_offset():
    encoder = CaesarCodeEncoder(offset=0, alphabet=["A", "B", "C"])

    assert "ABC" == encoder.encode("ABC")


def test_offset_1():
    encoder = CaesarCodeEncoder(offset=1, alphabet=["A", "B", "C"])

    assert "BCA" == encoder.encode("ABC")


def test_offset_2():
    encoder = CaesarCodeEncoder(offset=2, alphabet=["A", "B", "C"])

    assert "CAB" == encoder.encode("ABC")

def test_offset_defaul_null():
    encoder = CaesarCodeEncoder(offset=0)

    assert "ABC" == encoder.encode("ABC")


def test_offset_defaul_offset_2():
    encoder = CaesarCodeEncoder(offset=2)

    assert "CDEcde" == encoder.encode("ABCabc")


def test_get_code():
    encoder = CaesarCodeEncoder(offset=0, alphabet=["A"])

    assert "A"*8 == encoder.get_new_unencrypted_code(8)
