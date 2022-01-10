from flask import Flask
from graphql_server.flask import GraphQLView

from api.schema import schema
from api.db import db_session

app = Flask(__name__)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema.graphql_schema,
        graphiql=True,
    ),
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run()
