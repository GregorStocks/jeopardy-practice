import graphene


class Ping(graphene.Mutation):
    class Arguments:
        x = graphene.String()

    ping = graphene.String()

    def mutate(root, info, x):
        return Ping(ping=x)
