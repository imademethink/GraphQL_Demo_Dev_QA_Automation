from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, ObjectType
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, request, jsonify

# Load schema
type_defs = load_schema_from_path("schema.graphql")

# Mock data (In a real project, this would come from a database)
products_db = {
    "1": {"id": "1", "name": "Professional Laptop", "price": 1200.00},
    "2": {"id": "2", "name": "Wireless Mouse", "price": 25.50},
}

# Define resolvers
query = ObjectType("Query")

@query.field("product")
def resolve_product(_, info, id):
    return products_db.get(id)

schema = make_executable_schema(type_defs, query)
app = Flask(__name__)
explorer_html = ExplorerGraphiQL().html(None)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return explorer_html, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)