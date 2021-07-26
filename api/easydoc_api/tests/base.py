import os


def init_mock_env():
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_USER'] = 'mock_db_user'
    os.environ['DB_PASSWORD'] = 'mock_db_pass'
    os.environ['DB_NAME'] = 'mock_db_name'
    os.environ['AI_CLIENT_ID'] = 'mock_ai_client_id'
    os.environ['AI_CLIENT_SECRET'] = 'mock_ai_secret_id'


def get_fixture_path(filename: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), f'fixture/{filename}')
