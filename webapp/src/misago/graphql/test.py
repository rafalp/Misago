import json


class GraphQLTestClient:
    def __init__(self, client, url):
        self.client = client
        self.url = url

    def query(self, query, variables=None):
        data = {"query": query}
        if variables:
            data["variables"] = variables
        response = self.client.post(
            self.url, json.dumps(data), content_type="application/json"
        )
        json_data = response.json()
        assert not json_data.get("errors"), json_data.get("errors")
        return json_data["data"]
