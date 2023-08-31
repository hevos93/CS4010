from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

URL="https://www.vegvesen.no/trafikkdata/api/"

transport = AIOHTTPTransport(url=URL)

client = Client(transport=transport, fetch_schema_from_transport=True)

query= gql(
    """
        {
        trafficRegistrationPoints(
            searchQuery: {roadCategoryIds: [R], countyNumbers: [50], isOperational: true}
        ) {
            id
            name
            location {
            coordinates {
                latLon {
                lat
                lon
                }
            }
            }
        }
        }
    """
)

result = client.execute(query)
print(result)