from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, ObjectType, MutationType
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, request, jsonify

# Load schema from the .graphql file [cite: 1]
type_defs = load_schema_from_path("schema.graphql")

# Mock Data
suppliers_db = {
    "s1": {"id": "s1", "companyName": "TechLogistics Corp", "location": "California"},
    "s2": {"id": "s2", "companyName": "Global Parts Ltd", "location": "London"},
    "s3": {"id": "s3", "companyName": "FastShip Inc", "location": "Tokyo"},
}

products_db = {
    "1": {"id": "1", "name": "Professional Laptop", "price": 1200.00, "supplier_ids": ["s1", "s2"]},
    "2": {"id": "2", "name": "Wireless Mouse", "price": 25.50, "supplier_ids": ["s3"]},
}

# Resolvers
query = ObjectType("Query")
mutation = MutationType()
product = ObjectType("Product")

@query.field("product")
def resolve_product(_, info, id):
    return products_db.get(id)

@product.field("suppliers")
def resolve_product_suppliers(product_obj, info, limit=None):
    ids = product_obj.get("supplier_ids", [])
    all_suppliers = [suppliers_db.get(sid) for sid in ids]
    return all_suppliers[:limit] if limit else all_suppliers

# New Mutation Resolver for deleting a product
@mutation.field("deleteProduct")
def resolve_delete_product(_, info, id):
    if id in products_db:
        del products_db[id]
        return True  # Deletion successful
    return False  # ID not found

schema = make_executable_schema(type_defs, [query, mutation, product])

app = Flask(__name__)
explorer_html = ExplorerGraphiQL().html(None)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return explorer_html, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=app.debug)
    return jsonify(result), 200 if success else 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)