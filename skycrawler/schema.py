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

    def resolve_buildings(self, info):
        query = Building.get_query(info)
        return query.filter(BuildingModel.is_active == 1).all()

    def resolve_building(self, info, id):
        query = Building.get_query(info)
        return query.get(id)

    def resolve_cities(self, info):
        query = City.get_query(info)
        return query.all()

schema = graphene.Schema(query=Query, types=[Building, City])
