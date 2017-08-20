import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from skycrawler.model import Building as BuildingModel
from skycrawler.model import City as CityModel


class Building(SQLAlchemyObjectType):

    class Meta:
        model = BuildingModel
        interfaces = (relay.Node, )


class City(SQLAlchemyObjectType):

    class Meta:
        model = CityModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    buildings = graphene.List(Building)
    cities = graphene.List(City)
    building = graphene.Field(Building, id=graphene.ID())

    def resolve_buildings(self, args, context, info):
        query = Building.get_query(context)
        return query.filter(BuildingModel.is_active == 1).all()

    def resolve_building(self, args, context, info):
        query = Building.get_query(context)
        return query.get(args['id'])

    def resolve_cities(self, args, context, info):
        query = City.get_query(context)
        return query.all()

schema = graphene.Schema(query=Query, types=[Building, City])
