import pytest
import requests

@pytest.fixture(scope="session")
def api_url():
    # URL of your running Docker container or staging environment
    return "http://localhost:8000/graphql"

@pytest.fixture
def execute_query(api_url):
    def _execute(query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        response = requests.post(api_url, json=payload)
        return response
    return _execute