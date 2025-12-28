import pytest


def test_get_product_details_success(execute_query):
    """Verify that a valid product ID returns name, price, and suppliers."""
    query = """
    query GetProduct($id: ID!) {
      product(id: $id) {
        name
        price
        suppliers {
          companyName
          location
        }
      }
    }
    """
    variables = {"id": "1"}

    response = execute_query(query, variables)
    assert response.status_code == 200

    data = response.json().get("data").get("product")
    assert data is not None
    assert data["name"] == "Professional Laptop"
    assert isinstance(data["price"], float)
    assert isinstance(data["suppliers"], list)
    assert len(data["suppliers"]) > 0


def test_product_suppliers_limit(execute_query):
    """Verify the 'limit' argument on the suppliers field."""
    # This query tests the limit argument defined in your schema [cite: 3]
    query = """
    query GetLimitedSuppliers($id: ID!, $max: Int) {
      product(id: $id) {
        suppliers(limit: $max) {
          companyName
        }
      }
    }
    """
    limit_value = 1
    variables = {"id": "1", "max": limit_value}

    response = execute_query(query, variables)
    assert response.status_code == 200

    suppliers = response.json()["data"]["product"]["suppliers"]
    assert len(suppliers) == limit_value


def test_invalid_product_id(execute_query):
    """Verify response when an invalid product ID is provided."""
    query = """
    query GetProduct($id: ID!) {
      product(id: $id) {
        name
      }
    }
    """
    variables = {"id": "999"}

    response = execute_query(query, variables)
    assert response.status_code == 200

    # GraphQL returns 200 but the data object for the missing item should be null
    assert response.json()["data"]["product"] is None


def test_schema_violation_error(execute_query):
    """Verify that requesting a non-existent field returns a GraphQL error."""
    query = """
    query {
      product(id: "1") {
        nonExistentField
      }
    }
    """
    response = execute_query(query)
    # Most GraphQL servers return 400 for validation errors
    assert response.status_code == 400
    assert "errors" in response.json()