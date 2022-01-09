import graphene


class Queries(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "World"
