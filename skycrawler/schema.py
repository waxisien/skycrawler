import graphene
from graphene import ObjectType, relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from skycrawler.model import Building as BuildingModel
from skycrawler.model import City as CityModel
from skycrawler.model import Synchronization as SynchronizationModel


class Building(SQLAlchemyObjectType):

    class Meta:
        model = BuildingModel
        interfaces = (relay.Node, )


class City(SQLAlchemyObjectType):

    class Meta:
        model = CityModel
        interfaces = (relay.Node,)


class Stats(ObjectType):
    last_synchronization = graphene.DateTime()
    total_buildings = graphene.Int()

    @staticmethod
    def resolve_last_synchronization(root, info):
        last_sync = SynchronizationModel.query.order_by(SynchronizationModel.id.desc()).first()
        if last_sync:
            return last_sync.syncDate

    @staticmethod
    def resolve_total_buildings(root, info):
        return BuildingModel.query.count()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    buildings = graphene.List(Building)
    cities = graphene.List(City)
    building = graphene.Field(Building, id=graphene.ID())
    stats = graphene.Field(Stats)

    def resolve_buildings(self, info):
        query = Building.get_query(info)
        return query.filter(BuildingModel.is_active == 1).all()

    def resolve_building(self, info, id):
        query = Building.get_query(info)
        return query.get(id)

    def resolve_cities(self, info):
        query = City.get_query(info)
        return query.all()

    def resolve_stats(self, info):
        return Stats()


schema = graphene.Schema(query=Query, types=[Building, City])
