import graphene

class Queries(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "World"

class Ping(graphene.Mutation):
    class Arguments:
        x = graphene.String()

    ping = graphene.String()

    def mutate(root, info, x):
        return Ping(ping=x)

class Mutations(graphene.ObjectType):
    ping = Ping.Field()

schema = graphene.Schema(
    query=Queries, mutation=Mutations
)
