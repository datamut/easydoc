from .base import init_mock_env


def test_config():
    init_mock_env()

    from easydoc_api.config.config import app_config

    assert app_config.ai_client_id == 'mock_ai_client_id'
    assert app_config.ai_client_secret == 'mock_ai_secret_id'
    assert app_config.db_config.host == 'localhost'
    assert app_config.db_config.user == 'mock_db_user'
    assert app_config.db_config.password == 'mock_db_pass'
    assert app_config.db_config.port == 5432
    assert app_config.db_config.db_name == 'mock_db_name'
