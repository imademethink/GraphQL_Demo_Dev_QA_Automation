from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, ObjectType
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, request, jsonify

# 1. Load Schema
type_defs = load_schema_from_path("schema.graphql")

# 2. Mock Data with Nested Relationships
suppliers_db = {
    "s1": {"id": "s1", "companyName": "TechLogistics Corp", "location": "California"},
    "s2": {"id": "s2", "companyName": "Global Parts Ltd", "location": "London"},
    "s3": {"id": "s3", "companyName": "FastShip Inc", "location": "Tokyo"},
    "s4": {"id": "s4", "companyName": "Quality Goods Co", "location": "Berlin"},
}

products_db = {
    "1": {
        "id": "1",
        "name": "Professional Laptop",
        "price": 1200.00,
        "supplier_ids": ["s1", "s2", "s3"]  # Three suppliers for this product
    },
    "2": {
        "id": "2",
        "name": "Wireless Mouse",
        "price": 25.50,
        "supplier_ids": ["s2", "s3", "s4"]
    }
}

# 3. Define Resolvers
query = ObjectType("Query")
product = ObjectType("Product")

@query.field("product")
def resolve_product_query(_, info, id):
    return products_db.get(id)


@product.field("suppliers")
def resolve_product_suppliers(product_obj, info, location=None, limit=None):
    ids = product_obj.get("supplier_ids", [])
    all_suppliers = [suppliers_db.get(sid) for sid in ids]

    # Filtering logic
    if location:
        all_suppliers = [s for s in all_suppliers if
                         s['location'].lower() == location.lower()]

    # Limit logic
    if limit:
        all_suppliers = all_suppliers[:limit]

    return all_suppliers

schema = make_executable_schema(type_defs, [query, product])

# 4. Flask App Setup
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