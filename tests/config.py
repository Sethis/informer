from src.config import reader


def test_config_create():
    reader_data = reader()

    assert reader_data.token != "None"
    assert isinstance(reader_data.redis_port, int)
    assert isinstance(reader_data.encoder_offset, int)
    assert isinstance(reader_data.redis_db, int)
    assert reader_data.encoder_offset >= 0
