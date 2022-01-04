from graphql import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString

schema = GraphQLSchema(
    query=GraphQLObjectType(
        name="RootQueryType",
        fields={
            "hello": GraphQLField(GraphQLString, resolve=lambda obj, info: "world")
        },
    )
)
