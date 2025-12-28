import pytest

# Test Data Constants
VALID_PRODUCT_ID = "1"
NON_EXISTENT_ID = "999"


def test_mutation_delete_product(execute_gql):
    """
    Validates the deleteProduct mutation logic.
    Matches schema return type: Boolean!
    """
    mutation = """
    mutation RemoveItem($id: ID!) {
      deleteProduct(id: $id)
    }
    """
    variables = {"id": VALID_PRODUCT_ID}

    # Execute the mutation
    response = execute_gql(mutation, variables)
    assert response.status_code == 200

    result = response.json().get("data", {}).get("deleteProduct")
    assert isinstance(result, bool)

