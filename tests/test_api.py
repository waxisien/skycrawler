import context
from skycrawler.schema import schema


def test_get_all_builings(data_test):
    result = schema.execute('{buildings{name}}')
    assert len(result.data.get('buildings')) == 2


def test_get_all_cities(data_test):
    result = schema.execute('{cities{name}}')
    assert len(result.data.get('cities')) == 1

def test_get_a_building_by_id(data_test):
    result = schema.execute('{building(id:1){id,name,city{name}}}')
    assert result.data['building']['name'] == 'Building 1'
    assert result.data['building']['city']['name'] == 'Montreal'
