def test_graphql_route(app_client):
    page = app_client.post(
        '/graphql',
        data={'query': '{buildings{name}}'},
    )
    assert page.status_code == 200
