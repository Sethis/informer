import pytest

from src.presentation.render.code import SimpleCodeRender, CodeData


def test_simple_code_render_default_separator():
    render = SimpleCodeRender()

    input_data = CodeData(code_id=1, unencrypted_payload="SomePayload")

    encoded = render.encode(
        input_data
    )

    assert render.decode(encoded) == input_data


def test_hard_code_render_default_separator():
    render = SimpleCodeRender()

    input_data = CodeData(code_id=123123123, unencrypted_payload="SomePayload")

    encoded = render.encode(
        input_data
    )

    assert render.decode(encoded) == input_data

def test_hard_code_render_with_another_separator():
    render = SimpleCodeRender(separator="&")

    input_data = CodeData(code_id=123123123, unencrypted_payload="Some_Payload_")

    encoded = render.encode(
        input_data
    )

    assert render.decode(encoded) == input_data

def test_error_with_separator():
    render = SimpleCodeRender()

    input_data = CodeData(code_id=123123123, unencrypted_payload="Some_Payload_")

    encoded = render.encode(
        input_data
    )

    with pytest.raises(ValueError) as handled_error:
        assert render.decode(encoded) == input_data

    assert str(handled_error.value) == (
        "It was required to get 2 results after splitting but 4 were given"
    )
