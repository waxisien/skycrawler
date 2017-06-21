import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from model import Building as BuildingModel
from model import City as CityModel


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
    all_buildings = SQLAlchemyConnectionField(Building)
    all_cities = SQLAlchemyConnectionField(City)
    building = graphene.Field(Building)


schema = graphene.Schema(query=Query, types=[Building, City])
