import graphene

from api.schema.mutations.ping import Ping


class Mutations(graphene.ObjectType):
    ping = Ping.Field()
