import graphene

from api.db import db_session
from api import models


class Queries(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "World"

    num_games = graphene.Int()

    def resolve_num_games(self, info):
        return db_session.query(models.Game).count()
