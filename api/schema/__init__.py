import graphene

from api.schema import mutations, queries

schema = graphene.Schema(query=queries.Queries, mutation=mutations.Mutations)
