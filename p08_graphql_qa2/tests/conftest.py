import pytest
import requests

@pytest.fixture(scope="session")
def api_url():
    # URL pointing to your running Docker container
    return "http://localhost:8000/graphql"

@pytest.fixture
def execute_gql(api_url):
    """Helper to execute GraphQL operations."""
    def _execute(query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        response = requests.post(api_url, json=payload)
        return response
    return _execute