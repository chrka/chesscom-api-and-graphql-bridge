import os
from flask import Flask
from flask_graphql import GraphQLView
from .schema import schema

app = Flask(__name__)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)

if os.getenv('EXPOSE_GRAPHQL_BRIDGE', 'NO') == 'YES':
    app.run(host='0.0.0.0', port=5000)
else:
    app.run(port=5000)
